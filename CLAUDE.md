# CLAUDE.md - Maps Scraper (FleetOps AI)

## Proposito

Scraper de Google Maps que extrae gasolineras, las puntua (Decision Score 0-100) y genera recomendaciones. Pipeline: Apify > Python (Pydantic + Scorer) > n8n > Google Sheets.

---

## Estructura

```
maps_scraper/
├── src/                    # Core logic
│   ├── models.py           # GasStation Pydantic model
│   ├── scorer.py           # Decision Score (rating 50% + reviews 30% + 24h 20%)
│   ├── parser.py           # Apify JSON > GasStation
│   └── processor.py        # Batch: score + rank + savings + recomendacion
├── scripts/
│   ├── format_sheet.py     # Formatea XLSX para screenshots
│   ├── deploy_workflow.py  # Deploy JSON a n8n API
│   ├── sync_workflow.py    # Download workflow de n8n
│   ├── verify_scoring.py   # Test scorer con samples
│   └── test_proactive_logic.py
├── sheets/                 # Data local
│   ├── Google Maps Scraper - local.xlsx  # 563 registros (Data), Details vacia
│   ├── fiverr_sample.xlsx  # Formateado para gig Fiverr
│   └── *.csv               # Backups (Data=75 filas, Details=vacio)
├── tools/                  # Diagnostico
│   ├── diagnostic.py       # Health check (n8n, Apify, Sheets)
│   ├── test_workflow.py    # Abrir n8n en browser
│   └── clear_sheets.py     # Limpiar Google Sheets
├── workflows/
│   └── gas_station_analyzer.json  # n8n workflow (schedule 30 min)
├── tests/
│   └── test_logic.py       # Unit tests (scorer, parser, batch)
├── docs/
│   ├── screenshots/        # Screenshots para Fiverr
│   └── *.md                # Setup guides
├── docker-compose.yml      # n8n + PostgreSQL
├── Dockerfile
└── requirements.txt        # pydantic, pytest, openpyxl, requests, dotenv
```

---

## Data Flow

```
Google Sheets (Query) > n8n (30 min) > Apify (scrape Maps) > Python (parse+score+rank) > Google Sheets (Data)
```

---

## Estado actual

### XLSX (Google Maps Scraper - local.xlsx)
- **Query**: 1 fila (gas stations, Queretaro Mexico)
- **Data**: 563 filas, 10 columnas con datos reales
- **Details**: Solo headers, sin datos (amenities no implementado)

### CSVs
- Data.csv = 75 filas (subconjunto viejo del XLSX)
- Details.csv = solo headers
- Query.csv = 1 fila

### Produccion
- Necesita: Apify API key + Google Sheets OAuth + Sheet ID
- Datos tienen ~2 meses (enero 2026)

---

## Decision Score Formula

```
Score = (rating/5 * 50) + min(log10(reviews+1) * 10, 30) + (24h ? 20 : 0)
```

| Componente | Peso | Max |
|------------|------|-----|
| Rating | 50% | 50 pts |
| Reviews | 30% | 30 pts |
| 24 horas | 20% | 20 pts |

---

## Pendientes

- [ ] Poblar hoja Details (amenities: ATM, car wash, tienda, cafe)
- [ ] Sincronizar CSV con XLSX (75 vs 563 filas)
- [ ] Migrar a uv (actualmente pip + venv)
- [ ] Screenshots alta resolucion para Fiverr (3 tomas)

---

## Reglas

- NUNCA ejecutar git, dar comandos listos para copiar
- Modo socratico por default (usuario escribe, IA guia)
- Si el usuario no se siente bien, escribir codigo directo
