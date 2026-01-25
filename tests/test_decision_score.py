"""
Test suite for decision score algorithm
Test the core business logic of gas station ranking
"""
import pytest
from src.scorer import calculate_decision_score

# Test suite

class TestBasicScoring:
    """test for normal use cases with typical gas station data"""

    def test_perfect_station_scores_100(self):
        """
        A perfect station should score 100:
        - 5 stars (40 pts)
        - 1000+ reviews (30 pts)
        - 24hrs (10 pts)
        - 4 amenities (20 pts)
        """
        score = calculate_decision_score(5.0, 1000, True, 4)
        assert score == 100, "Perfect station should score 100"

    def test_worst_station_scores_0(self):
        """worst station (0 stars, 0 reviews, closed, 0 amenities) should score 0"""
        score = calculate_decision_score(0.0, 0, False, 0)
        assert score == 0, "Worst station should score 0"

    def test_average_station(self):
        """Average station (3.5 stars, 50 reviews, closed, 0 amenities)"""
        # manual calculation:
        # rating_score = (3.5/5)*40 = 28
        # reviews_score = log10(51)*10 ≈ 17
        # availability_score = 0
        # amenities_score = 0
        # total_score = 28 + 17 + 0 + 0 = 45
        score = calculate_decision_score(3.5, 50, False, 0)
        assert 44 <= score <= 46, f"Expected ~45, got {score}"

class TestEdgeCases:
    """Test for unusual inputs that might break the function"""

    def test_zero_reviews_doesnt_crash(self):
        """reviews=0 should work"""
        score = calculate_decision_score(4.0, 0, True, 0)
        # rating: 32, reviews: 0, availability: 10, amenities: 0 → 42
        assert score == 42
    
    def test_single_review(self):
        """Single review should contribute some points"""
        score = calculate_decision_score(5.0, 1, False, 0)
        # rating: 40, reviews: log(2)*10 ≈ 3, avail: 0, amen: 0 → 43
        assert score >= 42, "Single review should count for something"
    
    def test_extremely_high_reviews_caps_at_30(self):
        """10 million reviews shouldn't exceed 30 points"""
        score = calculate_decision_score(5.0, 10_000_000, True, 4)
        assert score == 100 

class TestAmenitiesScoring:
    """Tests for the new Amenities component (20%)"""

    def test_each_amenity_adds_5_points(self):
        """1 amenity = 5 points"""
        # Baseline: 3.0 stars (24 pts), 0 reviews (0), closed (0) = 24
        score_0 = calculate_decision_score(3.0, 0, False, 0)
        score_1 = calculate_decision_score(3.0, 0, False, 1)
        assert score_1 - score_0 == 5, "Each amenity should add 5 points"

    def test_amenities_cap_at_20_points(self):
        """5 amenities should score same as 4 (max 20 points)"""
        score_4 = calculate_decision_score(5.0, 0, False, 4)
        score_5 = calculate_decision_score(5.0, 0, False, 5)
        assert score_4 == score_5, "Amenities score should cap at 20 (4 items)"

    def test_full_amenities_score(self):
        """4 amenities = 20 points"""
        score = calculate_decision_score(0.0, 0, False, 4)
        assert score == 20

class TestInputValidation:
    """Tests that invalid inputs are rejected properly"""
    
    
    def test_rating_out_of_bounds_raises_error(self):
        """Rating must be between 0 and 5"""
        with pytest.raises(ValueError, match="Rating .* must be between"):
            calculate_decision_score(6.0, 100, True, 0)
        
        with pytest.raises(ValueError, match="Rating .* must be between"):
            calculate_decision_score(-1.0, 100, True, 0)

    def test_negative_reviews_raises_error(self):
        """Reviews cannot be negative"""
        with pytest.raises(ValueError, match="Reviews .* cannot be negative"):
            calculate_decision_score(4.0, -1, True, 0)

    def test_amenities_negative_raises_error(self):
        """Negative amenities count"""
        with pytest.raises(ValueError, match="Amenities .* cannot be negative"):
            calculate_decision_score(4.0, 100, True, -1)



class TestFormulaComponents:
    """Tests that verify each component of the formula works correctly"""
    
    def test_24hrs_adds_exactly_10_points(self):
        """24-hour availability should add exactly 10 points (Updated weight)"""
        score_closed = calculate_decision_score(3.0, 50, False, 0)
        score_open = calculate_decision_score(3.0, 50, True, 0)
        
        assert score_open - score_closed == 10, "24h should be 10 points now"

    