# Exam Result Summarizer + Notifier 📊

A comprehensive Flask-based web application for automated exam result processing, student classification, LLM-powered feedback generation, and email notifications.

## Features ✨

- **📤 CSV Upload & Parsing** — Upload exam results (CSV/Excel), automatic validation and parsing
- **🔢 Intelligent Classification** — Classify students as Pass/Fail/Distinction with configurable thresholds
- **📊 Interactive Dashboard** — Real-time statistics with Chart.js visualizations:
  - Pass rate, average marks, median, top scorer
  - Distribution charts (Pass/Fail/Distinction pie chart)
  - Category-wise average marks
- **🤖 LLM Feedback Generation** — Personalized feedback using Hugging Face
  - Constructive messages tailored to student category
  - Supports mock feedback for testing
- **📧 Email Notifications** — Send formatted emails with:
  - Student marks and status
  - Personalized feedback
  - Mock/SMTP support (Gmail, custom SMTP)
- **🔐 User Authentication** — Demo login with admin/faculty roles
- **💾 SQLite Database** — Persistent storage of exams, students, classifications, feedbacks, and notifications
- **🎨 Responsive UI** — Bootstrap 5 design, mobile-friendly interface

## Quick Start 🚀

### Prerequisites
- Python 3.11+

### Setup — Using `uv` (Recommended) ⚡

If you have `uv` installed:

```bash
# 1. Clone the repository
cd /workspaces/Exam_Result_Summarizer_Notifier

# 2. Install dependencies using uv
uv sync

# 3. Optional: Configure environment variables
cp .env.example .env
# Edit .env with your email/HF settings (or skip for demo mode)

# 4. Run the application
python main.py
```

### Setup — Using `pip` + `venv` (Alternative)

If you don't have `uv`, use standard Python tools:

```bash
# 1. Clone the repository
cd /workspaces/Exam_Result_Summarizer_Notifier

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install dependencies from pyproject.toml
pip install -e .
# Or manually install:
# pip install flask pandas openpyxl huggingface-hub python-dotenv werkzeug flask-session

# 6. Optional: Configure environment variables
cp .env.example .env
# Edit .env with your email/HF settings (or skip for demo mode)

# 7. Run the application
python main.py
```

### Access the App
- **URL:** http://localhost:5000
- **Demo Admin Login:** `admin` / `admin123`
- **Demo Faculty Login:** `faculty` / `faculty123`

### Deactivating Virtual Environment
When done, deactivate the virtual environment:
```bash
deactivate
```

## Project Structure

```
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database schema & initialization
│   ├── routes/
│   │   ├── auth.py              # Login/logout routes
│   │   ├── upload.py            # CSV upload & classification
│   │   ├── dashboard.py         # Main dashboard & stats API
│   │   ├── results.py           # View parsed results
│   │   ├── feedback.py          # LLM feedback generation
│   │   └── notifications.py     # Email sending & logging
│   ├── services/
│   │   ├── csv_parser.py        # CSV/Excel parsing utility
│   │   ├── classifier.py        # Pass/Fail/Distinction logic
│   │   ├── summary.py           # Statistics aggregation
│   │   ├── llm_service.py       # Hugging Face integration
│   │   └── email_service.py     # SMTP email sender
│   ├── templates/
│   │   ├── base.html            # Base layout with navbar
│   │   ├── login.html           # Login page
│   │   ├── dashboard.html       # Exam list & overview
│   │   ├── upload.html          # File upload form
│   │   ├── results.html         # Student results table
│   │   ├── feedback.html        # Feedback generation UI
│   │   ├── notifications.html   # Email queue & logs
│   │   ├── exam_detail.html     # Detailed analytics
│   │   └── 404.html             # Error page
│   └── static/
│       ├── css/style.css        # Bootstrap + custom styling
│       └── js/charts.js         # Chart.js utilities
├── samples/
│   └── sample_exam_results.csv  # Example CSV for testing
├── uploads/                     # Uploaded CSV files (created at runtime)
├── database.db                  # SQLite database (created at first run)
├── main.py                      # Application entry point
├── pyproject.toml               # Project metadata & dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Usage Guide 📋

### Step 1: Login
1. Open http://localhost:5000
2. Use demo credentials: `admin` / `admin123`

### Step 2: Upload Exam Results
1. Navigate to **Upload Exam** (or click "Upload New Exam" on dashboard)
2. Fill in:
   - **Exam Name:** e.g., "Mid Semester Test"
   - **Course Name:** e.g., "Data Structures"
   - **CSV File:** Upload your results file
   - **Thresholds:** Configure Pass/Fail/Distinction cutoffs (default: 40/40/70)
3. Click **Upload & Process**

### Step 3: View Results
- **Dashboard:** Overview of all exams with key statistics
- **Results Page:** Detailed student-wise results table
- **Exam Analytics:** Charts (pie chart, bar chart, statistics)

### Step 4: Generate Feedback
1. Go to **Generate Feedback** tab for the exam
2. Click **🤖 Generate Feedback for All**
3. AI generates personalized feedback for each student
4. Edit individual feedback if needed

### Step 5: Send Notifications
1. Go to **Email Notifications** tab
2. Click **📤 Send Notifications to All**
3. Emails are sent to studentid@students.university.edu (mock)
4. Check **Sent Notifications** log

## CSV File Format 📄

Your CSV/Excel file must have these columns (order doesn't matter):

```csv
Student Id,Name,Course,Marks
S001,Alice Johnson,Data Structures,85
S002,Bob Smith,Data Structures,92
S003,Charlie Brown,Data Structures,45
```

- **Student Id:** Unique identifier (string)
- **Name:** Full name (string)
- **Course:** Course/subject name (string)
- **Marks:** Marks obtained (number, 0-100 recommended)

## Configuration ⚙️

### Thresholds (Configurable per Exam)
- **Pass Threshold:** Minimum marks to pass (default: 40%)
- **Distinction Threshold:** Minimum marks for distinction (default: 70%)
- **Classification Logic:**
  - **Distinction:** marks ≥ distinction_threshold
  - **Pass:** marks ≥ pass_threshold AND marks < distinction_threshold
  - **Fail:** marks < pass_threshold

### Environment Variables (.env)

```
# Email Configuration (SMTP)
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Hugging Face API
HF_API_KEY=your-huggingface-api-key

# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
```

**Note:** In demo mode (without .env), emails are mocked to console and LLM uses fallback feedback.

### Gmail SMTP Setup
1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use generated password as `EMAIL_PASSWORD` in .env

## Database Schema 🗄️

### Users Table
```sql
id, username, password_hash, role (admin/faculty), created_at
```

### Exams Table
```sql
id, name, course, created_by (user_id), pass_threshold, fail_threshold, distinction_threshold, created_at
```

### Students Table
```sql
id, exam_id, student_id, name, marks, created_at
```

### Classifications Table
```sql
id, student_id, exam_id, status (Pass/Fail/Distinction), feedback, created_at
```

### Notifications Table
```sql
id, student_id, exam_id, recipient_email, subject, message_body, status (sent/failed), sent_at, created_at
```

## LLM Feedback System 🤖

### Hugging Face Integration
The system supports multiple **FREE** Hugging Face models via the Inference API (verified to work):

| Model | ID | Speed | Quality | Best For |
|-------|-----|-------|---------|----------|
| **FLAN-T5** ⭐ (Default) | `flan-t5` | ⚡⚡⚡ Very Fast | ⭐⭐⭐ Good | **Recommended** - Most reliable |
| **FLAN-T5 Large** | `flan-t5-large` | ⚡⚡ Fast | ⭐⭐⭐⭐ Very Good | Better quality, slightly slower |
| **GPT-Neo** | `gpt-neo` | ⚡⚡ Fast | ⭐⭐⭐ Good | Good instruction-following |
| **GPT-2** | `gpt2` | ⚡⚡⚡ Very Fast | ⭐⭐ Basic | Fallback, always available |
| **Zephyr-7B** | `zephyr` | ⚡⚡ Fast | ⭐⭐⭐⭐ Very Good | High quality (if available) |

**Note:** Models like Mistral and Llama2 may not be available on free tier or require special access approval.

### Setup Instructions

#### Step 1: Get Hugging Face API Key
1. Visit [Hugging Face](https://huggingface.co/settings/tokens)
2. Create a new token with **repo.read** permission
3. Copy the token (starts with `hf_`)

#### Step 2: Configure .env File
```bash
# .env file
HF_API_KEY=hf_your_token_here
HF_MODEL=flan-t5  # Choose one: flan-t5, flan-t5-large, gpt-neo, gpt2, zephyr
```

#### Step 3: Test Your Configuration
```bash
python main.py
# Browse to http://localhost:5000
# Upload exam → Generate Feedback → You should see real AI-generated feedback!
```

### API Specifications
- **API Type:** Hugging Face Inference API (free tier available)
- **Input:** Student name, marks, category (Pass/Fail/Distinction), course
- **Output:** 2-3 sentence personalized feedback
- **Max Tokens:** 120 (optimized for concise feedback)
- **Temperature:** 0.6 (balanced between creative and consistent)

### Feedback Tone
- **Distinction:** Congratulatory + advanced topic exploration
- **Pass:** Encouraging + specific improvement areas  
- **Fail:** Supportive + key weak areas + study recommendations

### Model Recommendations

**Recommended for Production:** `mistral`
- Fast response times (< 2s per student)
- High-quality, instruction-aware feedback
- Balanced resource usage

**Recommended for Accuracy:** `llama2`
- Highest quality outputs
- Better contextual understanding
- Slower (3-5s per feedback)

**Recommended for Speed:** `flan-t5`
- Fastest inference (< 1s)
- Good for batch processing
- Slightly shorter feedback

### Mock Feedback (When HF_API_KEY is Empty)
If you haven't set an HF API key, the system automatically uses template-based mock feedback for all students. This is perfect for testing UI without API usage.

### Troubleshooting LLM Issues

**Problem:** "Failed to authenticate. Invalid token"
- ✓ Verify HF_API_KEY is correct and starts with `hf_`
- ✓ Ensure token has `repo.read` permission
- ✓ Check Hugging Face API status: https://status.huggingface.co

**Problem:** "Model not found"
- ✓ Verify HF_MODEL env variable matches one of the available models
- ✓ Check internet connectivity to Hugging Face

**Problem:** "Rate limit exceeded"
- ✓ Free tier has limits (~3000 requests/month)
- ✓ Fall back to mock feedback in production demos
- ✓ Consider Hugging Face Pro ($9/month) for unlimited

**Problem:** Slow feedback generation
- ✓ Try `flan-t5` or `phi` models (faster)
- ✓ Reduce batch sizes
- ✓ Generate feedback async (future feature)

### Monitoring LLM Usage
Log messages show which model is active:
```
[✅ LLM Service] Initialized with model: mistralai/Mistral-7B-Instruct-v0.1
```

Console also logs API errors with fallback to mock feedback.

## Testing 🧪

### Sample Data
A sample CSV file is included at `samples/sample_exam_results.csv` with 20 sample students.

### Test Workflow
1. Configure `.env` with HF_API_KEY (or leave empty for mock mode)
2. Upload `sample_exam_results.csv`
3. Set thresholds: Pass=40, Fail=40, Distinction=70
4. View dashboard statistics
5. Click **🤖 Generate Feedback for All** — watch real AI feedback appear!
6. Send test email notifications
7. Check notifications log

### Expected Results
- **Total Students:** 20
- **Distinctions:** ~6 students (marks ≥ 70)
- **Pass:** ~9 students (40 ≤ marks < 70)
- **Fail:** ~5 students (marks < 40)

## API Endpoints 🔌

### Authentication
- `POST /login` — User login
- `GET /logout` — User logout

### Dashboard
- `GET /dashboard` — Main dashboard
- `GET /dashboard/exam/<exam_id>` — Detailed exam analytics
- `GET /dashboard/api/exam/<exam_id>/stats` — JSON stats for charts

### Upload
- `POST /upload` — Upload and process CSV

### Results
- `GET /results/<exam_id>` — View results
- `GET /results/api/<exam_id>` — JSON results

### Feedback
- `POST /feedback/api/<exam_id>/generate` — Generate feedback for exam
- `GET /feedback/api/<exam_id>/student/<student_id>/feedback` — Get student feedback
- `POST /feedback/api/<exam_id>/student/<student_id>/feedback` — Update student feedback

### Notifications
- `POST /notifications/api/<exam_id>/send-email` — Send single email
- `POST /notifications/api/<exam_id>/send-batch` — Send emails to all students

## Dependencies 📦

- **Flask** — Web framework
- **Pandas** — CSV/Excel parsing
- **OpenPyXL** — Excel support
- **Hugging Face Hub** — LLM API
- **Torch** — ML framework (for HF)
- **Python-DotEnv** — Environment variable loading
- **Werkzeug** — Password hashing
- **Flask-Session** — Session management

Install via: `uv sync`

## Deployment 🌍

### For Production
1. Set `DEBUG=False` in .env
2. Use a real WSGI server (Gunicorn):
   ```bash
   uv run gunicorn -w 4 -b 0.0.0.0:5000 main:app
   ```
3. Migrate database to PostgreSQL for scalability
4. Set up CORS for multi-origin access
5. Use environment variables from secrets manager
6. Enable HTTPS with SSL certificates

### Docker Deployment
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
```

