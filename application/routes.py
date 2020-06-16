from application import app, db, bcrypt
from application.models import Product, Users, Orders, Order_line
from flask_login import login_user, current_user, logout_user, login_required, current_user
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm, OrdersForm
from flask import render_template, redirect, url_for, request
import pymysql
import sqlalchemy

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)

        user = Users(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hash_pw
            )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)



@app.route('/submit_board', methods=['GET', 'POST'])
@login_required
def submit_board():
    form = PostForm()
    if form.validate_on_submit():
        postData = Product(
            name=form.name.data,
            size=form.size.data,
            style=form.style.data,
            volume=form.volume.data,
            price=form.price.data,
            stock=form.stock.data
            )

        db.session.add(postData)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        print(form.errors)

    return render_template('post.html', title='Post', form=form)


@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
    user = current_user.id
    account = Users.query.filter_by(id=user).first()
    posts = Posts.query.filter_by(user_id=user)
    for post in posts:
        db.session.delete(post)
    logout_user()
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('register'))


@app.route('/')
@app.route('/home')
def home():
    postData = Product.query.all()
    return render_template('home.html', title='Home', product=postData)


@app.route('/Product/<productItem>', methods=["GET", "POST"])
def product(productItem):
    form = OrdersForm()
    theProduct = Product.query.filter_by(id=productItem).first()
    itemPrice = theProduct.price
    if int(productItem) > Product.query.count():
        return redirect(url_for('home'))
    elif not current_user.is_authenticated:
        return redirect(url_for('home'))
    elif form.validate_on_submit():
        orderData = Orders(
                customer = current_user
                )

        db.session.add(orderData)
        db.session.commit()

        order_lineData = Order_line(
                order_id = Orders.query.count(),
                product_id = productItem,
                quantity = form.quantity.data,
                total = (form.quantity.data * itemPrice)
                )
        if order_lineData.quantity > theProduct.stock:
            theOrder = Orders.query.filter_by(id=Orders.query.count()).first()
            db.session.delete(theOrder)
            db.session.commit()
            return redirect(url_for('home'))

        db.session.add(order_lineData)
        theProduct.stock -= order_lineData.quantity
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('product.html', title='Product', data=theProduct, form=form)




@app.route('/about')
def about():
    return render_template('about.html', title ='About')



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name        
        form.email.data = current_user.email        
    return render_template('account.html', title='Account', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
