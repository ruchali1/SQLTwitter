import getpass

# User login
def login(conn):
    # Create a cursor
    cursor = conn.cursor()

    user_id = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    cursor.execute("SELECT usr FROM users WHERE usr = ? AND pwd = ?", (user_id, password))
    result = cursor.fetchone()

    if result:
        return user_id
    else:
        print("Invalid username or password.")
        return None
    
#Unique Id's
def get_unique_user_id(cursor):
    cursor.execute("SELECT MAX(usr) FROM users")
    max_id = cursor.fetchone()[0]
    if max_id is not None:
        return max_id + 1
    else:
        return 1  # If there are no existing users, start with user ID 1
    
# User registration
def register_user(conn):
    # Create a cursor
    cursor = conn.cursor()

    #user_id = input("Enter a username: ")
    user_id = get_unique_user_id(cursor)
    password = getpass.getpass("Enter a password: ")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    city = input("Enter your city: ")
    timezone = input("Enter your timezone: ")

    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (user_id, password, name, email, city, timezone))
    conn.commit()
    print(f"Registration successful. Your user ID is: {user_id}, use it to login")

