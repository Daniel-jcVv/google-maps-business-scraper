# Sheet Details - Estructura y Headers

## Headers necesarios (Fila 1):
```
Station_ID | Station_Name | Has_24_Hours | Has_ATM | Has_CarWash | Has_Store | Price_Level | Website | Phone
```

## Descripción de campos:

- **Station_ID**: ID único de Google Places
- **Station_Name**: Nombre de la gasolinera
- **Has_24_Hours**: TRUE/FALSE - Abierto 24 horas
- **Has_ATM**: TRUE/FALSE - Tiene cajero automático
- **Has_CarWash**: TRUE/FALSE - Tiene lavado de autos
- **Has_Store**: TRUE/FALSE - Tiene tienda de conveniencia
- **Price_Level**: 1-4 (1=Económico, 4=Premium)
- **Website**: URL del sitio web
- **Phone**: Teléfono de contacto

## Formato de datos:

| Station_ID | Station_Name | Has_24_Hours | Has_ATM | Has_CarWash | Has_Store | Price_Level | Website | Phone |
|---|---|---|---|---|---|---|---|---|
| ChIJ... | Pemex Centro | TRUE | TRUE | FALSE | TRUE | 2 | www.pemex.com | +52... |

## Actualizar Sheet Data con campos de ahorro:

Agregar estos headers al sheet "Data":
```
Ranking | Precio_Litro | Ahorro_Por_Litro | Ahorro_Tanque_50L | Ahorro_Mensual | Recomendacion
```

## Dashboard - Visualización recomendada:

### 1. Tabla principal (ordenada por Decision_Score):
- Ranking
- Station_Name
- Decision_Score
- Precio_Litro (MXN)
- Ahorro_Tanque_50L
- Ahorro_Mensual
- Recomendacion

### 2. Tarjetas de resumen:
- **Mejor Opción**: Gasolinera #1
- **Ahorro Máximo/Tanque**: $XX.XX MXN
- **Ahorro Mensual Estimado**: $XXX.XX MXN

### 3. Gráfica de comparación:
- Eje X: Gasolineras
- Eje Y: Precio por litro
- Color: Verde (económica), Amarillo (media), Rojo (cara)

### 4. Mapa de amenidades (tabla):
- Columnas: Has_24_Hours, Has_ATM, Has_CarWash, Has_Store
- Íconos: ✓ (disponible), ✗ (no disponible)

## Fórmulas para cálculo manual en Sheets:

```
Ahorro_Por_Litro = MAX(Precio_Litro) - Precio_Litro
Ahorro_Tanque_50L = Ahorro_Por_Litro * 50
Ahorro_Mensual = Ahorro_Tanque_50L * 4
```

## Importar workflow actualizado:

1. Ir a n8n: http://localhost:5678
2. Workflows > Import from File
3. Seleccionar: workflows/gas_station_analyzer.json
4. Activar el workflow
