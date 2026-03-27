from typing import List, Dict, Any
from .models import GasStation
from .parser import parse_apify_data
from .scorer import calculate_decision_score
from dotenv import load_dotenv

def process_stations_batch(raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # No external API keys needed for this simplified version
    load_dotenv()
    
    stations: List[GasStation] = []
    
    for item in raw_items:
        try:
            # Parse base data (Apify)
            station = parse_apify_data(item)
            
            # Note: We are no longer enriching with Google Places API to keep it lightweight.
            # Amenities will default to False unless found in raw_data (future improvement).
                
            # Calculate Score
            station.Decision_Score = calculate_decision_score(station)
            stations.append(station)
        except Exception:
            # Silently skip bad records
            continue
    # Market context for savings
    priced_stations = [s for s in stations if s.Precio_Litro is not None]
    max_price = max((s.Precio_Litro for s in priced_stations), default=0.0)

    # Sort & Decorate
    stations.sort(key=lambda s: s.Decision_Score or 0, reverse=True)
    
    enriched = []
    for rank, s in enumerate(stations, 1):
        s.Ranking = rank
        if s.Precio_Litro and max_price > 0:
            s.Ahorro_Por_Litro = max_price - s.Precio_Litro
            s.Ahorro_Tanque_50L = s.Ahorro_Por_Litro * 50
            s.Ahorro_Mensual = s.Ahorro_Tanque_50L * 4
        else:
            s.Ahorro_Por_Litro = s.Ahorro_Tanque_50L = s.Ahorro_Mensual = 0.0

        if rank == 1:
            s.Recomendacion = "🏆 MEJOR OPCIÓN"
        elif s.Decision_Score >= 80:
            s.Recomendacion = "✅ Recomendado"
        elif s.Decision_Score >= 50:
            s.Recomendacion = "⚠️ Opción Regular"
        else:
            s.Recomendacion = "❌ Evitar"
            
        enriched.append(s.model_dump())

    return enriched

if __name__ == "__main__":
    import json
    import sys

    try:
        data = sys.stdin.read()
        items = json.loads(data) if data else []
        if isinstance(items, dict): items = [items]
        print(json.dumps(process_stations_batch(items)))
    except Exception as e:
        print(json.dumps([{"error": str(e)}]))
