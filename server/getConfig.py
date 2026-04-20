import os
from dotenv import load_dotenv, dotenv_values
# Values that will be included in config file:
# EMAIL_SERVER - The email used by the server
# PASSWORD_SERVER - The password used by the server's email

def loadEnvValues():
    load_dotenv()
    return testEnvValues()

def testEnvValues():
    envValues = []
    envValues.append(os.getenv("EMAIL_SERVER"))
    envValues.append(os.getenv("PASSWORD_SERVER"))
    envValues.append(os.getenv("TEST"))
    for x in envValues:
        if x == None or x == "":
            return False
    return True

def getEmailServer():
    return os.getenv("EMAIL_SERVER")

def getPasswordServer():
    return os.getenv("PASSWORD_SERVER")