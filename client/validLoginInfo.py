import re
from email_validator import validate_email, EmailNotValidError

def checkValidUsername(username):

    length = len(username)

    if length > 20 or length < 8:
        return False
    
    return True

def checkValidEmail(email):
    try:
        valid = validate_email(email)
        return True
    except EmailNotValidError:
        return False

def checkValidPassword(password):

    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{6,20}$"

    pat = re.compile(reg)

    mat = re.search(pat, password)

    return mat
    

