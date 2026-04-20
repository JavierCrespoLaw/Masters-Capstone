import sqlite3
import os

Users = ".\\databases\\users\\databaseUsers.db"
Codes = ".\\databases\\codes\\databaseCodes.db"
AuthenticationNumbers = ".\\databases\\authenticationNumbers\\databaseAuthenticationNumbers.db"


# Creates userData.db if it doesn't exist
def createDatabases():
    os.makedirs(".\\databases\\users", exist_ok=True)
    os.makedirs(".\\databases\\codes", exist_ok=True)
    os.makedirs(".\\databases\\authenticationNumbers", exist_ok=True)

    conn = sqlite3.connect(Users)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
                   username TEXT PRIMARY KEY,
                   email TEXT NOT NULL,
                   password TEXT NOT NULL,
                   secure BOOLEAN NOT NULL
    )""")
    conn.commit()
    conn.close()

    conn = sqlite3.connect(Codes)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS codes (
                   username TEXT PRIMARY KEY,
                   code1 INTEGER NOT NULL,
                   code2 INTEGER NOT NULL,
                   code3 INTEGER NOT NULL
    )""")
    conn.commit()
    conn.close()

    conn = sqlite3.connect(AuthenticationNumbers)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authNums (
                   username TEXT PRIMARY KEY,
                   number INTEGER NOT NULL
    )""")
    conn.commit()
    conn.close()

# Saves the given email and password to the database
def saveToUserDatabase(username, email, password):

    conn = sqlite3.connect(Users)
    cursor = conn.cursor()

    query = "INSERT OR IGNORE INTO users (username, email, password, secure) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (username, email, password, True))

    conn.commit()
    conn.close()

def saveToAuthenticationNumbersDatabase(username, number):
    conn = sqlite3.connect(AuthenticationNumbers)
    cursor = conn.cursor()

    query = "INSERT OR IGNORE INTO authNums (username, number) VALUES (?, ?)"
    cursor.execute(query, (username, number))

    conn.commit()
    conn.close()

def saveToCodesDatabase(username, code1, code2, code3):

    conn = sqlite3.connect(Codes)
    cursor = conn.cursor()

    query = "INSERT OR IGNORE INTO codes (username, code1, code2, code3) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (username, code1, code2, code3))

    conn.commit()
    conn.close()

# saveToDatabase("test@email.com", "testpass123")

def existsInDatabase(username, password):
    conn = sqlite3.connect(Users)
    cursor = conn.cursor()

    #cursor.execute(f"""
    #SELECT password FROM users WHERE email = {email}
    #""")

    query = "SELECT password FROM users WHERE username = ?"
    cursor.execute(query, (username,))

    data = cursor.fetchone()
    print(data)

    if data is not None:
        if data[0] == password:
            return True
        
    return False


def emailInDatabase(email):
    conn = sqlite3.connect(Users)
    cursor = conn.cursor()

    query = "SELECT EXISTS(SELECT 1 FROM users WHERE email = ?)"
    cursor.execute(query, (email,))

    c = cursor.fetchone()
    print(c)

    if c[0] == 1:
        return True
    else:
        return False
    
def usernameInDatabase(username):
    conn = sqlite3.connect(Users)
    cursor = conn.cursor()

    query = "SELECT EXISTS(SELECT 1 FROM users WHERE username = ?)"
    cursor.execute(query, (username,))

    c = cursor.fetchone()
    print(c)

    if c[0] == 1:
        return True
    else:
        return False
    
def getCodesFromDatabase(username):
    conn = sqlite3.connect(Codes)
    cursor = conn.cursor()

    query = "SELECT code1, code2, code3 FROM codes WHERE username = ?"
    cursor.execute(query, (username,))

    data = cursor.fetchone()

    if data is not None:
        return data[0], data[1], data[2]
    
    return None, None, None

def getAuthNumFromDatabase(username):
    conn = sqlite3.connect(AuthenticationNumbers)
    cursor = conn.cursor()

    query = "SELECT number FROM authNums WHERE username = ?"
    cursor.execute(query, (username,))
    data = cursor.fetchone()
    if data is not None:
        return data[0]
    return None



def main():
    # print("Attempting to save something to database")
    # saveToDatabase("testing@email.com", "TestPass#123")
    #print("Check if email and password exists in database")
    #print(emailInDatabase("test@email.com"))
    #print(usernameInDatabase("TestUser"))
    #print(existsInDatabase("TestUser", "fakepass"))

    print("Creating databases. ")
    createDatabases()

if __name__ == "__main__":
    main()