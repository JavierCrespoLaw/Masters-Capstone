import sqlite3

# Creates userData.db if it doesn't exist
def createDatabase():

    conn = sqlite3.connect("userData.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
                   email TEXT PRIMARY KEY,
                   password TEXT NOT NULL
    )""")

    conn.commit()
    conn.close()

# Saves the given email and password to the database
def saveToDatabase(email, password):
    createDatabase()

    conn = sqlite3.connect("userData.db")
    cursor = conn.cursor()

    cursor.execute(f"""
    INSERT OR IGNORE INTO users (email, password) VALUES
    ('{email}', '{password}')
    """)

    conn.commit()
    conn.close()


# saveToDatabase("test@email.com", "testpass123")

def existsInDatabase(email, password):
    conn = sqlite3.connect("userData.db")
    cursor = conn.cursor()

    #cursor.execute(f"""
    #SELECT password FROM users WHERE email = {email}
    #""")

    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))

    data = cursor.fetchone()
    print(data)

    if data is not None:
        if data[0] == password:
            return True
        
    return False


def emailInDatabase(email):
    conn = sqlite3.connect("userData.db")
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT EXISTS(SELECT 1 FROM users WHERE email = {email})
    """)

    c = cursor.fetchone
    print(c)

    if c:
        return True
    else:
        return False

def passwordInDatabase(email, password):
    conn = sqlite3.connect("userData.db")
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT password FROM users WHERE email = {email}
    """)

    row = cursor.fetchone()
    print(row)

    #if row[1] == password :
    #    return True
    #else:
    #    return False
    return True


