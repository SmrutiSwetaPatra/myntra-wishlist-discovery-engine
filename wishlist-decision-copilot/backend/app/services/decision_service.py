import json
from sqlalchemy.orm import Session
from app.models.decision import Decision, Comparison
from app.models.product import Product
from app.services.ai_service import ai_service

def analyze_product_decision(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
        
    ai_result = ai_service.analyze_decision(product)
    
    db_decision = Decision(
        product_id=product_id,
        decision_factors=json.dumps(ai_result.get("decision_factors")),
        concerns=json.dumps(ai_result.get("concerns")),
        supporting_info=json.dumps(ai_result.get("supporting_info")),
        ai_summary=ai_result.get("ai_summary"),
        recommendation=ai_result.get("recommendation"),
        confidence=ai_result.get("confidence")
    )
    db.add(db_decision)
    db.commit()
    db.refresh(db_decision)
    
    # Return as dict matching the schema (parsing JSON strings back)
    return {
        "id": db_decision.id,
        "product_id": db_decision.product_id,
        "decision_factors": json.loads(db_decision.decision_factors) if db_decision.decision_factors else [],
        "concerns": json.loads(db_decision.concerns) if db_decision.concerns else [],
        "supporting_info": json.loads(db_decision.supporting_info) if db_decision.supporting_info else {},
        "ai_summary": db_decision.ai_summary,
        "recommendation": db_decision.recommendation,
        "confidence": db_decision.confidence,
        "timestamp": db_decision.timestamp
    }

def compare_products(db: Session, product_ids: list):
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    if len(products) < 2:
        return None
        
    ai_result = ai_service.compare_products(products)
    
    db_comparison = Comparison(
        product_ids=json.dumps(product_ids),
        comparison_factors=json.dumps(ai_result.get("comparison_factors")),
        key_differences=json.dumps(ai_result.get("key_differences")),
        recommendation=json.dumps(ai_result.get("recommendation"))
    )
    db.add(db_comparison)
    db.commit()
    db.refresh(db_comparison)
    
    return {
        "id": db_comparison.id,
        "product_ids": json.loads(db_comparison.product_ids),
        "comparison_factors": json.loads(db_comparison.comparison_factors) if db_comparison.comparison_factors else [],
        "key_differences": json.loads(db_comparison.key_differences) if db_comparison.key_differences else [],
        "recommendation": json.loads(db_comparison.recommendation) if db_comparison.recommendation else {},
        "timestamp": db_comparison.timestamp
    }
