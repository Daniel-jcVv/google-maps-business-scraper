from typing import Dict, Any
from .models import GasStation, Restaurant


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

    # Extract amenities from additionalInfo
    additional_info = raw_data.get('additionalInfo', {})
    if not isinstance(additional_info, dict):
        additional_info = {}
    amenities = extract_amenities(additional_info, name)

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
        Nearby_ATM=amenities["has_atm"],
        Nearby_Coffee=amenities["has_coffee"],
        Nearby_Mechanic=False,
        Nearby_OXXO=amenities["has_oxxo"],
        Has_CarWash=amenities["has_car_wash"],
        Has_Store=amenities["has_store"],
        address=raw_data.get('address', 'N/A'),
        Google_Maps_URL=raw_data.get('url', '')
    )


def extract_amenities(additional_info: dict, station_name: str) -> dict:
    """Extract amenity booleans from Apify additionalInfo field."""

    # Paso 1: juntar TODOS los nombres de servicios en un solo texto
    # Ejemplo: "Air pump Restroom Convenience store Diesel gas Credit cards"
    # Asi despues buscamos keywords con "in" de forma simple
    all_services = ""
    for category in additional_info.values():   # recorre ["Amenities", "Offerings", ...]
        for item in category:                   # cada item es {"Air pump": True}
            for key in item:                    # key = "Air pump" (el nombre)
                all_services += key + " "

    # Paso 2: convertir a minusculas para que la busqueda no falle por mayusculas
    all_services = all_services.lower()
    name_lower = station_name.lower()

    # Paso 3: buscar cada amenity por keyword
    return {
        "has_atm": "atm" in all_services,
        "has_car_wash": "car wash" in all_services,
        "has_store": "convenience store" in all_services or "tienda" in all_services,
        "has_oxxo": "oxxo" in name_lower,          # oxxo esta en el nombre, no en amenities
        "has_coffee": "coffee" in all_services or "café" in all_services,
    }


def extract_restaurant_amenities(additional_info: dict) -> dict:
    """Extract amenity booleans for restaurants from Apify additionalInfo"""

    all_services = ""
    for category in additional_info.values():
        for item in category:
            for key in item:
                all_services += key + " "

    all_services = all_services.lower()

    return {
        "has_delivery": "delivery" in all_services,
        "has_dine_in": "dine-in" in all_services or "dine in" in all_services,
        "has_takeout": "takeout" in all_services or "take-out" in all_services,
        "has_wifi": "wifi" in all_services or "wifi" in all_services,
        "has_reservations": "reserv" in all_services,
    }


def parse_restaurant_data(raw_data: dict) -> Restaurant:
    """Parse raw JSON from Apify/Google Maps into a Restaurant model."""

    place_id = raw_data.get("placeId", raw_data.get("cid", "unknown"))
    name = raw_data.get("title", "Unknown")

    rating = float(raw_data.get("totalScore", 0))
    reviews = int(raw_data.get("reviewsCount", 0))

    location = raw_data.get("location", {})
    lat = location.get("lat", raw_data.get("lat"))
    lng = location.get("lng", raw_data.get("lng"))

    has_24_hours = False
    opening_hours = raw_data.get("openingHours", [])
    if opening_hours:
        for dh in opening_hours:
            if "open 24 hours" in str(dh).lower():
                has_24_hours = True
                break

    additional_info = raw_data.get("additionalInfo", {})
    if not isinstance(additional_info, dict):
        additional_info = {}
    amenities = extract_restaurant_amenities(additional_info)

    return Restaurant(
        place_id=place_id,
        name=name,
        address=raw_data.get("address", "N/A"),
        phone=raw_data.get("phone"),
        website=raw_data.get("website"),
        rating=rating,
        total_reviews=reviews,
        price_level=raw_data.get("priceLevel"),
        has_24_hours=has_24_hours,
        has_delivery=amenities["has_delivery"],
        has_dine_in=amenities["has_dine_in"],
        has_takeout=amenities["has_takeout"],
        has_wifi=amenities["has_wifi"],
        has_reservation=amenities["has_reservations"],
        latitude=lat,
        longitude=lng,
        google_maps_url=raw_data.get("url", ""),
    )
