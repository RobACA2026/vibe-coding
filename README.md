# vibe-coding
vibe coding mirror
Vibe Code Extension & Streamlit Management Portal

An enterprise-ready freemium architecture pairing a browser extension with a Streamlit management dashboard and a validation API. Individual productivity features run directly inside the browser, while advanced collaboration and business tools unlock upon validating a license key generated in the portal.
Project Architecture

    Extension (/extension): Manifest V3 client application providing immediate local utility and peer workspace interfaces.

    Management Portal (/backend/app.py): Streamlit application handling user registration, license key management, domain telemetry, and subscription upgrades.

    Validation API (/backend/api.py): FastAPI execution endpoint validating license keys and serving active entitlement permissions to the browser extension.

Directory Structure

.
├── extension/             # Browser extension source code
│   ├── manifest.json      # Extension configuration file
│   ├── popup.html         # Extension popup interface
│   └── background.js      # Background service worker and state listener
├── backend/               # Streamlit application and validation backend
│   ├── app.py             # Streamlit management portal
│   ├── api.py             # FastAPI license validation engine
│   └── database.py        # Relational models and key verification logic
├── .env.example           # Environment template file
├── requirements.txt       # Python dependency list
└── README.md              # System documentation

Prerequisites

    Python: Version 3.10 or higher.

    Browser: Any Chromium-based browser (Google Chrome, Microsoft Edge, Brave) with Developer Mode enabled.

    Git: Installed on your local machine.

Environment Setup

    Clone the Repository:
    Bash

    git clone https://github.com/your-username/vibe-code-extension.git
    cd vibe-code-extension

    Create a Virtual Environment:
    Bash

    python -m venv venv
    source venv/bin/activate
    # On Windows: venv\Scripts\activate

    Install Dependencies:
    Bash

    pip install -r requirements.txt

    Configure Environment Variables:
    Copy the .env.example file to create your local .env file.
    Bash

    cp .env.example .env

    Open .env and configure your credentials:
    Code snippet

    DATABASE_URL=sqlite:///./app.db
    SECRET_KEY=your_secret_signing_key_here
    STRIPE_SECRET_KEY=sk_test_example

Running the Backend Services

    Start the Streamlit Management Portal:
    Bash

    streamlit run backend/app.py

    Access the web dashboard at http://localhost:8501.

    Start the Validation API:
    Run Uvicorn in a separate terminal window to handle API traffic from the extension.
    Bash

    uvicorn backend.api:app --reload --port 8000

    The API will run at http://localhost:8000.

Installing the Browser Extension

    Open your browser and navigate to chrome://extensions.

    Enable Developer mode using the toggle in the top-right corner.

    Click Load unpacked in the top-left menu.

    Select the extension/ directory from this repository.

    Confirm that the extension icon appears in your browser toolbar.

Demo Verification Workflow

    Navigate to the Streamlit portal at http://localhost:8501.

    Register a test user account and navigate to the License Management panel.

    Click Generate License Key to create a active business key.

    Click the extension icon in your browser toolbar to open the HUD.

    Click API Key: Unset, paste your generated key into the key manager, and click Connect API.

    Verify that the indicator updates to Connected and business capabilities activate in the extension popup.
