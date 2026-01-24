"""
Test suite for decision score algorithm
Test the core business logic of gas station ranking
"""
import pytest
from src.scorer import calculate_decision_score

# Test suite

class TestBasicScoring:
    """test for normal  use cases with typical gas station data"""

    def test_perfect_station_scores_100(self):
        """A perfect station (5 stars, 1000+ reviews, 24hrs) should score 100"""
        # Why 1000 reviews? log10(1001) * 10 = 30 (hits the max)
        score = calculate_decision_score(5.0, 1000, True)
        assert score  == 100, "Perfect station should score 100"

    def test_worst_station_scores_0(self):
        """worst station (0 stars, 0 reviews, not 24hrs) should score 0"""
        score = calculate_decision_score(0.0, 0, False)
        assert score == 0, "Worst station should score 0"

    def test_average_station(self):
        """Average station (3.5 stars, 50 reviews, not 24hrs"""
        # manual calculation:
        # rating_score = (3.5/5)*40 = 28
        # reviews_score = log10(51)*10 = 17.07 = 17
        # availability_score = 0
        # total_score = 28 + 17 + 0 = 45
        score = calculate_decision_score(3.5, 50, False)
        assert 44 <= score <= 46, f"Expected ~45, got{score}"

    def test_high_rating_few_reviews(self):
        """New station with 5 stars but few reviews, not 24 hrs"""
        score = calculate_decision_score(5.0, 10, False)
        # rating: 40, reviews: log10(11)*10 ≈ 10.4, availability: 0 → total ≈ 50
        assert 49 <= score <= 51, f"Expected ~50, got {score}"


class TestEdgeCases:
    """Test for unusual inputs that might break the function"""

    def test_zero_reviews_doesnt_crash(self):
        """reviews=0 should work (log(0+1) = log(1) = 0)"""
        score = calculate_decision_score(4.0, 0, True)
        # rating: 32, reviews: 0, availability: 30 → 62
        assert score == 62
    
    def test_single_review(self):
        """Single review should contribute some points"""
        score = calculate_decision_score(5.0, 1, False)
        # rating: 40, reviews: log(2)*10 ≈ 3, availability: 0 → 43
        assert score >= 42, "Single review should count for something"
    
    def test_extremely_high_reviews_caps_at_30(self):
        """10 million reviews shouldn't exceed 30 points"""
        score = calculate_decision_score(5.0, 10_000_000, True)
        assert score == 100  # 40 + 30 (capped) + 30 = 100
class TestInputValidation:
    """Tests that invalid inputs are rejected properly"""
    
    def test_rating_too_high_raises_error(self):
        """Rating > 5 should raise ValueError"""
        with pytest.raises(ValueError, match="Rating .* must be between"):
            calculate_decision_score(6.0, 100, True)
    
    def test_rating_negative_raises_error(self):
        """Negative rating should raise ValueError"""
        with pytest.raises(ValueError, match="Rating .* must be between"):
            calculate_decision_score(-1.0, 100, True)
    
    def test_negative_reviews_raises_error(self):
        """Negative review count makes no sense"""
        with pytest.raises(ValueError, match="Reviews .* cannot be negative"):
            calculate_decision_score(4.0, -10, True)
class TestFormulaComponents:
    """Tests that verify each component of the formula works correctly"""
    
    @pytest.mark.parametrize("rating,expected", [
        (5.0, 40),  # 100% → 40 points
        (4.0, 32),  # 80% → 32 points
        (2.5, 20),  # 50% → 20 points
        (0.0, 0),   # 0% → 0 points
    ])
    def test_rating_scales_linearly(self, rating, expected):
        """Rating component should scale linearly from 0-5 to 0-40"""
        # Isolate rating by setting reviews=0, 24hrs=False
        score = calculate_decision_score(rating, 0, False)
        assert score == expected
    
    def test_reviews_use_logarithmic_scale(self):
        """Verify reviews don't scale linearly (anti-big-chain bias)"""
        score_10 = calculate_decision_score(0, 10, False)
        score_100 = calculate_decision_score(0, 100, False)
        score_1000 = calculate_decision_score(0, 1000, False)
        
        # Logarithmic: each 10x increase adds ~10 points (not linear)
        # log10(11) ≈ 1.04 → 10 points
        # log10(101) ≈ 2.00 → 20 points
        # log10(1001) ≈ 3.00 → 30 points
        assert 9 <= score_10 <= 11
        assert 19 <= score_100 <= 21
        assert 29 <= score_1000 <= 31
    
    def test_24hrs_adds_exactly_30_points(self):
        """24-hour availability should add exactly 30 points"""
        score_closed = calculate_decision_score(3.0, 50, False)
        score_open = calculate_decision_score(3.0, 50, True)
        
        assert score_open - score_closed == 30

"""
- ✅ Escribes código testeado (confiabilidad)
- ✅ Manejas edge cases (defensive programming)
- ✅ Validas inputs (seguridad)
- ✅ Documentas código (mantenibilidad)
"""


    