## Troubleshooting 🔧

### "No module named 'app'"
- Ensure you're running `python main.py` from project root
- Check `uv sync` completed successfully

### "database.db permission denied"
- Ensure write permission in project directory
- Delete `database.db` and restart (will recreate)

### LLM feedback returns None
- Check if HF_API_KEY is set in .env
- Verify Hugging Face API quota/rate limits
- Fallback mock feedback will be used automatically

### EmailService not sending
- Configure `.env` with valid SMTP credentials
- In demo mode, emails are logged to console
- Check email body formatting in email_service.py

### Chart.js not rendering
- Ensure no JavaScript errors in browser console
- Verify `/dashboard/api/exam/<id>/stats` returns valid JSON
- Check Chart.js CDN is accessible

## Future Enhancements 🚀

- [ ] Bulk export to PDF reports
- [ ] Student portal login
- [ ] Bulk email import (email addresses from CSV)
- [ ] WhatsApp notifications via Twilio
- [ ] Scheduled email campaigns
- [ ] Performance analytics & trends
- [ ] Automated grading rubrics
- [ ] Mobile app
- [ ] Multi-language support

## License 📄

This project is open-source and available under the MIT License.

## Support 💬

For issues or questions:
1. Check **Troubleshooting** section
2. Review logs in browser console (F12)
3. Ensure all dependencies installed: `uv sync`
4. Restart Flask app: `python main.py`

---

**Happy Exam Grading!** 🎓✨ Made with ❤️ for educators