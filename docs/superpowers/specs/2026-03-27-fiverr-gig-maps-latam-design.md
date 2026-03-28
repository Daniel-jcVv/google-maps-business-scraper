# Spec: Fiverr Gig — Google Maps Restaurant Data LATAM

## Contexto

El usuario necesita ingresos en 0-30 dias. Tiene un pipeline funcional de scraping de Google Maps (Apify > Python > XLSX) que actualmente scrapea gasolineras en Queretaro. El objetivo es adaptar este pipeline para restaurantes y publicar un gig en Fiverr especializado en datos de Google Maps para Mexico/LATAM.

## Estudio de mercado (hallazgos clave)

- ~7,000 gigs de scraping en Fiverr, saturado en rango $5-$30
- Google Maps leads es el nicho mas demandado pero muy competido
- Diferenciador viable: especializacion en LATAM (pocos sellers lo ofrecen)
- Restaurantes tiene la demanda mas alta entre tipos de negocio
- Top sellers se diferencian por: especializacion vertical, muestras reales, formatos multiples

## Posicionamiento

- **Nicho:** Google Maps restaurant data en Mexico y LATAM
- **Diferenciador:** Especialista LATAM (la mayoria de sellers solo cubren USA/Europa)
- **Idioma del gig:** Ingles (mercado global de Fiverr)

## Titulo del gig

"I will scrape Google Maps restaurant data in Mexico and Latin America"

## Paquetes

| | Basic $15 | Standard $30 | Premium $50 |
|--|-----------|-------------|-------------|
| Records | 100 | 500 | 1,000+ |
| Campos | Nombre, direccion, telefono, rating | + reviews, horarios, website | + amenities, fotos URL, coordenadas |
| Ciudades | 1 | Hasta 3 | Hasta 5 |
| Formato | XLSX | XLSX + CSV | XLSX + CSV + JSON |
| Entrega | 2 dias | 3 dias | 5 dias |

## Descripcion del gig

> Need restaurant data from Google Maps in Mexico or Latin America? I'll scrape and deliver clean, organized data including name, address, phone, ratings, reviews, hours, and amenities. Perfect for market research, competitor analysis, or lead generation. Data delivered in XLSX, CSV, or JSON format.

## Screenshots necesarios (3)

1. **XLSX formateado** — tabla de restaurantes con colores, filtros, datos limpios
2. **Vista de datos** — zoom en columnas clave (nombre, rating, telefono, horario)
3. **Grafico/resumen** — distribucion de ratings, % con telefono, top 10

## Cambios tecnicos al pipeline

### 1. Query configurable

Actualmente la query esta hardcodeada a "gas stations Queretaro Mexico". Necesita ser configurable para aceptar cualquier tipo de negocio y ciudad.

- **Archivo:** `sheets/Google Maps Scraper - local.xlsx` (hoja Query)
- **Cambio:** Parametrizar la query en scripts para que lean tipo de negocio + ciudad como argumentos

### 2. Amenities de restaurantes

El parser actual extrae amenities de gasolineras (ATM, CarWash, Store, OXXO, Coffee). Para restaurantes los amenities son diferentes.

- **Archivo:** `src/parser.py` (funcion `extract_amenities`)
- **Cambio:** Detectar tipo de negocio y extraer amenities relevantes:
  - Restaurantes: WiFi, Delivery, Dine-in, Takeout, Reservations, Wheelchair accessible (verificar contra datos reales de Apify, ajustar segun lo que devuelva)
  - Gasolineras: ATM, CarWash, Store, OXXO, Coffee (mantener)

### 3. Script de formato Fiverr

Crear script que tome el XLSX con datos crudos y genere una version formateada profesionalmente para screenshots.

- **Archivo nuevo:** `scripts/format_fiverr_sample.py`
- **Funcionalidad:**
  - Header con colores corporativos
  - Columnas con ancho auto-ajustado
  - Filtros activados
  - Rating con formato condicional (verde > 4.0, amarillo 3.0-4.0, rojo < 3.0)
  - Hoja resumen con estadisticas (total, promedio rating, % con telefono, top 10)

### 4. Sample de restaurantes

Correr un scrape real de restaurantes en Queretaro via Apify (~$0.50 de credito).

- Usar `scripts/scrape_all_details.py` adaptado con query "restaurants Queretaro Mexico"
- Procesar con pipeline existente (parser > processor > populate_details)
- Generar XLSX formateado con `format_fiverr_sample.py`

## Flujo de trabajo para clientes (post-publicacion)

```
Cliente pide: "500 restaurantes en CDMX"
  > Configurar query en Apify (ciudad + tipo)
  > Correr scrape (~$1-2 de Apify)
  > Procesar con pipeline Python
  > Formatear XLSX
  > Entregar al cliente
```

## Costo por orden

- Apify: ~$0.50-$2.00 por scrape (dependiendo de volumen)
- Tiempo: ~30 min por orden (mayoria automatizado)
- Margen: $13-$48 por orden despues de costos Apify

## Criterios de exito

1. XLSX sample de restaurantes generado con datos reales
2. 3 screenshots de alta calidad listos para Fiverr
3. Gig publicado con titulo, descripcion, paquetes y screenshots
4. Pipeline adaptado para aceptar cualquier query (no solo gasolineras)

## Fuera de alcance

- MercadoLibre scraper (proyecto separado, proxima sesion)
- Automatizacion de ordenes (despues de primeras 5 reviews)
- Dashboard o frontend (no necesario para MVP)
