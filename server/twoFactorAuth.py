import pyotp
import qrcode
import random

def generateCodes():
    code1 = pyotp.random_base32()
    code2 = pyotp.random_base32()
    code3 = pyotp.random_base32()
    return code1, code2, code3

def verifyCodes(code1, code2, code3, userOTP, authNum):
    otp1 = pyotp.TOTP(code1)
    otp2 = pyotp.TOTP(code2)
    otp3 = pyotp.TOTP(code3)

    pass1 = otp1.now()
    pass2 = otp2.now()
    pass3 = otp3.now()

    success1 = (pass1 == userOTP)
    success2 = (pass2 == userOTP)
    success3 = (pass3 == userOTP)

    print(f"OTP 1: {pass1} OTP 2: {pass2} OTP 3: {pass3}")

    match authNum:
        case 1:
            if success1:
                return "SUCCESS"
            elif success2 or success3:
                return "HONEYTOKEN"
            else:
                return "FAILURE"
        case 2:
            if success2:
                return "SUCCESS"
            elif success1 or success3:
                return "HONEYTOKEN"
            else:
                return "FAILURE"
        case 3:
            if success3:
                return "SUCCESS"
            elif success1 or success2:
                return "HONEYTOKEN"
            else:
                return "FAILURE"
            
def generateRandomNumber():
    random_number = random.randint(0, 999999)
    padded_number = f"{random_number:06}"
    return padded_number
