import json

class AIService:
    """
    Deterministic stub for AI service. 
    In Phase 2, this will be replaced with an actual LLM API call.
    """
    
    def analyze_decision(self, product) -> dict:
        # Determine some mock deterministic factors based on product data
        price_val = product.price
        rating_val = product.rating or 0.0
        
        factors = []
        if rating_val >= 4.5:
            factors.append("Highly rated by other users")
        if price_val < 1000:
            factors.append("Great value for the price")
            
        concerns = []
        if rating_val < 4.0:
            concerns.append("Rating is below average")
        if product.review_count < 50:
            concerns.append("Low number of reviews, might be a new product")
            
        return {
            "decision_factors": factors,
            "concerns": concerns,
            "supporting_info": {"notes": "Based on deterministic analysis for MVP."},
            "ai_summary": f"This {product.brand} {product.name} is a solid choice if you value {factors[0] if factors else 'design'} over some minor concerns.",
            "recommendation": "BUY" if rating_val >= 4.0 and price_val < 2500 else "WAIT",
            "confidence": "High" if product.review_count > 100 else "Medium"
        }
    
    def compare_products(self, products: list) -> dict:
        if len(products) < 2:
            return {}
            
        p1, p2 = products[0], products[1]
        
        diffs = [
            f"{p1.brand} is priced at Rs.{p1.price}, while {p2.brand} is Rs.{p2.price}",
            f"{p1.brand} has a rating of {p1.rating}, compared to {p2.brand}'s {p2.rating}"
        ]
        
        recommendation = f"Choose {p1.brand} for better value, or {p2.brand} if you prefer that style."
        
        return {
            "comparison_factors": ["Price", "Rating", "Brand"],
            "key_differences": diffs,
            "recommendation": recommendation
        }

ai_service = AIService()
