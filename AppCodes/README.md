````
# Invoice Manager – Smart Invoice Scanner & Expense Tracker

Invoice Manager is a Flask-based web application that enables users to register, log in, and upload invoices for automated data extraction using AI and OCR technologies. The system processes uploaded invoices and securely stores extracted data in a PostgreSQL database hosted on Supabase.

---

## 🚀 Key Features

- 🔐 User Authentication (Signup / Login)
- 📸 Invoice Upload and OCR Scanning via RapidAPI
- 🧠 Semantic Analysis using Gemini API
- 💾 Data Storage using Supabase PostgreSQL
- 🗂️ Dashboard to View Stored Invoices
- 📝 Automatic extraction of:
  - Vendor Name
  - Items Purchased
  - Amounts
  - Dates
  - Total Cost

---

## 🛠️ Tech Stack

| Layer             | Tool/Service                    |
|------------------|----------------------------------|
| Web Framework     | Flask                           |
| OCR               | RapidAPI (OCR Text Scanner)     |
| AI Language Model | Google Gemini API               |
| Database          | Supabase (PostgreSQL)           |
| ORM               | SQLAlchemy                      |
| Authentication    | Flask-Login                     |
| Env Management    | python-dotenv                   |
| Frontend          | HTML, Bootstrap (optional)      |
| Logging           | Python logging module           |

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/SnapSpend.git
   cd SnapSpend
````

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   Create a `.env` file in the root directory with the following:

   ```env
   DATABASE_URL=[Your Supabase DB URL]
   SUPABASE_KEY=[Your Supabase Service Role Key]
   GEMINI_API_KEY=[Your Gemini API Key]
   RAPIDAPI_KEY=[Your RapidAPI OCR Key]
   SESSION_SECRET=[Your Secret Key]
   FLASK_APP=app.py
   ```

   👉 Generate a session key using:

   ```python
   import os
   print(os.urandom(32).hex())
   ```

---

## 🔌 API Configuration

### 📦 Supabase (PostgreSQL)

* Create an account at [https://supabase.io](https://supabase.io)
* Create a new project and get your database URL and service key.
* Add them to your `.env` file as shown above.

### 🧠 Gemini API (Google Generative AI)

* Create an API key via [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
* Paste it into `.env`.

### 🔍 OCR via RapidAPI

* Visit:
  [OCR Text Scanner API](https://rapidapi.com/api4ai-api4ai-default/api/ocr43/playground/apiendpoint_c7d481a7-f86a-45f0-be7f-14f4d5383691)
* Subscribe to the API and paste the key into `.env`.

---

## ▶️ Running the App Locally

```bash
python main.py
```

Then open your browser and navigate to:
[http://localhost:8080](http://localhost:8080)

---

## 🔄 How It Works

1. **Register/Login**

   * Go to `/register` to sign up.
   * Log in via `/login`.

2. **Upload Invoice**

   * Navigate to the upload page.
   * Upload `.jpg`, `.png`, or `.pdf` invoice images.

3. **Invoice Scanning**

   * OCR API extracts raw text from the image.
   * Gemini API semantically interprets and structures the data.

4. **Store in Database**

   * Parsed data is saved in Supabase PostgreSQL.
   * Users can view uploaded invoices via the dashboard.

---

## 📡 Sample APIs Used

* ✅ **RapidAPI OCR**

  * Provider: OCR Text Scanner
  * API: `ocr-text-scanner.p.rapidapi.com`

* ✅ **Gemini (Google Generative AI)**

  * Provider: Google AI
  * API: `generativelanguage.googleapis.com`

* ✅ **Supabase**

  * PostgreSQL cloud database platform

---

## 🙏 Acknowledgements

* 💡 Google Gemini API – for semantic text analysis
* 📸 RapidAPI OCR – for text extraction from invoice images
* 🗃️ Supabase – for secure and scalable cloud database hosting

---

## 🔐 Security Notice

* **Do not commit `.env` files to GitHub**
  (Add `.env` to `.gitignore`!)

* Use hashed passwords and secure sessions.

* Keep all API keys and secrets safe.

---

## 📁 .gitignore (Recommended)

Make sure your `.gitignore` includes:

```
.env
venv/
__pycache__/
*.pyc
```
