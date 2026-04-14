import sqlite3

# Creates userData.db if it doesn't exist
def createDatabase():

    conn = sqlite3.connect("userData.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
                   username TEXT PRIMARY KEY,
                   email TEXT NOT NULL,
                   password TEXT NOT NULL
    )""")

    conn.commit()
    conn.close()

# Saves the given email and password to the database
def saveToDatabase(username, email, password):

    createDatabase()

    conn = sqlite3.connect("userData.db")
    cursor = conn.cursor()

    query = "INSERT OR IGNORE INTO users (username, email, password) VALUES (?, ?, ?)"
    cursor.execute(query, (username, email, password))

    conn.commit()
    conn.close()


# saveToDatabase("test@email.com", "testpass123")

def existsInDatabase(username, password):
    conn = sqlite3.connect("userData.db")
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
    conn = sqlite3.connect("userData.db")
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
    conn = sqlite3.connect("userData.db")
    cursor = conn.cursor()

    query = "SELECT EXISTS(SELECT 1 FROM users WHERE username = ?)"
    cursor.execute(query, (username,))

    c = cursor.fetchone()
    print(c)

    if c[0] == 1:
        return True
    else:
        return False




def main():
    # print("Attempting to save something to database")
    # saveToDatabase("testing@email.com", "TestPass#123")
    print("Check if email and password exists in database")
    print(emailInDatabase("test@email.com"))
    print(usernameInDatabase("TestUser"))
    print(existsInDatabase("TestUser", "fakepass"))

if __name__ == "__main__":
    main()