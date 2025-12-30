import re
from email_validator import validate_email as email_validator, EmailNotValidError


def validate_email(email):
    """
    Validate email format
    Returns: (is_valid, error_message)
    """
    try:
        # For testing, skip DNS check
        email_validator(email, check_deliverability=False)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)


def validate_password_strength(password):
    """
    Validate password strength
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    
    Returns: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, None


def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present in request data
    Returns: (is_valid, missing_fields)
    """
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return False, missing_fields
    
    return True, None
