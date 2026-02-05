from typing import Dict, Any
from fastapi import HTTPException
from app.models.scale import Scale, AnswerValue

def validate_answers(scale: Scale, answers: Dict[str, AnswerValue]) -> Dict[str, Any]:
    """
    Validate answers against scale definition.
    Returns normalized answers (converted to correct types).
    """
    validated = {}
    errors = []
    
    for item in scale.items:
        item_id = item.item_id
        answer = answers.get(item_id)
        
        # Check required
        if item.required and answer is None:
            errors.append(f"Item '{item_id}' is required")
            continue
        
        if answer is None:
            continue
        
        # Validate by type
        try:
            if item.item_type == "single_choice":
                validated[item_id] = _validate_single_choice(item, answer)
            
            elif item.item_type == "multi_choice":
                validated[item_id] = _validate_multi_choice(item, answer)
            
            elif item.item_type == "numeric":
                validated[item_id] = _validate_numeric(item, answer)
            
            elif item.item_type == "text":
                validated[item_id] = str(answer)
            
            else:
                errors.append(f"Unknown item type '{item.item_type}' for item '{item_id}'")
        
        except ValueError as e:
            errors.append(f"Item '{item_id}': {str(e)}")
    
    if errors:
        raise HTTPException(status_code=422, detail={
            "message": "Validation failed",
            "errors": errors
        })
    
    return validated


def _validate_single_choice(item, answer) -> int:
    """Validate and normalize single choice answer"""
    # Convert to int if possible
    try:
        answer_int = int(answer)
    except (ValueError, TypeError):
        raise ValueError(f"Expected integer, got {type(answer).__name__}")
    
    # Check if answer matches available options
    if item.options:
        valid_keys = [int(opt.key) if isinstance(opt.key, (int, str)) and str(opt.key).isdigit() else opt.key 
                      for opt in item.options]
        if answer_int not in valid_keys:
            raise ValueError(f"Invalid option. Expected one of {valid_keys}, got {answer_int}")
    
    return answer_int


def _validate_multi_choice(item, answer) -> List[int]:
    """Validate multi-choice answer"""
    if not isinstance(answer, list):
        raise ValueError(f"Expected list for multi-choice, got {type(answer).__name__}")
    
    validated = []
    for val in answer:
        try:
            validated.append(int(val))
        except (ValueError, TypeError):
            raise ValueError(f"All multi-choice values must be integers, got {val}")
    
    return validated


def _validate_numeric(item, answer) -> float:
    """Validate numeric answer"""
    try:
        val = float(answer)
    except (ValueError, TypeError):
        raise ValueError(f"Expected numeric value, got {type(answer).__name__}")
    
    if item.min_value is not None and val < item.min_value:
        raise ValueError(f"Value {val} below minimum {item.min_value}")
    
    if item.max_value is not None and val > item.max_value:
        raise ValueError(f"Value {val} above maximum {item.max_value}")
    
    return val