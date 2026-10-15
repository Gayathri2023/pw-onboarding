# 🏦 Digital Banking Onboarding - End-to-End Test Automation Suite

An enterprise-grade End-to-End (E2E) automation testing framework designed for a **Digital Banking Onboarding Platform (DigiDOB)**. Built using **Python**, **Playwright**, and **Pytest**, this framework automates complex customer acquisition and KYC (Know Your Customer) workflows across diverse retail, SME, and investment banking products.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Design Pattern](#-architecture--design-pattern)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Test Coverage & Products](#-test-coverage--products)
- [Technical Highlights & Challenges Solved](#-technical-highlights--challenges-solved)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Configuration](#database-configuration)
- [Executing Tests](#-executing-tests)
- [Reporting & Debugging](#-reporting--debugging)
- [Best Practices Implemented](#-best-practices-implemented)

---

## 🔍 Overview

The **DigiDOB Automation Suite** validates the paperless customer onboarding journey for financial institutions. The application under test is a modern Angular single-page application (SPA) that requires applicants to choose a product, agree to terms, satisfy eligibility criteria, authenticate via OTP, upload compliance documents, fill out multi-section personal and financial profiles, complete video liveness/recording, and digitally sign on an HTML5 canvas.

This framework replaces hours of manual regression and sanity testing with robust, repeatable automated test suites capable of handling real-world banking edge cases.

---

## ✨ Key Features

- **Page Object Model (POM)**: High maintainability with complete separation between UI locators/actions and test case logic.
- **Dynamic Database Integration for 2FA/OTP**: Integrates directly with MySQL via `PyMySQL` to retrieve transient one-time passwords during test execution, eliminating test flakiness and manual intervention.
- **Data-Driven Dynamic Test Data**: Leverages `Faker` to generate localized, valid test data on the fly (e.g., Malawi phone numbers `+265`, realistic dates of birth, names, addresses).
- **Complex UI Component Handling**:
  - HTML5 Canvas digital signatures using coordinate-based pointer actions.
  - Custom Angular reactive form controls (`ng-select`, `ngx-intl-tel-input`, custom radio & checkbox bindings).
  - Multi-document file uploads (`.png`, `.jpeg`) with automated warning dismissals.
  - Browser permissions management (`camera`, `microphone`, `geolocation`) for biometric and video KYC verification.
- **Modular Multi-Product Coverage**: Covers retail, SME, and investment products with employment-specific variants (employed, self-employed, unemployed, retired).

---

## 🏛 Architecture & Design Pattern

The test framework follows a layered **Page Object Model (POM)** architecture:

```
┌────────────────────────────────────────────────────────┐
│                      Test Layer                        │
│   (test_current_account.py, test_mlimi_account.py,...)  │
└──────────────────────────┬─────────────────────────────┘
                           │ Invokes
┌──────────────────────────▼─────────────────────────────┐
│                   Page Object Layer                    │
│   (landing, eligibility, personal_info, preview, etc.)  │
└──────────────┬──────────────────────────┬──────────────┘
               │                          │
┌──────────────▼─────────────┐ ┌──────────▼──────────────┐
│       Database Layer       │ │    Test Data Generation │
│    (PyMySQL OTP Query)     │ │        (Faker API)      │
└──────────────┬─────────────┘ └─────────────────────────┘
               │
┌──────────────▼─────────────────────────────────────────┐
│              Browser & Driver (Playwright)             │
│        (Chromium, WebKit, Firefox | Headless/Headed)    │
└────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.9+ | Core programming language |
| **Automation Engine** | Playwright (`playwright`, `pytest-playwright`) | Next-generation fast, reliable browser automation |
| **Test Runner** | Pytest | Test discovery, fixtures, parameterization, and reporting |
| **Database Connector** | PyMySQL | Direct query execution for backend 2FA / OTP validation |
| **Test Data Generation**| Faker | Generation of realistic emails, phone numbers, and dates |
| **Target Application** | Angular SPA | Single-page banking onboarding web application |

---

## 📂 Project Structure

```bash
tocode-testcase-main/
│
├── pages/                                # Page Object Model definitions
│   ├── landing.py                        # Product selection and entry navigation
│   ├── consent.py                        # Terms and privacy consent handling
│   ├── eligibility.py                    # Questionnaire & regulatory declarations
│   ├── personal_info.py                  # Primary KYC details (Phone, Email, DOB)
│   ├── otp.py                            # OTP verification flow (UI + DB integrated)
│   ├── recording.py                      # Video KYC recording simulation
│   ├── preview.py                        # Summary review & Canvas signature signing
│   └── finalize_application.py          # Final submission & core integration checks
│
├── utils/                                # Helper utilities and database helpers
│   └── test_db_connection.py             # MySQL connector to fetch user OTPs
│
├── backside_image.png                    # Test fixture: Sample ID/Document backside
├── front_image.png                       # Test fixture: Sample ID/Document front
│
├── test_application.py                   # Baseline E2E onboarding script
├── test_current_account.py               # E2E: Retail Current Account workflow
├── test_fixeddeposit.py                  # E2E: Investment Fixed Deposit workflow
├── test_minors_itf_account.py            # E2E: Minors / In Trust For (ITF) Account
├── test_mlimi_account.py                 # E2E: Agricultural (Mlimi) Account workflow
├── test_savings_ordinary.py              # E2E: Savings Ordinary Account workflow
├── test_savings_special_saver.py         # E2E: Savings Special Saver Account workflow
├── test_sole_proprietor_current.py       # E2E: SME Sole Proprietor Account workflow
├── test_stepup_entrepreneur.py           # E2E: SME Step Up Entrepreneur Account
├── test_student_serve.py                 # E2E: Student Serve Account workflow
│
├── test_so_employed.py                   # Scenario: Employed applicant journey
├── test_so_selfemployed.py               # Scenario: Self-employed applicant journey
├── test_so_unemployed.py                 # Scenario: Unemployed applicant journey
├── test_so_retired.py                    # Scenario: Retired applicant journey
├── test_add.py                           # Pytest unit testing sample
│
├── requirements.txt                      # Project dependencies
└── README.md                             # Documentation
```

---

## 🎯 Test Coverage & Products

The framework provides comprehensive test coverage across several banking product verticals:

### 1. Retail Banking Accounts
- **Current Account** (`test_current_account.py`): Full onboarding with salary slip, guardian certificate, and employment verification.
- **Savings Ordinary** (`test_savings_ordinary.py`): Primary savings account flow across all employment categories.
- **Savings Special Saver** (`test_savings_special_saver.py`): Premium savings variant requiring specialized KYC verifications.
- **Minors / ITF Account** (`test_minors_itf_account.py`): In-Trust-For accounts requiring guardian details and relationship proofs.
- **Student Serve** (`test_student_serve.py`): Student onboarding requiring university admission letters, college ID (`ADM_LTR`, `SCL_ID`), and student verification.
- **Mlimi Account** (`test_mlimi_account.py`): Specialized agricultural account onboarding requiring Tobacco Commission registration (`TOBCOM1`) and farming profile.

### 2. SME & Commercial Accounts
- **Sole Proprietor Current** (`test_sole_proprietor_current.py`): Business onboarding including date of incorporation, trading license, and tax information.
- **Step Up Entrepreneur** (`test_stepup_entrepreneur.py`): Micro-enterprise account onboarding flow.

### 3. Investment Products
- **Fixed Deposit Account** (`test_fixeddeposit.py`): High-interest term deposit account workflow.

---

## 💡 Technical Highlights & Challenges Solved

### 1. Automated OTP Extraction from MySQL Database
**Challenge**: Traditional automation fails at 2FA/OTP because SMS gateways introduce latency and flakiness.  
**Solution**: Implemented `utils/test_db_connection.py` using `pymysql`. When the user triggers "Get OTP", the test queries the backend database directly:
```python
cur.execute(f'SELECT mobile_otp FROM user_dtls WHERE user_email="{email}" AND user_phone="{mobile}";')
otp = cur.fetchone()[0]
```
The OTP is programmatically populated into sequential input boxes without mocking or manual delay.

### 2. HTML5 Canvas Digital Signature Automation
**Challenge**: Banking regulations require a hand-drawn customer signature on an HTML5 `<canvas>` element which lacks standard input fields.  
**Solution**: Utilized Playwright's mouse and coordinate-based click dispatch on the canvas locator:
```python
page.locator("canvas").click(position={"x": 306, "y": 141})
page.get_by_role("button", name="Save").click()
```

### 3. Handling Custom Angular Reactive Components
**Challenge**: Angular's `ng-select` and dynamic class names (e.g., `.ng-untouched.ng-pristine.ng-invalid`) make traditional XPath locators brittle.  
**Solution**: Prioritized Playwright's accessible locators (`get_by_role`, `get_by_placeholder`, `get_by_text`) paired with state waiters (`wait_for(state="visible")`) for robust synchronization.

### 4. Biometrics & Video KYC Simulation
**Challenge**: Modern onboarding triggers browser dialogs for camera, microphone, and geolocation permissions.  
**Solution**: Injected browser context permissions at initialization:
```python
context = browser.new_context(
    permissions=["camera", "microphone", "geolocation"],
    geolocation={"latitude": 12.9716, "longitude": 77.5946},
    locale="en-US"
)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js (for Playwright driver binaries)
- Access to MySQL database (or local instance)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd tocode-testcase-main
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

### Database Configuration

Ensure your MySQL database credentials in `utils/test_db_connection.py` match your target environment:

```python
conn = pymysql.connect(
    host='localhost',          # or UAT DB host
    user='root',
    password='your_password',
    database='onboarding'
)
```

---

## 🧪 Executing Tests

### Run all tests:
```bash
pytest
```

### Run a specific test suite:
```bash
# Run Current Account test
pytest test_current_account.py

# Run Student Serve test
pytest test_student_serve.py

# Run Mlimi (Agriculture) test
pytest test_mlimi_account.py
```

### Run in Headed mode (to view browser actions):
```bash
pytest test_current_account.py --headed
```

### Run with slow-motion (for visual debugging):
```bash
pytest test_current_account.py --headed --slowmo 500
```

### Run tests in parallel:
```bash
pytest -n auto
```

---

## 📊 Reporting & Debugging

- **Playwright Trace Viewer**: Inspect exact steps, network traffic, DOM snapshots, and execution timelines:
  ```bash
  playwright show-trace trace.zip
  ```
- **Pytest HTML Report**: Generate visual test reports:
  ```bash
  pytest --html=report.html --self-contained-html
  ```
- **Playwright Inspector (Code Generation / Interactive Debugging)**:
  ```bash
  playwright codegen https://digidobuat.ndayesa.co.mw/#/
  ```

---

## 🏆 Best Practices Implemented

- **DRY (Don't Repeat Yourself)**: Common screens (Consent, Personal Info, Eligibility, Video Recording, Preview) are centralized into reusable modules in `pages/`.
- **Dynamic Test Data**: Zero reliance on hardcoded phone numbers or emails; all applicant identities are generated dynamically using `Faker`.
- **Resilient Locators**: Avoided brittle auto-generated CSS selectors in favor of user-facing roles and labels.
- **Fail-Safe Uploads**: Modular per-document upload handlers that manage dropdown selections, file attachments, and dismiss system alerts.
