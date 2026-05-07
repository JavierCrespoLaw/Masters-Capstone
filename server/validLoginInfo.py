import re
from email_validator import validate_email, EmailNotValidError

# Checks if the given username is between 8 and 20 characters long
def checkValidUsername(username):

    length = len(username)

    if length > 20 or length < 8:
        return False
    
    return True

# Checks if the given email is a real one
def checkValidEmail(email):
    try:
        valid = validate_email(email)
        return True
    except EmailNotValidError:
        return False

# Checks if the given password is between 6 to 20 characters long and contains at least
# 1 uppercase, 1 lowercase, 1 number, and 1 special character
def checkValidPassword(password):

    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{6,20}$"

    pat = re.compile(reg)

    mat = re.search(pat, password)

    return mat
    

    