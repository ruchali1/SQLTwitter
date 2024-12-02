import datetime 
from compose_tweet import compose_tweet

# Display tweets from followed users
def display_tweets_and_retweets(conn,user_id):
    while True:
            try:
                #allow users to choose to see tweets or retweets
                TorR= input("Enter '1' to see Tweets and '2' to see retweets, Enter any other key to exit to Main Menu: ")

                if TorR !='1' and TorR !='2':
                    break
                elif TorR =='1':
                    display_tweets(conn, user_id)
                elif TorR =='2':
                    display_retweets(conn, user_id)
            except ValueError:
                print("Invalid input. Please Try again.")
                break
            
# Function to find and display tweets of the followers the logged in user follows
def display_tweets(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""
            SELECT t.tid, t.writer, t.tdate, t.text, t.replyto
            FROM tweets AS t
            WHERE t.writer IN (
                SELECT flwee
                FROM follows
                WHERE flwer = ?
            )
            ORDER BY t.tdate DESC

        """, (user_id,))
    tweets = cursor.fetchall()
    #paginate tweets. 5 per page
    tweet_ids = [tweet[0] for tweet in tweets]
    total_tweets = len(tweets)
    page = 1
    tweets_per_page = 5
    while True:
        #quit if no tweets
        if not tweets:
            print("No tweets to display.")
            return
        start_index = (page - 1) * tweets_per_page
        end_index = start_index + tweets_per_page
        displayed_tweets = tweets[start_index:end_index]

        #display tweet info
        for tweet in displayed_tweets:
            print(f"Tweet ID: {tweet[0]}")
            print(f"Writer: {tweet[1]}")
            print(f"Date: {tweet[2]}")
            print(f"Text: {tweet[3]}")
            print(f"Reply To: {tweet[4]}\n")
          
        #prompt for next page
        response = input("Do you want to see more tweets? (yes/no), Any other key will return you to the previous menu: ")
        if response.lower() != 'yes':
            break

        elif response.lower() == 'yes':
            if end_index < total_tweets:
                page += 1
            else:
                print("No more tweets.")
                break
    #quit at invalid choice
    if response.lower() != 'yes' and response.lower() != 'no':
        return
    else:
        #allow user to see more information on tweets, reply to them or retweet them 
        response2 = input("Do you want to see more information on any of these tweets, or reply or retweet any? (yes/no), press any other key to reach exit menu: ")
        if response2.lower() == 'yes':
            tweetId = int(input("Enter the ID of the tweet you want more information on: "))
            if tweetId in tweet_ids:
                get_info(conn, tweetId)
                action = input("If you want to retweet this tweet, enter retweet, if you want to reply to it enter reply, if you want to exit enter any other key: ")
                if action.lower() != 'retweet' and action.lower() != 'reply' :
                    return
                elif action.lower() == 'retweet':
                    cursor.execute("SELECT * FROM retweets WHERE usr = ? AND tid = ?", (user_id, tweetId))
                    existing_retweet = cursor.fetchone()

                    if existing_retweet:
                        print("You have already retweeted this tweet")
                    else:
                        retweet(conn,tweetId,user_id)
                elif action.lower() == 'reply':
                    tweet_text= input("Enter you reply text: ")
                    replyto = tweetId
                    #insert tweet id into replyto of tweets table, call compose tweets
                    compose_tweet(conn, user_id, tweet_text, replyto)
                    print("Sucessfully replied")

            else:
                print("Invalid ID.")
                return
        
#Function to find and display retweets of the followers the logged in user follows
def display_retweets(conn,user_id):
    cursor = conn.cursor()
    #create limit and offset to siplay 5 tweets at a time
    offset = 0 
    limit = 5
    while True:
        cursor.execute("""
            SELECT r.usr, r.tid, r.rdate
            FROM retweets AS r
            WHERE r.usr IN (
                SELECT flwee
                FROM follows
                WHERE flwer = ?
            )
            ORDER BY r.rdate DESC
            LIMIT  ? OFFSET ?
        """, (user_id,limit,offset))
        retweets = cursor.fetchall()

        if not retweets:
            print("No retweets to display.")
            break

        for retweet in retweets:
            print(f"Writer of Retweet: {retweet[0]}")
            print(f"ID of tweet: {retweet[1]}")
            print(f"Retweet date: {retweet[2]}")
            

        response = input("Do you want to see more retweets? (yes/no): ")
        if response.lower() != 'yes':
            break
        #next 5 when response is yes
        offset += limit


#get more information on tweets to display when asked by user
def get_info(conn, tweetId):
    cursor = conn.cursor()

    #Number of tweets

    cursor.execute("SELECT COUNT(*) FROM retweets WHERE tid= ?",(tweetId,))

    retweet_count = cursor.fetchone()[0]

    if  retweet_count:
        print(f"Number of retweets for Tweet {tweetId} is {retweet_count}")
    else:
        print("tweet has no retweets.")

    #Number of replies


    cursor.execute("SELECT COUNT(*) FROM tweets WHERE replyto= ?",(tweetId,))

    reply_count = cursor.fetchone()[0]

    if  reply_count:
        print(f"Number of replies for Tweet {tweetId} is {reply_count}")
    else:
        print("tweet has no replies.")



#rewtweet slected tweet, insert into retweets table
def retweet(conn,tweetId, user_id):
    cursor=conn.cursor()
    rdate = datetime.datetime.now().strftime('%Y-%m-%d') 
    cursor.execute("INSERT INTO retweets (usr, tid, rdate) VALUES (?, ?, ?)", (user_id, tweetId, rdate))
    print(f"Sucesfully retweeted Tweet {tweetId}" )
    conn.commit()
    return
