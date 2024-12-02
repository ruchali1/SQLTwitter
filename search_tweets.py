from datetime import datetime
from compose_tweet import *  # Import necessary functions from other modules
from display_tweets import retweet

# Search for tweets
def search_tweets(conn, user_id, keywords):
    cursor = conn.cursor()
    keyword_list = keywords.split()  # Split the space-separated keywords into a list

    # Remove any empty or whitespace-only keywords
    keyword_list = [keyword for keyword in keyword_list if keyword.strip()]

    # If there are no valid keywords, print a message and return
    if not keyword_list:
        print("No valid keywords provided. Please enter keywords to search.")
        return

    # Create a placeholder for the WHERE clause conditions
    conditions = []

    # Create a list of parameters to pass to the execute method
    params = []

    # Iterate through the keywords and add conditions for each one
    for keyword in keyword_list:
        # Add a condition for the keyword appearing in the tweet text
        conditions.append("(t.text LIKE ?)")

        # Add a condition for the keyword appearing as a mention
        conditions.append("(t.tid IN (SELECT tid FROM mentions WHERE term = ?))")

        # Add the keyword with '%' as a wildcard for SQL LIKE
        params.extend(['%' + keyword + '%', keyword])

    # Join the conditions with OR to combine them
    where_clause = " OR ".join(conditions)

    cursor.execute(f"""
        SELECT DISTINCT t.tid, t.writer, t.tdate, t.text, t.replyto
        FROM tweets AS t
        WHERE 
        ({where_clause})
        ORDER BY t.tdate DESC
    """, params)
    
    tweets = cursor.fetchall()

    if not tweets:
        print("No matching tweets found.")
        return

    display_tweet_list(conn, user_id, tweets)

def display_tweet_list(conn, user_id, tweets):
    count = 5
    for i in range(0, min(5, len(tweets))):
        tweet = tweets[i]
        print(f"{i + 1}. Tweet ID: {tweet[0]}")
        print(f"   Writer: {tweet[1]}")
        print(f"   Date: {tweet[2]}")
        print(f"   Text: {tweet[3]}")
        print(f"   Reply To: {tweet[4]}\n")
    while True:
        choice = input("Enter the number of a tweet to see more information, '0' to view more, or 'back' to go back: ")

        if choice == '0':
            if count >= len(tweets):
                print("No more tweets to display.")
                return

            for i in range(count, min(count + 5, len(tweets))):
                tweet = tweets[i]
                print(f"{i + 1}. Tweet ID: {tweet[0]}")
                print(f"   Writer: {tweet[1]}")
                print(f"   Date: {tweet[2]}")
                print(f"   Text: {tweet[3]}")
                print(f"   Reply To: {tweet[4]}\n")

            count += 5

        elif choice == 'back':
            return
        elif choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(tweets):
                selected_tweet = tweets[index]
                display_tweet_info(conn, user_id, selected_tweet)
            else:
                print("Invalid tweet number. Please try again.")
        else:
            print("Invalid choice. Please try again.")

def display_tweet_info(conn, user_id, tweet):
    cursor = conn.cursor()
    tid = tweet[0]

    # Count retweets by checking the retweets table
    cursor.execute("SELECT COUNT(*) FROM retweets WHERE tid = ?", (tid,))
    retweet_count = cursor.fetchone()[0]

    # Count replies by checking the tweets table for tweets with the same text and the current tweet as their replyto
    cursor.execute("SELECT COUNT(*) FROM tweets WHERE replyto = ?", (tid,))
    reply_count = cursor.fetchone()[0]

    print(f"Tweet ID: {tweet[0]}")
    print(f"Writer: {tweet[1]}")
    print(f"Date: {tweet[2]}")
    print(f"Text: {tweet[3]}")
    print(f"Reply To: {tweet[4]}")
    print(f"Retweets: {retweet_count}")
    print(f"Replies: {reply_count}")

    while True:
        action = input("Enter 'R' to retweet, 'C' to compose a reply, or 'B' to go back: ").upper()

        if action == 'B':
            return
        elif action == 'R':
            cursor.execute("SELECT * FROM retweets WHERE usr = ? AND tid = ?", (user_id, tid))
            existing_retweet = cursor.fetchone()
            
            if existing_retweet:
                print("You have already retweeted this tweet")
            else:
                retweet(conn, tid, user_id)

        elif action == 'C':
            reply_text = input("Compose your reply: ")
            compose_tweet(conn, user_id, reply_text, tid)  # Include reply text and tid
