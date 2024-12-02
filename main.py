import sqlite3
import sys
import os
from user import login, register_user
from list_followers import *
from search_tweets import *
from compose_tweet import *
from search_users import *
from display_tweets import *

# Initialize SQLite database connection
# Do not hard code file name. Pass as a command line argument
if len(sys.argv) == 2:
        db_file = sys.argv[1]
        if not os.path.exists(db_file):
            print("Error: The specified file does not exist.")
            sys.exit(1)
else:
       while True:
        db_file = input("Enter the database file name: ")
        if os.path.exists(db_file):
            break
        else:
            print("Error: The specified file does not exist. Please enter a valid database file name.")
print(f"Using database file: {db_file}")

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Main menu
while True:
    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        user_id = login(conn)
        if user_id:
            display_tweets_and_retweets(conn,user_id)
            while True:
                print("1. Back to Display Tweets or Retweets")
                print("2. Search for Tweets")
                print("3. Search for Users")
                print("4. Compose a Tweet")
                print("5. List Followers")
                print("6. Logout")

                user_choice = input("Enter your choice: ")

                if user_choice == '1':
                    display_tweets_and_retweets(conn,user_id)
                elif user_choice == '2':
                    keywords = input("Enter keywords: ")
                    search_tweets(conn, user_id, keywords)
                elif user_choice == '3':
                    keyword = input("Enter a keyword: ")
                    search_users(conn, keyword, user_id)
                elif user_choice == '4':
                    tweet_text = input("Compose your tweet: ")
                    replyto = None
                    compose_tweet(conn, user_id, tweet_text,replyto)
                elif user_choice == '5':
                    list_followers(conn, user_id)
                elif user_choice == '6':
                    break
    elif choice == '2':
        register_user(conn)
    elif choice == '3':
        break

# Close the database connection
conn.close()
