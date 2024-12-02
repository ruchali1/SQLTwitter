import sqlite3
import re
from datetime import datetime

def compose_tweet(conn, user_id, text, replyto):
    # Connect to the SQLite database
    cursor = conn.cursor()
    # Find hashtags
    hashtags = re.findall(r'(#\w+)', text)

    # Get ID of new tweet
    tweet_id = get_unique_tweet_id(cursor)

    # Insert tweet
    cursor.execute("INSERT INTO tweets (tid, writer, tdate, text,replyto) VALUES (?, ?, ?, ?,?)", (tweet_id, user_id, datetime.now().strftime('%Y-%m-%d'), text, replyto))
    conn.commit()

    # Insert mentions
    for hashtag in hashtags:
        hashtag=hashtag[1:]
        # Check if already exists
        cursor.execute("SELECT term FROM hashtags WHERE term = ?", (hashtag,))
        existing_hashtag = cursor.fetchone()

        if existing_hashtag is None:
            # insert into table
            cursor.execute("INSERT INTO hashtags (term) VALUES (?)", (hashtag,))

        # Insert mention
        cursor.execute("INSERT INTO mentions (tid, term) VALUES (?, ?)", (tweet_id, hashtag))
    print("Sucesfully Tweeted")
    conn.commit()

def get_unique_tweet_id(cursor):
    cursor.execute("SELECT MAX(tid) FROM tweets")
    max_id = cursor.fetchone()[0]
    if max_id is not None:
        return max_id + 1
    else:
        return 1  # If there are no existing users, start with user ID 1