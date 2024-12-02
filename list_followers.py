#List followers
#The user should be able to list all users who follow them. From the list, the user should be able to select a follower and see more information about the follower including the number of tweets, the number of users being followed, the number of followers and up to 3 most recent tweets. The user should be given the option to follow the selected user or see more tweets.
from datetime import datetime
    
#function to display ID and Name of the users who follow the logged in user
def list_followers(conn, user_id):
    # Create a cursor
    cursor = conn.cursor()
    #join users and follows to get name of followers (and ID)
    cursor.execute("""
        SELECT u.usr, u.name
    FROM follows f
    JOIN users u ON f.flwer = u.usr
    WHERE f.flwee = ?
    """, (user_id,))
    followers = cursor.fetchall()

    if not followers:
        print("You have no followers.")
    else:
        #display name and ID
        print(" Followers:")
        for follower in followers:
            user_id, name = follower
            print(f"- Name: {name}  User ID: {user_id}")
    
        while True:
            try:
                #give users option to see more info on followers
                seemore = input("For more information on followers Enter '0', Enter '1' to see your followers again and press any other key to exit: ")

                #invalid choice
                if seemore !='0' and seemore !='1':
                    break
                
                #incase lots of information, allow them to view followers again
                elif seemore =='1':
                    print(" Followers:")
                    for follower in followers:
                        user_id, name = follower
                        print(f"- Name: {name}  User ID: {user_id}")

                #otherwise what user do they want to see more on 
                elif seemore == '0':
                    user_to_check  = int(input('Enter the Id of your follower that you want to view more information on: '))
                 
                    if user_to_check in [follower[0] for follower in followers]:
                        get_follower_info(conn, user_to_check)

                        nextChoice= input("'0' to follow user, '1' to view more tweets: ")
                        if nextChoice == '0':
                      # Check if the user is already following the selected user
                            cursor.execute("SELECT * FROM follows WHERE flwer = ? AND flwee = ?", (user_id,user_to_check))

                            existing_follow = cursor.fetchone()

                            if existing_follow:
                                print("You are already following this user.")
                            else:
                            # Insert a new follow record
                                cursor.execute("INSERT INTO follows VALUES (?, ?, ?)", (user_id, user_to_check, datetime.now().strftime('%Y-%m-%d')))
                                print("You are now following this user.")
                                conn.commit()
                        elif nextChoice == '1':
                            print_tweets(conn, user_to_check) 
                    else:
                        print("Invalid follower ID.")
            except ValueError:
                print("Invalid input. Please Try again.")
                continue



# find and display info for slected follower
def get_follower_info(conn,user_to_check):
    cursor = conn.cursor()

    #Display User ID and Name
    cursor.execute("""
                            SELECT * 
                             FROM users
                             WHERE usr = ?
                         """, (user_to_check,))
    follower_info = cursor.fetchone()

    #when there is data, print name and ID and follwing details   
    if follower_info:
        print(f"More information about {follower_info[2]} (User ID: {follower_info[0]})")
    else:
        print("Follower not found.")

    #Number of followers 
    cursor.execute("SELECT COUNT(*) FROM follows WHERE flwer = ?", (user_to_check,))
    following_count = cursor.fetchone()[0]
    if following_count:
        print(f"Number of Followers {following_count}")
    else:
        print("User has no Followers")

    #Number of tweets

    cursor.execute("SELECT COUNT(*) FROM tweets WHERE writer = ?",(user_to_check,))

    tweet_count = cursor.fetchone()[0]

    if  tweet_count:
        print(f"Number of Tweets {tweet_count}")
    else:
        print("User has no Tweets.")


    #Three most recent tweets 
    cursor.execute("""
        SELECT tid, writer, tdate, text
        FROM tweets
        WHERE writer = ?
        ORDER BY tdate DESC
        Limit 3

    """, (user_to_check,))
    recent_tweets = cursor.fetchall()

    if  recent_tweets:
        print("Recent Tweets:")
        for tweet in recent_tweets:
            print(f"  Text: {tweet[3]}")

def print_tweets(conn, user_to_check):
    cursor = conn.cursor()
    #use limit and offset to print next tweets (besides first three)
    cursor.execute("""
        SELECT tid, writer, tdate, text
        FROM tweets
        WHERE writer = ?
        ORDER BY tdate DESC
        Limit -1 OFFSET 3

    """, (user_to_check,))

    Alltweets = cursor.fetchall()

    if  Alltweets:
        print("More Tweets:")
        for tweet in Alltweets:
            print(f"- {tweet[3]}")
    else:
        print("User has no more tweets")



