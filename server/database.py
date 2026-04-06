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

    query = "INSERT OR IGNORE INTO users (email, password) VALUES (?, ?)"
    cursor.execute(query, (email, password))

    conn.commit()
    conn.close()


# saveToDatabase("test@email.com", "testpass123")

def existsInDatabase(email, password):
    conn = sqlite3.connect("userData.db")
    cursor = conn.cursor()

    #cursor.execute(f"""
    #SELECT password FROM users WHERE email = {email}
    #""")

    query = "SELECT password FROM users WHERE email = ?"
    cursor.execute(query, (email,))

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




def main():
    # print("Attempting to save something to database")
    # saveToDatabase("testing@email.com", "TestPass#123")
    print("Check if email and password exists in database")
    print(emailInDatabase("test@email.com"))

if __name__ == "__main__":
    main()