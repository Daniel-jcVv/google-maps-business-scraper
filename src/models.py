from pydantic import BaseModel, Field
from typing import Optional

class GasStation(BaseModel):
    # Match Google Sheets Headers exactly for auto-mapping
    Station_ID: str = Field(..., description="Unique ID of the station")
    Station_Name: str = Field(..., description="Name of the gas station")
    Has_24_Hours: bool = Field(..., description="Whether the station is open 24/7")
    total_reviews: int = Field(..., ge=0, description="Total number of reviews") # used in calculation
    rating: float = Field(..., ge=0, le=5, description="Google Maps rating (0-5)") # used in calculation
    amenities_count: int = Field(..., ge=0, description="Count of nearby amenities") # used in calculation
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None
    Precio_Litro: Optional[float] = Field(None, description="Price per liter")
    
    # Amenities breakdown
    Nearby_OXXO: bool = False
    Nearby_Coffee: bool = False
    Nearby_Mechanic: bool = False
    Nearby_ATM: bool = False
    
    # Dashboard calculated fields (Matching Sheets Headers)
    Ranking: Optional[int] = None
    Decision_Score: Optional[int] = None
    Ahorro_Por_Litro: Optional[float] = None
    Ahorro_Tanque_50L: Optional[float] = None
    Ahorro_Mensual: Optional[float] = None
    Recomendacion: Optional[str] = None

    # Extra info that might be useful
    address: Optional[str] = None
    Google_Maps_URL: Optional[str] = None
