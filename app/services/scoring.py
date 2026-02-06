#app/services/scoring.py
def score_scale(scale: dict, answers: dict) -> tuple[float, str]:
    """
    Args:
        scale: Scale definition from JSON
        answers: Dict of {item_id: answer_key} (e.g., {"gds15_q01": 1})
    """
    total = 0.0
    
    for item in scale.get("items", []):
        item_id = item["item_id"]
        answer_value = answers.get(item_id)
        
        if answer_value is None:
            continue
        
        # For GDS-15 style scales, the answer is directly the score (0 or 1)
        # If using options array, we'd map it here
        score_value = answer_value
        
        if not isinstance(score_value, (int, float)):
            continue
     
        #reverse scoring if needed
        if item.get("reverse", False):
            score_value = 1 - score_value
            
        weight = item.get("weight", 1.0)
        total += score_value * weight
    
    #get interpretation
    interpretation = "未分類"
    for interp in scale.get("scoring", {}).get("interpretation", []):
        if interp["min"] <= total <= interp["max"]:
            interpretation = interp["label"]
            break
    
    return total, interpretation