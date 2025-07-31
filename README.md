Invoice Manager - AI-Powered Invoice Processing Web Application
A comprehensive Flask web application that uses OCR and AI technology to automatically extract and process invoice data. Upload invoice images, and the system will intelligently extract dates, amounts, items, and provide financial insights.

🚀 Features
User Authentication: Secure registration and login system with password hashing
Invoice Upload: Support for multiple image formats (PNG, JPG, JPEG, GIF)
OCR Text Extraction: Automatic text extraction from invoice images using RapidAPI OCR service
AI Data Processing: Google Gemini AI extracts structured data (dates, amounts, items) from invoice text
Transaction History: View all processed invoices with detailed information
Financial Dashboard: Spending summaries and transaction insights
AI Financial Advice: Personalized spending recommendations based on transaction patterns
Responsive Design: Dark theme Bootstrap interface that works on all devices
Database Storage: Secure PostgreSQL database for user data and transactions
📋 Prerequisites
Before installing, ensure you have:

Python 3.9+ installed
PostgreSQL database (local or cloud-hosted like Supabase)
API keys for external services (details below)
🛠️ Installation
1. Clone or Download the Project
git clone <your-repository-url>
cd invoice-manager
2. Install Dependencies
The project uses uv for dependency management. All required packages are listed in pyproject.toml:

# Dependencies will be automatically installed when running on Replit
# For local development, install:
pip install flask flask-sqlalchemy flask-login werkzeug psycopg2-binary
pip install google-genai requests gunicorn email-validator
3. Database Setup
Option A: Using Supabase (Recommended)
Go to Supabase Dashboard
Create a new project
Navigate to Settings → Database
Copy the connection string from "Connection string" → "Transaction pooler"
Replace [YOUR-PASSWORD] with your database password
Option B: Local PostgreSQL
Install PostgreSQL on your system
Create a new database for the application
Note your connection details
4. Environment Variables
Set up the following environment variables (in Replit Secrets or your .env file):

Required Variables:
DATABASE_URL: Your PostgreSQL connection string
SESSION_SECRET: A secure random string for session encryption
GEMINI_API_KEY: Google Gemini AI API key
RAPIDAPI_KEY: RapidAPI OCR service key
Example:
DATABASE_URL=postgresql://username:password@host:port/database
SESSION_SECRET=your-very-secure-random-string-here
GEMINI_API_KEY=your-gemini-api-key
RAPIDAPI_KEY=your-rapidapi-key
🔑 API Keys Setup
Google Gemini API Key
Go to Google AI Studio
Sign in with your Google account
Click "Create API Key"
Copy the generated key
RapidAPI OCR Key
Go to RapidAPI
Sign up for a free account
Subscribe to an OCR service (like "OCR Extract Text")
Copy your API key from the dashboard
🚀 Running the Application
On Replit
Upload your project files to a new Replit
Add your environment variables to Replit Secrets
The application will start automatically using the configured workflow
Local Development
# Start the application
python main.py
# Or using Gunicorn (production)
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
The application will be available at http://localhost:5000

📖 Usage Guide
1. User Registration & Login
Navigate to the homepage
Click "Register" to create a new account
Provide username, email, and secure password
Login with your credentials
2. Uploading Invoices
After logging in, click "Upload Invoice"
Select an image file containing an invoice (PNG, JPG, JPEG, GIF)
Maximum file size: 16MB
Click "Upload and Process"
3. Processing Flow
Image Upload: Your invoice image is securely uploaded
OCR Processing: RapidAPI extracts text from the image
AI Analysis: Google Gemini AI identifies:
Invoice date
Total amount
Individual items and prices
Vendor information
Database Storage: Processed data is saved to your account
4. Viewing Results
Dashboard: Overview of spending patterns and recent transactions
Transaction History: Detailed list of all processed invoices
Financial Advice: AI-generated insights based on your spending
5. Dashboard Features
Total Transactions: Count of processed invoices
Total Spending: Sum of all invoice amounts
Recent Transactions: Last 5 processed invoices
Monthly Insights: Spending breakdown and trends
🏗️ Project Structure
invoice-manager/
├── app.py                 # Flask application setup and database configuration
├── main.py               # Application entry point
├── models.py             # Database models (User, Transaction)
├── routes.py             # Web routes and request handlers
├── invoice_processor.py  # OCR and AI processing logic
├── static/
│   ├── css/
│   │   └── bootstrap-agent-dark-theme.min.css  # Local styling
│   └── uploads/          # Uploaded invoice images
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage/dashboard
│   ├── login.html        # User login form
│   ├── register.html     # User registration form
│   ├── upload.html       # Invoice upload form
│   ├── transactions.html # Transaction history
│   └── advice.html       # Financial advice page
├── pyproject.toml        # Project dependencies
└── README.md            # This file
