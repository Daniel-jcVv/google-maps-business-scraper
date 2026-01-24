
import math

def calculate_decision_score(
    rating: float, 
    total_reviews: int, 
    open_24_hours: bool
) -> int:
    """
    calculate the decision score for a gas station based on quality, popularity,
    and availability
    
    This is the CORE business logic of the project. The formula is:
    Decision Score = (Rating/5)*40 + min(log(reviews+1)*10, 30) + (24hrs ? 30 : 0)
    
    Why these weights?
    - Rating (40%): Quality is most important for user safety
    - Reviews (30%): Popularity indicates reliability (logarithmic to prevent big chain bias)
    - 24hrs (30%): Convenience for travelers

    Args:
        rating: Google Maps average rating (0.0-5.0)
        total_reviews: Number of reviews (must be >= 0)
        open_24_hours: True if station operates 24/7
        
    Returns:
        Integer score between 0-100
        
    Raises:
        ValueError: If rating is outside [0, 5] or reviews is negative
        
    Examples:
        >>> calculate_decision_score(5.0, 1000, True)
        100
        >>> calculate_decision_score(0.0, 0, False)
        0
    
    References:
        - Formula documented in workflows/README.md
        - PEP 484: Type hints
    """
    # validation fail with clear error messages (best practice)
    if not 0 <= rating <= 5:
        raise ValueError(f"Rating {rating} must be between 0 and 5")
    
    if total_reviews < 0:
        raise ValueError(f"Reviews {total_reviews} cannot be negative")

    # Component 1: rating score (40 points max)
    # normalized 0-5 to 0-40 scale
    rating_score = (rating/5)*40

    # Component 2: reviews score (30 points max, logarithmic)
    # why logarithmic? So 1000 reviews doesn't unfarly dominate over 100 reviews
    # log10(1) = 0, log10(10) = 1, log10(100) = 2, log10(1000) = 3, etc.
    reviews_score = min(math.log10(total_reviews + 1) * 10, 30)

    # Component 3: availability score (30 points max)
    # binary either 30 points or 0
    availability_score = 30 if open_24_hours else 0

    # total sum all components and round to integer
    # why round? User dont'n care about decimals
    total_score = rating_score + reviews_score + availability_score
    return round(total_score)