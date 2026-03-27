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
│   ├── populate_details.py # Apify JSON → Details sheet en XLSX
│   ├── scrape_all_details.py # Scrape amenities por placeId via Apify
│   ├── test_apify_details.py # Test scrape de 3 estaciones
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
- **Data**: 75 filas, 10 columnas (33 IDs unicos, hay duplicados)
- **Details**: 33 filas con amenities POBLADAS (sesion 2026-03-27)
  - 24h: 25 (76%), Store: 11 (33%), CarWash: 3 (9%), OXXO: 3 (9%)
  - ATM: 0, Coffee: 0 (Google Maps no reporta estos para gasolineras MX)

### Sheets cleanup (sesion 2026-03-27)
- CSVs eliminados (Data, Details, Query) — eran subconjuntos viejos
- apify_sample.json y apify_full_details.json eliminados — ya procesados
- Solo quedan: XLSX principal + fiverr_sample.xlsx

### Sesion 2026-03-27 (segunda parte)

- Claude Code settings configurados: `.claude/settings.json` con hooks y ignorePatterns
- Carpetas obsoletas eliminadas: `.context/`, `.agent/`
- Brainstorming Fiverr: gig "scrape any website", 3 paquetes (Basic $10 / Standard $25 / Premium $50)
- Estrategia screenshots: 3 datasets (refacciones MercadoLibre + gasolineras Maps + vista general)
- MercadoLibre validado: BeautifulSoup funciona, gratis, 48+ productos por búsqueda
- Comparación por región NO funciona (ML es marketplace nacional) → comparación por MARCA sí
- Decisión: crear proyecto separado `mercadolibre_scraper/` (herramientas diferentes a maps_scraper)
- Apify: $4.78 crédito restante este mes

### Produccion
- Necesita: Apify API key + Google Sheets OAuth + Sheet ID
- Datos scrapeados 2026-03-27 con details via startUrls (por placeId)

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

- [x] Poblar hoja Details (amenities via Apify startUrls) — DONE sesion 2026-03-27
- [x] Sincronizar CSV con XLSX — DONE (CSVs eliminados, XLSX es fuente unica)
- [x] Commit sesion 2026-03-27 — DONE
- [x] Claude Code settings: hooks (.env protection, auto-test) + ignorePatterns — DONE sesion 2026-03-27
- [x] Cleanup carpetas obsoletas (.context/, .agent/) — DONE sesion 2026-03-27
- [ ] Estudio de mercado: qué scraping se vende más en Fiverr (próxima sesión)
- [ ] Crear proyecto `mercadolibre_scraper/` — scraper de refacciones por marca (BeautifulSoup, gratis)
- [ ] Formatear XLSX para Fiverr — 3 screenshots: refacciones ML + gasolineras Maps + vista general
- [ ] Screenshots alta resolución para Fiverr (3 tomas)
- [ ] Publicar gig Fiverr: "scrape any website and deliver clean data"
- [ ] Migrar a uv (baja prioridad)

---

## Reglas

- NUNCA ejecutar git, dar comandos listos para copiar
- Modo socratico por default (usuario escribe, IA guia)
- Si el usuario no se siente bien, escribir codigo directo
