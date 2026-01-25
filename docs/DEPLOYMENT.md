# Local Deployment Guide - Google Maps Business Scraper

This guide will help you deploy the complete project on your local machine.

---

## Prerequisites

Before starting, make sure you have:

- n8n installed (version 0.200.0 or higher)
- Python 3.8 or higher
- Apify account (free tier available)
- Google Cloud account with Sheets API enabled

---

## Step 1: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```bash
   # Apify API Key (REQUIRED)
   APIFY_API_KEY=apify_api_your_key_here
   
   # Google Cloud OAuth2 (REQUIRED)
   GOOGLE_CLIENT_ID=your_client_id_here
   GOOGLE_CLIENT_SECRET=your_client_secret_here
   
   # Google Sheets (REQUIRED)
   GOOGLE_SHEET_ID=your_spreadsheet_id_here
   ```

> **Note**: To get your Apify API Key, visit: https://console.apify.com/account/integrations

---

## Step 2: Install Python Dependencies (Optional)

**Good news**: The diagnostic scripts use only Python's standard library, so **no external dependencies are required**.

However, if you prefer to use a virtual environment (recommended for best practices):

```bash
# Create virtual environment (optional)
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies (currently empty, but ready for future additions)
pip install -r requirements.txt
```

**Without venv** (simpler approach):
```bash
# No installation needed - scripts work out of the box
python3 scripts/diagnostic.py
```

> **Note**: The `requirements.txt` file is currently empty because all scripts use Python's standard library only.

---

## Step 3: Start n8n

### Option A: npm installation
```bash
n8n start
```

### Option B: Docker
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

Access n8n at: http://localhost:5678

---

## Step 4: Verify System Health

Run the diagnostic tool to verify everything is configured correctly:

```bash
python3 scripts/diagnostic.py
```

Expected output:
```
============================================================
N8N Workflow Diagnostic Report
============================================================

[PASS] n8n Server Status
      Running at http://localhost:5678
[PASS] Environment Variable: APIFY_API_KEY
      Set
[PASS] Environment Variable: GOOGLE_SHEET_ID
      Set
[PASS] Apify API Connectivity
      API responding correctly
[PASS] Google Sheets URL
      https://docs.google.com/spreadsheets/d/...

============================================================
Summary
============================================================

Total Checks: 5
Passed: 5
Failed: 0

All checks passed. Workflow should be operational.
```

---

## Step 5: Configure Google Sheets

### 5.1 Create the Spreadsheet

Create a new Google Sheet with the following structure:

**Sheet 1: Query**
| Query | Location | Status |
|-------|----------|--------|
| gas stations | Queretaro, Mexico | false |

**Sheet 2: Data**
| Station_ID | Station_Name | address | Latitude | Longitude | Rating_Average | Total_Reviews | Open_24_Hours | Google_Maps_URL | Decision_Score |
|------------|--------------|---------|----------|-----------|----------------|---------------|---------------|-----------------|----------------|

**Sheet 3: Details** (Optional - for contact extraction)
| website | emails | linkedin | facebook | instagram | twitter |
|---------|--------|----------|----------|-----------|---------|

### 5.2 Get Sheet ID

The Sheet ID is in the URL:
```
https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
```

Add this to your `.env` file as `GOOGLE_SHEET_ID`.

---

## Step 6: Configure Credentials in n8n

### 6.1 Google Sheets OAuth2

1. In n8n, go to **Settings** → **Credentials**
2. Click **+ Add Credential**
3. Search and select **Google Sheets OAuth2 API**
4. Enter:
   - Client ID: (from `.env`)
   - Client Secret: (from `.env`)
5. Click **Connect my account**
6. Authorize access in the Google popup
7. Click **Save**

### 6.2 Apify Bearer Token

1. In n8n, go to **Settings** → **Credentials**
2. Click **+ Add Credential**
3. Search and select **HTTP Bearer Auth**
4. Name it: `Bearer Auth apyfy`
5. Enter your Apify API key
6. Click **Save**

---

## Step 7: Import Workflow

1. In n8n, click the **+** button (top right)
2. Select **Import from File**
3. Navigate to `workflows/gas_station_analyzer.json`
4. Click **Import**

---

## Step 8: Test the Workflow

1. Open the imported workflow
2. Click **Execute Workflow** (play button)
3. Verify each node executes successfully:
   - Read Pending Queries
   - Start Apify Scraping Job
   - Wait for Job Succeed
   - Check Scraping Status
   - Fetch Scraped Results
   - Save Business Data

4. Check your Google Sheet - you should see data in the "Data" tab

---

## Step 9: Activate Automatic Execution

To run the workflow automatically every 30 minutes:

1. In n8n, open the workflow
2. Click the **Active** toggle (top right)
3. The workflow will now run on schedule

---

## Useful Commands

### Check n8n Status
```bash
curl http://localhost:5678/healthz
```

### Run Diagnostic
```bash
python3 scripts/diagnostic.py
```

### Fix OAuth2 Issues
```bash
python3 scripts/fix_oauth.py
```

### Test Workflow
```bash
python3 scripts/test_workflow.py
```

---

## Troubleshooting

### Problem: "DNS error" when connecting to Apify

**Solution**: Check your network connection
```bash
ping api.apify.com
```

If ping fails, check:
1. Network connectivity
2. DNS settings
3. Firewall rules

### Problem: "OAuth2 authorization error"

**Solution**: Re-authenticate Google Sheets
```bash
python3 scripts/fix_oauth.py
```

Follow the instructions to reconnect your Google account.

### Problem: "Cannot find workflow file"

**Solution**: Verify file path
```bash
ls -la workflows/gas_station_analyzer.json
```

The file should exist in the `workflows/` directory.

### Problem: "Apify job failed"

**Solution**: Check Apify credits
1. Visit https://console.apify.com/
2. Check your account balance
3. Verify API key is valid

---

## Verify Everything Works

### 1. n8n
Visit: http://localhost:5678 - You should see the login interface.

### 2. Diagnostic
```bash
python3 scripts/diagnostic.py
```
All checks should pass.

### 3. Google Sheets
Open your spreadsheet - you should see scraped data in the "Data" tab.

---

## Next Steps

1. **Customize Queries**: Add more search queries to the "Query" sheet
2. **Enable Contact Extraction**: Add Firecrawl API key to `.env`
3. **Adjust Schedule**: Modify the Schedule Trigger interval in n8n
4. **Export Data**: Use Google Sheets export features for analysis

---

## Support

If you encounter any problems:

1. Run diagnostic: `python3 scripts/diagnostic.py`
2. Check n8n logs in the terminal
3. Consult n8n documentation: https://docs.n8n.io

---


