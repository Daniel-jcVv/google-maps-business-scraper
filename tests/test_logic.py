import pytest
from src.models import GasStation
from src.scorer import calculate_decision_score
from src.parser import parse_apify_data
from src.processor import process_stations_batch

# --- Tests for Scorer ---
def test_perfect_station():
    """A perfect station should maximize scores."""
    station = GasStation(
        Station_ID="1",
        Station_Name="Perfect Fuel",
        rating=5.0,
        total_reviews=1000, 
        Has_24_Hours=True, 
        amenities_count=4,  
        Precio_Litro=20.0
    )
    score = calculate_decision_score(station)
    assert score == 100 

def test_worst_station():
    """Worst station gets 0."""
    station = GasStation(
        Station_ID="0", Station_Name="Bad Fuel", rating=0, total_reviews=0, Has_24_Hours=False, amenities_count=0
    )
    assert calculate_decision_score(station) == 0

def test_validation_works():
    """Pydantic raises ValidationError on invalid inputs."""
    with pytest.raises(Exception): 
        GasStation(Station_ID="x", Station_Name="x", rating=6.0, total_reviews=10, Has_24_Hours=True, amenities_count=0)

# --- Tests for Processor (End-to-End Logic) ---
def test_process_batch_savings():
    """Verify savings calculation based on max price in batch."""
    raw_data = [
        {"placeId": "A", "title": "Expensive", "totalScore": 5, "reviewsCount": 100, "price": 25.0, "openingHours": [{"hours": "open 24 hours"}]},
        {"placeId": "B", "title": "Cheap", "totalScore": 3, "reviewsCount": 10, "price": 20.0, "openingHours": []},
    ]
    
    results = process_stations_batch(raw_data)
    
    assert len(results) == 2
    a = next(r for r in results if r['Station_ID'] == "A")
    b = next(r for r in results if r['Station_ID'] == "B")
    
    assert a['Ahorro_Por_Litro'] == 0.0
    assert b['Ahorro_Por_Litro'] == 5.0
    assert b['Ahorro_Tanque_50L'] == 250.0 
    
    # Check Recommendations
    assert "🏆" in a['Recomendacion'] 
    assert "⚠️" in b['Recomendacion'] or "❌" in b['Recomendacion']
