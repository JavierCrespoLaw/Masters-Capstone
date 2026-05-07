import sqlite3
import os

# File paths of the databases
Users = ".\\databases\\users\\databaseUsers.db"
Codes = ".\\databases\\codes\\databaseCodes.db"
AuthenticationNumbers = ".\\databases\\authenticationNumbers\\databaseAuthenticationNumbers.db"

# Creates databases for user info, 2FA codes, and authentication numbers if they don't exist already
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

# Saves the given username, email and password to the database
def saveToUserDatabase(username, email, password):

    conn = sqlite3.connect(Users)
    cursor = conn.cursor()

    query = "INSERT OR IGNORE INTO users (username, email, password, secure) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (username, email, password, True))

    conn.commit()
    conn.close()

# Saves the given username and authentication number to the database
def saveToAuthenticationNumbersDatabase(username, number):
    conn = sqlite3.connect(AuthenticationNumbers)
    cursor = conn.cursor()

    query = "INSERT OR IGNORE INTO authNums (username, number) VALUES (?, ?)"
    cursor.execute(query, (username, number))

    conn.commit()
    conn.close()

# Saves the given username and authentication codes to the database
def saveToCodesDatabase(username, code1, code2, code3):

    conn = sqlite3.connect(Codes)
    cursor = conn.cursor()

    query = "INSERT OR IGNORE INTO codes (username, code1, code2, code3) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (username, code1, code2, code3))

    conn.commit()
    conn.close()

# Checks if the given username and password combination exists in the database
def existsInDatabase(username, password):
    conn = sqlite3.connect(Users)
    cursor = conn.cursor()

    query = "SELECT password FROM users WHERE username = ?"
    cursor.execute(query, (username,))

    data = cursor.fetchone()
    print(data)

    if data is not None:
        if data[0] == password:
            return True
        
    return False

# Checks if the given email exists in the database
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
    
# Checks if the given username exists in the database
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
    
# Gets the codes associated with the given username
def getCodesFromDatabase(username):
    conn = sqlite3.connect(Codes)
    cursor = conn.cursor()

    query = "SELECT code1, code2, code3 FROM codes WHERE username = ?"
    cursor.execute(query, (username,))

    data = cursor.fetchone()

    if data is not None:
        return data[0], data[1], data[2]
    
    return None, None, None

# Gets the authentication number associated with the given username
def getAuthNumFromDatabase(username):
    conn = sqlite3.connect(AuthenticationNumbers)
    cursor = conn.cursor()

    query = "SELECT number FROM authNums WHERE username = ?"
    cursor.execute(query, (username,))
    data = cursor.fetchone()
    if data is not None:
        return data[0]
    return None

# Gets the username associated with the given email
def getUsernameFromDatabase(email):
    conn = sqlite3.connect(Users)
    cursor = conn.cursor()

    query = "SELECT username FROM users WHERE email = ?"
    cursor.execute(query, (email,))

    data = cursor.fetchone()

    if data is not None:
        return data[0]
    return None

# Gets the password associated with the given username
def getPasswordFromDatabase(username):
    conn = sqlite3.connect(Users)
    cursor = conn.cursor()

    query = "SELECT password FROM users WHERE username = ?"
    cursor.execute(query, (username,))

    data = cursor.fetchone()

    if data is not None:
        return data[0]
    return None

# Gets the secure value associated with the given username
def getSecureFromDatabase(username):
    conn = sqlite3.connect(Users)
    cursor = conn.cursor()

    query = "SELECT secure FROM users WHERE username = ?"
    cursor.execute(query, (username,))

    data = cursor.fetchone()

    if data is not None:
        return data[0]
    return None

# Replaces the password value associated with the given username with a new password value
def updatePassword(username, newPassword):
    conn = sqlite3.connect(Users)
    cursor = conn.cursor()

    query = "UPDATE users SET password = ? WHERE username = ?"
    cursor.execute(query, (newPassword, username))

    conn.commit()
    conn.close()

# Replaces the authentication number value associated with the given username with a new authentication number value
def updateAuthNum(username, newAuthNum):
    conn = sqlite3.connect(AuthenticationNumbers)
    cursor = conn.cursor()

    query = "UPDATE authNums SET number = ? WHERE username = ?"
    cursor.execute(query, (newAuthNum, username))

    conn.commit()
    conn.close()

# Replaces the secure value associated with the given username with a new secure value
def updateSecure(username, newSecure):
    conn = sqlite3.connect(Users)
    cursor = conn.cursor()

    query = "UPDATE users SET secure = ? WHERE username = ?"
    cursor.execute(query, (newSecure, username))

    conn.commit()
    conn.close()

# Replaces the authentication code values associated with the given username with new authentication code values
def updateAuthCodes(username, code1, code2, code3):

    conn = sqlite3.connect(Codes)
    cursor = conn.cursor()

    query = "UPDATE codes SET code1 = ?, code2 = ?, code3 = ? WHERE username = ?"
    cursor.execute(query, (code1, code2, code3, username))

    conn.commit()
    conn.close()

# Main function used for testing the database
def main():
    # print("Attempting to save something to database")
    # saveToDatabase("testing@email.com", "TestPass#123")
    #print("Check if email and password exists in database")
    #print(emailInDatabase("test@email.com"))
    #print(usernameInDatabase("TestUser"))
    #print(existsInDatabase("TestUser", "fakepass"))

    print("Creating databases. ")
    createDatabases()
    print(emailInDatabase)

if __name__ == "__main__":
    main()