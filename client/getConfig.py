import os
from dotenv import load_dotenv, dotenv_values
# Values that will be included in config file:
# IP_ADDRESS - The IP address of the server

# Loads the environment variables from the env file so that they can be accessed
def loadEnvValues():
    load_dotenv()
    return testEnvValues()

# Checks to make sure that each of the environment variables are filled in
def testEnvValues():
    envValues = []
    envValues.append(os.getenv("IP_ADDRESS"))
    for x in envValues:
        if x == None or x == "":
            return False
    return True

# Gets the IP Address field from the environment variables
def getIPAddress():
    return os.getenv("IP_ADDRESS")