import os
import json
import logging
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Transaction
from invoice_processor import process_invoice

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if current_user.is_authenticated:
        # retriving latest transactions for dashboard
        recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
            .order_by(Transaction.processed_at.desc()).limit(5).all()
        
        # Calculating total spending this month
        from datetime import date
        current_month = date.today().replace(day=1)
        monthly_total = db.session.query(db.func.sum(Transaction.total_amount))\
            .filter(Transaction.user_id == current_user.id,
                   Transaction.processed_at >= current_month).scalar() or 0
        
        return render_template('index.html', 
                             recent_transactions=recent_transactions,
                             monthly_total=monthly_total)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Preventing submitting empty field
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Registration error: {e}")
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(request.url)
        
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp on the name to prevent error
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            

            upload_dir = os.path.join(app.config['UPLOAD_FOLDER'])
            os.makedirs(upload_dir, exist_ok=True)
            
            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)
            
            try:
                invoice_data = process_invoice(filepath)
                
                #getting  data from image
                invoice_date = None
                due_date = None
                if invoice_data.get('invoice_date'):
                    try:
                        invoice_date = datetime.strptime(invoice_data['invoice_date'], '%Y-%m-%d').date()
                    except ValueError:
                        logging.warning(f"Could not parse invoice date: {invoice_data['invoice_date']}")
                
                if invoice_data.get('due_date'):
                    try:
                        due_date = datetime.strptime(invoice_data['due_date'], '%Y-%m-%d').date()
                    except ValueError:
                        logging.warning(f"Could not parse due date: {invoice_data['due_date']}")
                
                total_amount = 0.0
                if invoice_data.get('total_amount'):
                    try:
                        
                        amount_str = str(invoice_data['total_amount']).replace('$', '').replace(',', '')
                        total_amount = float(amount_str)
                    except ValueError:
                        logging.warning(f"Could not parse total amount: {invoice_data['total_amount']}")
                
                # recording data in db
                transaction = Transaction(
                    user_id=current_user.id,
                    invoice_date=invoice_date,
                    due_date=due_date,
                    total_amount=total_amount,
                    items_json=json.dumps(invoice_data.get('items', [])),
                    filename=filename,
                    raw_text=invoice_data.get('raw_text', '')
                )
                
                db.session.add(transaction)
                db.session.commit()
                
                flash('Invoice processed successfully!', 'success')
                return redirect(url_for('transactions'))
                
            except Exception as e:
                logging.error(f"Invoice processing error: {e}")
                flash('Failed to process invoice. Please try again.', 'danger')
                # Deleting the error file
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            flash('Invalid file type. Please upload an image file.', 'danger')
    
    return render_template('upload.html')

@app.route('/transactions')
@login_required
def transactions():
    from datetime import date

    today = date.today()
    page = request.args.get('page', 1, type=int)
    transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.processed_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('transactions.html', transactions=transactions,today=today)

@app.route('/advice')
@login_required
def advice():
    # Getting user's transactions for analysis
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    
    if not transactions:
        return render_template('advice.html', 
                             advice_text="No transaction data available yet. Upload some invoices to get personalized advice!",
                             monthly_spending=0,
                             avg_transaction=0,
                             total_transactions=0)
    
    # Calculate spending statistics
    total_spending = sum(t.total_amount for t in transactions)
    avg_transaction = total_spending / len(transactions) if transactions else 0
    
    # Monthly spending calculation
    from datetime import date
    current_month = date.today().replace(day=1)
    monthly_transactions = [t for t in transactions if t.processed_at.date() >= current_month]
    monthly_spending = sum(t.total_amount for t in monthly_transactions)
    
    # Generate advice based on spending patterns
    advice_text = generate_spending_advice(total_spending, avg_transaction, len(transactions), monthly_spending)
    
    return render_template('advice.html', 
                         advice_text=advice_text,
                         monthly_spending=monthly_spending,
                         avg_transaction=avg_transaction,
                         total_transactions=len(transactions))

def generate_spending_advice(total_spending, avg_transaction, num_transactions, monthly_spending):
    """Generate spending advice based on user's transaction data"""
    advice_points = []
    
    if avg_transaction > 100:
        advice_points.append("Your average transaction amount is quite high. Consider reviewing if all expenses are necessary.")
    
    if monthly_spending > 1000:
        advice_points.append("Your monthly spending is significant. Consider creating a budget to track your expenses better.")
    
    if num_transactions > 20:
        advice_points.append("You have many transactions. Consider consolidating purchases to reduce fees and better track spending.")
    
    if monthly_spending > total_spending * 0.5:
        advice_points.append("A large portion of your spending happened this month. Monitor your expenses closely.")
    

    if not advice_points:
        advice_points.append("Keep track of your expenses regularly to maintain good financial health.")
        advice_points.append("Consider setting monthly spending limits for different categories.")
    
    return " ".join(advice_points)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
