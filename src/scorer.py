
import math

def calculate_decision_score(
    rating: float, 
    total_reviews: int, 
    open_24_hours: bool,
    amenities_count: int = 0
) -> int:
    """
    calculate the decision score for a gas station based on quality, popularity,
    availability, and amenities.
    
    This is the CORE business logic of the project. The formula is:
    Score = (Rating/5)*40 + min(log(reviews+1)*10, 30) + (24hrs ? 10 : 0) + min(amenities*5, 20)
    
    Weights (Top 100 points):
    - Rating (40%): Quality is most important
    - Reviews (30%): Popularity (logarithmic)
    - 24hrs (10%): Convenience
    - Amenities (20%): Extra services (OXXO, Coffee, etc.)

    Args:
        rating: Google Maps average rating (0.0-5.0)
        total_reviews: Number of reviews (must be >= 0)
        open_24_hours: True if station operates 24/7
        amenities_count: Number of nearby amenities (OXXO, Coffee, etc.)
        
    Returns:
        Integer score between 0-100
        
    Raises:
        ValueError: If inputs are invalid (negative numbers, rating > 5)
    """
    # validation fail with clear error messages (best practice)
    if not 0 <= rating <= 5:
        raise ValueError(f"Rating {rating} must be between 0 and 5")
    
    if total_reviews < 0:
        raise ValueError(f"Reviews {total_reviews} cannot be negative")
        
    if amenities_count < 0:
        raise ValueError(f"Amenities {amenities_count} cannot be negative")

    # Component 1: rating score (40 points max)
    rating_score = (rating/5)*40

    # Component 2: reviews score (30 points max, logarithmic)
    reviews_score = min(math.log10(total_reviews + 1) * 10, 30)

    # Component 3: availability score (10 points max)
    # Reduced from 30 to 10 to make room for amenities
    availability_score = 10 if open_24_hours else 0
    
    # Component 4: amenities score (20 points max)
    # 5 points per amenity, capped at 20 (4 amenities)
    amenities_score = min(amenities_count * 5, 20)

    # total sum all components and round to integer
    total_score = rating_score + reviews_score + availability_score + amenities_score
    return round(total_score)