from src.processor import process_stations_batch
import json

def test_proactive_logic():
    # Mock some data for a gas station in Mexico City (for example)
    # 19.4326, -99.1332 (Center)
    mock_raw_data = [
        {
            "placeId": "test_station_1",
            "title": "Gasolinera Test Proactiva",
            "totalScore": 4.5,
            "reviewsCount": 100,
            "location": {"lat": 19.4326, "lng": -99.1332},
            "address": "Av. Reforma, CDMX",
            "url": "https://maps.google.com/?cid=123"
        }
    ]

    print("🧪 Probando procesamiento proactivo (incluyendo búsqueda de amenidades)...")
    results = process_stations_batch(mock_raw_data)
    
    print("\n📊 Resultados del Script:")
    print(json.dumps(results, indent=2))
    
    # Check if amenities were added
    station = results[0]
    if "Nearby_OXXO" in station:
        print("\n✅ El sistema ahora busca amenidades automáticamente.")
        print(f"   Score Final: {station['Decision_Score']}")
    else:
        print("\n❌ No se detectaron campos de amenidades. Revisa la lógica.")

if __name__ == "__main__":
    test_proactive_logic()
