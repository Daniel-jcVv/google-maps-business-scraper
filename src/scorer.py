import math
from .models import GasStation

# Scoring Constraints
# Scoring Constraints - Rebalanced for Fleet Efficiency
MAX_RATING_SCORE = 50       # Quality is king (50%)
MAX_REVIEWS_SCORE = 30      # Popularity/Reliability (30%)
MAX_AVAILABILITY_SCORE = 20 # 24/7 Access (20%)

def calculate_decision_score(station: GasStation) -> int:
    """
    Calculate the decision score (0-100).
    Optimized for fleets: Quality + Reliability + Access.
    """
    # 1. Rating Score (50%)
    rating_score = (station.rating / 5) * MAX_RATING_SCORE

    # 2. Reviews Score (30%)
    reviews_score = min(math.log10(station.total_reviews + 1) * 10, MAX_REVIEWS_SCORE)

    # 3. Availability Score (20%)
    availability_score = MAX_AVAILABILITY_SCORE if station.Has_24_Hours else 0
    
    # 4. Amenities Score (Deprecated in v1.0 MVP)
    # amenities_score = min(station.amenities_count * 5, MAX_AMENITIES_SCORE)

    return round(rating_score + reviews_score + availability_score)
