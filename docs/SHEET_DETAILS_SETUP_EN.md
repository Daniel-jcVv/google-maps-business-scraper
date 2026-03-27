# Sheet Details - Structure and Headers

## Required Headers (Row 1):
```
Station_ID | Station_Name | Has_24_Hours | Has_ATM | Has_CarWash | Has_Store | Price_Level | Website | Phone
```

## Field Descriptions:

- **Station_ID**: Unique Google Places ID
- **Station_Name**: Gas station name
- **Has_24_Hours**: TRUE/FALSE - Open 24 hours
- **Has_ATM**: TRUE/FALSE - Has ATM
- **Has_CarWash**: TRUE/FALSE - Has car wash
- **Has_Store**: TRUE/FALSE - Has convenience store
- **Price_Level**: 1-4 (1=Economy, 4=Premium)
- **Website**: Website URL
- **Phone**: Contact phone

## Data Sheet - Add Savings Columns:

Add these headers to "Data" sheet:
```
Ranking | Price_Per_Liter | Savings_Per_Liter | Savings_Per_Tank_50L | Monthly_Savings | Recommendation
```

## Dashboard Visualization:

### 1. Main Table (sorted by Decision_Score):
- Ranking
- Station_Name
- Decision_Score
- Price_Per_Liter (MXN)
- Savings_Per_Tank_50L
- Monthly_Savings
- Recommendation

### 2. Summary Cards:
- **Best Option**: Station #1
- **Max Savings/Tank**: $XX.XX MXN
- **Estimated Monthly Savings**: $XXX.XX MXN

### 3. Price Comparison Chart:
- X-axis: Gas Stations
- Y-axis: Price per liter
- Color: Green (cheap), Yellow (mid), Red (expensive)

### 4. Amenities Map (table):
- Columns: Has_24_Hours, Has_ATM, Has_CarWash, Has_Store
- Icons: ✓ (available), ✗ (not available)

## Calculation Formulas:

```javascript
Savings_Per_Liter = MAX(Price_Per_Liter) - Price_Per_Liter
Savings_Per_Tank_50L = Savings_Per_Liter * 50
Monthly_Savings = Savings_Per_Tank_50L * 4
```

## Import Updated Workflow:

1. Go to n8n: http://localhost:5678
2. Workflows > Import from File
3. Select: workflows/gas_station_analyzer.json
4. Activate workflow
