# Gas Station Analyzer Workflow

## Overview
Automated workflow that scrapes gas station data from Google Maps and calculates a Decision Score to help drivers choose the best station.

## Workflow Phases

### 1. Data Collection Phase
- **Trigger**: Schedule (daily at 8 AM) or manual
- **Input**: Google Sheets with pending queries
- **Process**: Reads location queries and triggers Apify scraper

### 2. Scraping & Validation Phase
- **API**: Apify Google Maps scraper
- **Wait Time**: Polls every 30 seconds until job completes
- **Validation**: Checks job status (SUCCEEDED/FAILED)

### 3. Transformation Phase
- **Input**: Raw Apify data (JSON)
- **Process**: Extracts and structures station data
- **Output**: Normalized station records with base Decision Score

### 4. Storage Phase
- **Destination**: Google Sheets "Data" tab
- **Method**: Append rows
- **Authentication**: OAuth2

## Decision Score Formula

```javascript
Decision Score = (Rating × 8) + (Reviews Score × 3) + (24hrs × 30)

Where:
- Rating Score = (rating / 5) × 40 points (max 40)
- Reviews Score = min(log(reviews + 1) × 10, 30) (max 30)
- 24hrs Score = 30 points if open 24hrs, else 0
```

## Data Fields

| Field | Type | Description |
|-------|------|-------------|
| Station_ID | String | Google Maps Place ID |
| Station_Name | String | Business name |
| Address | String | Full address |
| Latitude | Number | GPS latitude |
| Longitude | Number | GPS longitude |
| Rating_Average | Number | Google rating (0-5) |
| Total_Reviews | Number | Review count |
| Open_24_Hours | Boolean | 24hr availability |
| Google_Maps_URL | String | Direct link to place |
| Decision_Score | Number | Calculated score (0-100) |

## Error Handling

- **Error Trigger**: Captures all workflow errors
- **Notification**: Sends email/webhook on failure
- **Retry Logic**: Apify job retries automatically

## Usage

### Manual Execution
1. Open workflow in n8n
2. Click "Execute Workflow"
3. Monitor execution in real-time
4. Check Google Sheets for results

### Scheduled Execution
- Runs daily at 8:00 AM
- Processes all pending queries
- Updates Google Sheets automatically

## Maintenance

### Update Queries
Add new searches to Google Sheets "Queries" tab:
- Column A: Query (e.g., "gas stations")
- Column B: Location (e.g., "Queretaro, Mexico")
- Column C: Status (FALSE = pending)

### Monitor Costs
- Apify: ~$0.50 per 1000 places scraped
- Google Sheets API: Free
- n8n: Self-hosted (free)

## Version History

- v1.0 (2026-01-21): Initial workflow with basic Decision Score
- v1.1 (planned): Add amenities enrichment with Google Places API

## Author
Daniel SH - Portfolio Project for Upwork/Fiverr

## License
MIT
