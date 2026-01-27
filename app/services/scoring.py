from typing import Dict, Tuple, Any

def score_scale(scale: Dict[str, Any], answers: Dict[str, int]) -> Tuple[int, str]:
    """
    Args:
        scale: 量表資料（包含 items 和 scoring.interpretation）
        answers: 使用者答案 {item_id: score}
    """
    # 計算總分
    total = 0
    
    # 如果量表有 items，考慮 weight 和 reverse
    if "items" in scale:
        for item in scale["items"]:
            item_id = item["item_id"]
            if item_id in answers:
                score = answers[item_id]
                weight = item.get("weight", 1.0)
                reverse = item.get("reverse", False)
                
                # 如果是反向計分
                if reverse:
                    # 假設最大分數為1（yes=1, no=0），反向則為 1-score
                    score = 1 - score
                
                total += score * weight
    else:
        # 簡單加總
        total = sum(answers.values())
    
    # 根據分數找出對應的等級
    level_label = "未知"
    
    # 優先使用 scoring.interpretation
    if "scoring" in scale and "interpretation" in scale["scoring"]:
        for level in scale["scoring"]["interpretation"]:
            min_score = level.get("min", 0)
            max_score = level.get("max", float('inf'))
            
            if min_score <= total <= max_score:
                level_label = level.get("label", "未知")
                break
    # 向後兼容舊的 levels 格式
    elif "levels" in scale:
        for level in scale["levels"]:
            min_score = level.get("min", 0)
            max_score = level.get("max", float('inf'))
            
            if min_score <= total <= max_score:
                level_label = level.get("label", "未知")
                break
    
    return int(total), level_label