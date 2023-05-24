import re

def validate(data, regex):
    """Custom Validator"""
    return True if re.match(regex, data) else False

def validatePassword(password: str):
    """Password Validator"""
    regex = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
    return validate(password, regex)

def validateEmail(email: str):
    """Email Validator"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return validate(email, regex)

def validateEmailAndPassword(email: str, password: str):
    """Email and Password Validator"""
    if not (email and password):
        return {
            'email': 'Email is required',
            'password': 'Password is required'
        }
    if not validateEmail(email):
        return {
            'email': 'Email is invalid'
        }
    if not validatePassword(password):
        return {
            'password': 'Password is invalid, should be 8-20 characters long with \
upper and lower case letters, numbers and special characters (@$!%*#?&)'
        }
    return None
