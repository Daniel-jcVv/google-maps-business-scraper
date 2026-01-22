# Changelog - Gas Station Analyzer

All notable changes to this workflow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Add Google Places API integration for nearby amenities
- Implement amenities scoring (OXXO, cafes, mechanics, ATMs)
- Update Decision Score formula to include amenities (20% weight)

## [1.0.0] - 2026-01-21

### Added
- Initial workflow implementation
- Apify Google Maps scraper integration
- Base Decision Score calculation (Rating + Reviews + 24hrs)
- Google Sheets integration for data storage
- Error handling with notifications
- Sticky notes for workflow organization
- Comprehensive node documentation

### Features
- Automated daily scraping at 8 AM
- Processes up to 15 gas stations per query
- Calculates Decision Score (0-100 scale)
- Stores results in Google Sheets

### Technical Details
- n8n version: Latest
- Apify API: compass~crawler-google-places
- Google Sheets API: OAuth2 authentication
- Error handling: Email/Webhook notifications

## [0.1.0] - 2026-01-18

### Added
- Project structure setup
- Initial workflow draft
- Google Sheets template creation
- Apify account configuration

---

## Version Numbering

- **MAJOR**: Breaking changes to workflow structure
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, documentation updates
