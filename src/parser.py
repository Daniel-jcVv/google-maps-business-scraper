from typing import Dict, Any
from .models import GasStation

def parse_apify_data(raw_data: Dict[str, Any]) -> GasStation:
    """
    Parse raw JSON from Apify/Google Maps into a validated GasStation model.
    """
    # Extract basic info
    station_id = raw_data.get('placeId', raw_data.get('cid', 'unknown'))
    name = raw_data.get('title', 'Unknown Station')
    
    # Rating & Reviews
    rating = float(raw_data.get('totalScore', 0))
    reviews = int(raw_data.get('reviewsCount', 0))
    
    # Location
    location = raw_data.get('location', {})
    lat = location.get('lat', raw_data.get('lat'))
    lng = location.get('lng', raw_data.get('lng'))
    
    # Open 24 Hours?
    has_24_hours = False
    opening_hours = raw_data.get('openingHours', [])
    if opening_hours:
        for dh in opening_hours:
            if 'open 24 hours' in str(dh).lower():
                has_24_hours = True
                break
    
    # If not found in openingHours, check additionalInfo
    if not has_24_hours:
        additional_info = raw_data.get('additionalInfo', {})
        if isinstance(additional_info, dict):
            for key, val in additional_info.items():
                if '24' in str(val).lower() or '24' in str(key).lower():
                    has_24_hours = True
        elif isinstance(additional_info, list):
            for item in additional_info:
                if '24' in str(item).lower():
                    has_24_hours = True

    # Amenities & Price
    amenities_count = raw_data.get('amenities_count', 0)
    # Map 'price' or 'priceLevel' to a numeric value for savings logic
    # Maps priceLevel is 1-4. We can mock a price if needed, or use raw price if exists.
    precio = raw_data.get('price', raw_data.get('priceLevel', None))
    if isinstance(precio, (int, float)):
        # priceLevel 1 -> ~21, 2 -> ~22, etc (Mocking for dashboard impact)
        if precio < 10: # likely priceLevel
            precio = 20.0 + precio
    else:
        precio = None

    return GasStation(
        Station_ID=station_id,
        Station_Name=name,
        Has_24_Hours=has_24_hours,
        total_reviews=reviews,
        rating=rating,
        amenities_count=amenities_count,
        Latitude=lat,
        Longitude=lng,
        Precio_Litro=precio,
        address=raw_data.get('address', 'N/A'),
        Google_Maps_URL=raw_data.get('url', '')
    )
