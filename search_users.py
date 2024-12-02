from datetime import datetime
import sqlite3

# Function to search for users matching a keyword
def search_users(conn, keyword, user_id):
    if keyword == '':
        print("no keyword to search for")
        return
    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Execute an SQL query to search for users whose names contain the keyword
    cursor.execute("""
        SELECT usr, name, city
        FROM users
        WHERE name LIKE ?
        ORDER BY
            CASE
                WHEN name = ? THEN 0
                ELSE LENGTH(name)
            END
    """, ('%' + keyword + '%', keyword,))
    
    # Fetch the search results for users with matching names
    usersname = cursor.fetchall()

    # Execute an SQL query to search for users whose cities and not names contain the keyword
    cursor.execute("""
        SELECT usr, name, city
        FROM users
        WHERE city LIKE ? AND name NOT LIKE ?
        ORDER BY
            CASE
                WHEN city = ? THEN 0
                ELSE LENGTH(city)
            END
    """, ('%' + keyword + '%','%' + keyword + '%',keyword))

    # Fetch the search results for users with matching cities but not names
    userscity = cursor.fetchall()

    # Combine the results from both name and city searches
    users = usersname + userscity

    # Check if any matching users were found
    if len(users) == 0:
        print("No matching users found.")
        return

    count = 0
    # Display the first 5 matching users
    for i in range(count, min(count + 5, len(users))):
        print(f"{i + 1}. Name: {users[i][1]}")

    count += 5

    while True:
        # case when search results contain more than 5 matching users
        if len(users) > 5:
            choice = input("'0' to view more or Enter the number of a user to see more information or 'back' to go back: ")
            if choice == 'back':
                return
            # If there are more than 5 matching users, provide an option to view more
            elif choice == '0':
                if count >= len(users):
                    print("No more users.")
                    continue
                # prints the next 5 users 
                for i in range(count, min(count + 5, len(users))):
                    print(f"{i + 1}. Name: {users[i][1]}")
                    count += 5
            elif choice.isdigit():
                # check if selected user is valid
                if int(choice) > 0 and int(choice) < (len(users) + 1):
                    try:
                        selected_user = users[int(choice) - 1]

                        # displays the information about selected user
                        user_info = get_user_info(conn, selected_user[0])
                        display_user_info(user_info)
                        goback = False
                        count2 = 3
                        while not goback:
                            # ask user if they want to follow user or view more tweeets
                            follow = input("'0' to follow user, '1' to view more tweets, 'back' to go back: ")
                            if follow == '0':
                                # Check if the user is already following the selected user
                                cursor.execute("SELECT * FROM follows WHERE flwer = ? AND flwee = ?", (user_id, selected_user[0]))
                                existing_follow = cursor.fetchone()

                                if existing_follow:
                                    print("You are already following this user.")
                                    goback = True
                                else:
                                    # Insert a new follow record
                                    cursor.execute("INSERT INTO follows VALUES (?, ?, ?)", (user_id, selected_user[0], datetime.now().strftime('%Y-%m-%d')))
                                    print("You are now following this user.")
                                    conn.commit()
                                    goback = True
                            # prints 3 more tweets
                            elif follow == '1' and (user_info['tweet_count'] > 3):
                                print_more_tweets(user_info, count2)
                                count2 += 3
                            elif follow == '1' and (user_info['tweet_count'] <= 3):
                                print("no more tweets")
                            elif follow == 'back':
                                goback = True
                            else:
                                print("Invalid choice. Please try again.")
                    except (ValueError, IndexError):
                        print("Invalid choice. Please try again.")
                else:
                    print("Invalid choice. Please try again.")
            else:
                print("Invalid choice. Please try again.")

        # case when search results contain 5 of less matching users
        elif len(users) <= 5:
            choice = input("Enter the number of a user to see more information or 'back' to go back: ")
            if choice == 'back':
                return
            elif choice.isdigit():
                if int(choice) > 0 and int(choice) < (len(users) + 1):
                    try:
                        selected_user = users[int(choice) - 1]

                        # displays the information about selected user
                        user_info = get_user_info(conn, selected_user[0])
                        display_user_info(user_info)
                        goback = False
                        count2 = 3
                        while not goback:
                            # ask user if they want to follow user or view more tweeets
                            follow = input("'0' to follow user, '1' to view more tweets, 'back' to go back: ")
                            if follow == '0':
                                # Check if the user is already following the selected user
                                cursor.execute("SELECT * FROM follows WHERE flwer = ? AND flwee = ?", (user_id, selected_user[0]))
                                existing_follow = cursor.fetchone()

                                if existing_follow:
                                    print("You are already following this user.")
                                    goback = True
                                else:
                                    # Insert a new follow record
                                    cursor.execute("INSERT INTO follows VALUES (?, ?, ?)", (user_id, selected_user[0], datetime.now().strftime('%Y-%m-%d')))
                                    print("You are now following this user.")
                                    conn.commit()
                                    goback = True
                            # prints 3 more tweets
                            elif follow == '1' and (user_info['tweet_count'] > 3):
                                print_more_tweets(user_info, count2)
                                count2 += 3
                            elif follow == '1' and (user_info['tweet_count'] <= 3):
                                print("no more tweets")
                            elif follow == 'back':
                                goback = True
                            else:
                                print("Invalid choice. Please try again.")
                    except (ValueError, IndexError):
                        print("Invalid choice. Please try again.")
                else:
                    print("Invalid choice. Please try again.")
            else:
                print("Invalid choice. Please try again.")

# Function to retrieve user information
def get_user_info(conn, user_id):
    cursor = conn.cursor()

    # Get the number of tweets posted by the user
    cursor.execute("SELECT COUNT(*) FROM tweets WHERE writer = ?", (user_id,))
    tweet_count = cursor.fetchone()[0]

    # Get the number of users being followed by the user
    cursor.execute("SELECT COUNT(*) FROM follows WHERE flwer = ?", (user_id,))
    following_count = cursor.fetchone()[0]

    # Get the number of followers of the user
    cursor.execute("SELECT COUNT(*) FROM follows WHERE flwee = ?", (user_id,))
    followers_count = cursor.fetchone()[0]

    # Get up to 3 most recent tweets of the user
    cursor.execute("""
        SELECT tid, writer, tdate, text
        FROM tweets
        WHERE writer = ?
        ORDER BY tdate DESC
    """, (user_id,))
    recent_tweets = cursor.fetchall()

    # Return the retrieved user information as a dictionary
    return {
        'tweet_count': tweet_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'recent_tweets': recent_tweets,
    }

# Function to display user information
def display_user_info(user_info):
    print(f"Number of Tweets: {user_info['tweet_count']}")
    print(f"Number of Following: {user_info['following_count']}")
    print(f"Number of Followers: {user_info['followers_count']}")

    if user_info['recent_tweets']:
        print("Recent Tweets:")
        for i in range(0, min(3, len(user_info['recent_tweets']))):
            print(f"  Text: {user_info['recent_tweets'][i][3]}")

# Function to print more recent tweets for a user
def print_more_tweets(user_info, count):
    if count >= user_info['tweet_count']:
        print("No more tweets")
    else:
        print("Recent Tweets:")
        for i in range(count, min(count + 3, user_info['tweet_count'])):
            print(f"  Text: {user_info['recent_tweets'][i][3]}")
