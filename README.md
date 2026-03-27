# 🚗 FleetOps AI: Automated Fuel Cost Optimizer

> **Business Problem**: Small fleet managers waste \$1000s/month because drivers choose gas stations blindly, often paying premium prices for poor service.
> **Solution**: An autonomous AI agent that scouts 100+ stations daily to identify the **top 3 highest ROI stations** based on price, quality, and driver convenience.

![Banner](https://img.shields.io/badge/Status-Production%20Ready-success)
![Stack](https://img.shields.io/badge/Stack-n8n%20|%20Python%20|%20Apify%20|%20Google%20Sheets-blue)

## 💡 The Value Proposition
This isn't just a scraper; it's a decision-support system for logistics.

| Metric | Before AI | With FleetOps AI |
| :--- | :--- | :--- |
| **Decision Time** | 15 mins/day (Manual search) | **0 mins/day (Automated)** |
| **Station Quality** | Random (Risk of bad fuel) | **Verified (>4.2 Stars)** |
| **Cost Efficiency** | Unknown | **Optimized (Price vs Quality)** |
| **Driver Access** | Guesswork | **24/7 Confirmed** |

---

## 🏗️ Architecture (The "Wrapper" Model)
We wrap complex data sources into a simple, actionable dashboard for the end-user.

```mermaid
graph LR
    A[Google Maps\n(Raw Data)] -->|Apify Scraper| B(Python AI Agent)
    B -->|Clean & Validate| C{Decision Engine}
    C -->|Calculate ROI Score| D[Google Sheets Dashboard]
    D -->|Daily Email| E[Fleet Manager]
    
    style B fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
```

### The "Secret Sauce": Decision Score v1.0
We don't just dump data. We crunch it into a single **0-100 Score**:
- **50% Quality (Rating)**: Avoids vehicle damage from bad fuel.
- **30% Reliability (Reviews)**: Filters out fake/new listings.
- **20% Access (24/7)**: Critical for night shifts.

---

## 🛠️ How It Works (Under the Hood)
1.  **Extract**: `Apify` acts as the sensory array, scanning a 5km radius.
2.  **Process**: `Python` scripts (Pydantic models) strictly validate every data point.
3.  **Rank**: Our custom algorithm sorts stations by `Decision_Score`.
4.  **Deliver**: The system pushes a "Top 3 Recommendation" table to Google Sheets.

## 🚀 Setup & Deployment
This project is built to run on standard, low-cost infrastructure.

### Prerequisites
- Docker (for n8n)
- Python 3.9+
- Apify Account (Free tier works)
- Google Cloud Account (for Sheets API)

### Quick Start
1.  **Clone & Configure**:
    ```bash
    git clone https://github.com/yourusername/fleet-ops-ai.git
    cd fleet-ops-ai
    cp .env.example .env
    # Add your APIFY_API_KEY and Google Credentials
    ```

2.  **Deploy Workflow**:
    ```bash
    # We use a custom script to hot-deploy to n8n
    python3 scripts/deploy_workflow.py
    ```

3.  **Run**:
    - Open your n8n dashboard (`localhost:5678`).
    - Activate the "Daily Schedule" trigger.
    - Sit back and watch the Google Sheet populate.

## 📊 Dashboard Preview
*(Insert screenshot of your Google Sheet here)*
- **Column A**: Rank (🏆 #1, ✅ #2, ⚠️ #3)
- **Column B**: Station Name
- **Column I**: **Decision Score** (The magic number)
- **Column J**: Estimated Savings (vs Market Avg)

---

## 🔮 Future Roadmap (v2.0)
- [ ] **Waze Integration**: Check real-time traffic to station.
- [ ] **Slack Bot**: specific `/gas` command for drivers.
- [ ] **Predictive Pricing**: Buy before the weekend hike.

---
**License**: MIT | Built for the automated economy.
