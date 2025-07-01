# 🧪 Selenium Web Automation Framework with Dashboard & Docker

This is a **sample project** demonstrating web automation testing using **Selenium + Pytest**

## 📁 Project Structure

```
selenium-python-web-automation/
├── dashboard/            # Streamlit dashboard app
│   └── app.py
├── db/                   # SQLite DB for results
│   └── test_results.db
├── docker-compose.yml    # Services: test-runner & dashboard
├── Dockerfile            # Environment config
├── pages/                # Page Object Models
├── requirements.txt
├── tests/                # Test cases and pytest config
│   ├── conftest.py
│   └── test_login.py
├── utils/                # Utility scripts
│   └── logger.py
└── README.md
```

## ⚙️ Local Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/selenium-web-automation.git
cd selenium-web-automation
```

2. Create virtual environment & install dependencies:
```bash
python -m venv venv
venv\Scripts\activate       # Windows
# or
source venv/bin/activate    # Mac/Linux

pip install -r requirements.txt
```

3. Run tests:
```bash
pytest tests/ --browser=chrome
```

4. Launch dashboard:
```bash
streamlit run dashboard/app.py
```

## 🐳 Docker Setup (Cross-platform)

### 1. Build the container:
```bash
docker-compose build
```

### 2. Run tests (Chrome / Firefox):
```bash
docker-compose run test-runner
```

### 3. Launch dashboard:
```bash
docker-compose up dashboard
```

Access: http://localhost:8501

## 📊 Sample Dashboard (Preview)

![Screenshot 2025-07-01 202837](https://github.com/user-attachments/assets/62b397c2-8d29-45b1-9d0c-d984c4639907)

![Screenshot 2025-07-01 202904](https://github.com/user-attachments/assets/acc3a99c-f263-4ba4-98e3-5a01186c4116)


