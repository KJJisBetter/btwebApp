from flask import Blueprint, render_template, flash, redirect, url_for, request, abort, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, TransactionForm, DeleteTransactionForm, FilterSortForm
from app.models import User, Transaction
from sqlalchemy import func
from datetime import datetime, timedelta


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# registration route
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', title='Register', form=form)

# login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('main.login'))
        
        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('main.dashboard'))
    
    return render_template('login.html', title='Login', form=form)

# logout route
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# dashboard route
@main.route('/dashboard')
@login_required
def dashboard():
    last_10_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).limit(10).all()
    return render_template('dashboard.html', transactions=last_10_transactions)


# profile route
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm(original_username=current_user.username, original_email=current_user.email)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.set_password(form.password.data)

        db.session.commit()

        flash('Account updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('profile.html', title='Profile', form=form)

# transactios route
@main.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    form = TransactionForm()
    
    if form.validate_on_submit():
        trasaction = Transaction(
            amount=form.amount.data,
            category=form.category.data,
            date=form.date.data,
            description=form.description.data,
            user_id=current_user.id
        )
        
        if form.category.data == 'Other':
            trasaction.category = form.custom_category.data

        db.session.add(trasaction)
        db.session.commit()

        flash('Transaction added successfully!', 'success')
        return redirect(url_for('main.transactions'))
    
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('transactions.html', title='Transactions', form=form, transactions=transactions)

@main.route ('/transaction/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    form = TransactionForm()

    if form.validate_on_submit():
        if category == 'Other':
            category = form.custom_category.data

        transaction.amount = form.amount.data
        transaction.category = form.category.data
        transaction.date = form.date.data
        transaction.description = form.description.data

        db.session.commit()

        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('main.transactions'))
    
    elif request.method == 'GET':
        form.amount.data = transaction.amount
        form.category.data = transaction.category
        form.date.data = transaction.date
        form.description.data = transaction.description

        #! man copilot is really amazing sometimes. it made this whole function by just my typting /update on the route

    return render_template('update_transaction.html', title='Update Transaction', form=form)

@main.route ('/transaction/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    form = DeleteTransactionForm()

    if transaction.user_id != current_user.id:
        abort(403)

    if form.validate_on_submit():
        db.session.delete(transaction)
        db.session.commit()

        flash('Transaction deleted successfully!', 'success')
        return redirect(url_for('main.transactions'))
    
    return render_template('delete_transaction.html', title='Delete Transaction', form=form)

# !kinda got it right. but it still loses the filter sometimes
#TODO: fix the filter and pagination to work together
@main.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    form = FilterSortForm()
    query = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc())

    if form.validate_on_submit():
        if form.start_date.data:
            query = query.filter(Transaction.date >= form.start_date.data)
        if form.end_date.data:
            query = query.filter(Transaction.date <= form.end_date.data)
        if form.sort.data:
            if form.sort.data == 'amount':
                query = query.order_by(Transaction.amount.desc())
            elif form.sort.data == 'date':
                query = query.order_by(Transaction.date.desc())
            elif form.sort.data == 'category':
                query = query.order_by(Transaction.category.desc())
        
        
        page = request.args.get('page', 1, type=int)
        transactions_pagination = query.paginate(page=page, per_page=10)
        transactions = transactions_pagination.items

        return render_template('history.html', transactions=transactions, pagination=transactions_pagination, form=form, filter_applied=True)

    
    else:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        sort = request.args.get('sort')

        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if sort:
            if sort == 'amount':
                query = query.order_by(Transaction.amount.desc())
            elif sort == 'date':
                query = query.order_by(Transaction.date.desc())
            elif sort == 'category':
                query = query.order_by(Transaction.category.desc())

        page = request.args.get('page', 1, type=int)
        transactions_pagination = query.paginate(page=page, per_page=10)
        transactions = transactions_pagination.items

        return render_template('history.html', transactions=transactions, pagination=transactions_pagination, form=form, filter_applied=False, start_date=start_date, end_date=end_date, sort=sort)




#api route
@main.route('/api/transactions/data')
@login_required
def transactions_data():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    data = {
        "labels": [transaction.date.strftime('%Y-%m-%d') for transaction in transactions],
        "data": [transaction.amount for transaction in transactions]
    }
    return jsonify(data)

@main.route('/api/daily_spending')
@login_required
def daily_spending():
    # Calculate the date one month ago from today
    one_month_ago = datetime.today() - timedelta(days=30)
    
    daily_spending_data = (
        db.session.query(
            func.date(Transaction.date).label('date'),
            func.sum(Transaction.amount).label('total')
        )
        .filter(Transaction.user_id == current_user.id, Transaction.date >= one_month_ago)
        .group_by(func.date(Transaction.date))
        .order_by(func.date(Transaction.date))
        .all()
    )
    
    data = {
        "labels": [entry.date.strftime('%Y-%m-%d') for entry in daily_spending_data],
        "data": [entry.total for entry in daily_spending_data]
    }
    return jsonify(data)


# about route
@main.route('/about')
def about():
    return render_template('about.html')
