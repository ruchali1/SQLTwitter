Use 1: In user.py get_unique_user_id was created by the help of ChatGpt (https://chat.openai.com/)

Input:
 heres my code to register a user
    def register_user(conn):
    # Create a cursor
    cursor = conn.cursor()

    user_id = input("Enter a username: ")
    user_id = get_unique_user_id(cursor)
    password = getpass.getpass("Enter a password: ")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    city = input("Enter your city: ")
    timezone = input("Enter your timezone: "), 
    
    note the user_id is a primary key in my sql database,
    how can i make it so The user id (i.e. the field usr in table users) 
    should be provided by the system and be unique and is a simple integer.

Output:
    def get_unique_user_id(cursor):
    cursor.execute("SELECT MAX(user_id) FROM users")
    max_id = cursor.fetchone()[0]
    if max_id is not None:
        return max_id + 1
    else:
        return 1  # If there are no existing users, start with user ID 1

    In this modified version, 
    the get_unique_user_id function queries the database to find the maximum existing user ID 
    and then increments it by 1 to get the new unique user ID. 
    This ensures that the user IDs are unique and not repeated in the database.

END of Use 1

Use 2: Populate Database; help of ChatGpt (https://chat.openai.com/)


Input: 
```write me an sql file to populate this database 
drop table if exists includes;
drop table if exists lists;
drop table if exists retweets;
drop table if exists mentions;
drop table if exists hashtags;
drop table if exists tweets;
drop table if exists follows;
drop table if exists users;

create table users (
  usr         int,
  pwd	      text,
  name        text,
  email       text,
  city        text,
  timezone    float,
  primary key (usr)
);
create table follows (
  flwer       int,
  flwee       int,
  start_date  date,
  primary key (flwer,flwee),
  foreign key (flwer) references users,
  foreign key (flwee) references users
);
create table tweets (
  tid	      int,
  writer      int,
  tdate       date,
  text        text,
  replyto     int,
  primary key (tid),
  foreign key (writer) references users,
  foreign key (replyto) references tweets
);
create table hashtags (
  term        text,
  primary key (term)
);
create table mentions (
  tid         int,
  term        text,
  primary key (tid,term),
  foreign key (tid) references tweets,
  foreign key (term) references hashtags
);
create table retweets (
  usr         int,
  tid         int,
  rdate       date,
  primary key (usr,tid),
  foreign key (usr) references users,
  foreign key (tid) references tweets
);
create table lists (
  lname        text,
  owner        int,
  primary key (lname),
  foreign key (owner) references users
);
create table includes (
  lname       text,
  member      int,
  primary key (lname,member),
  foreign key (lname) references lists,
  foreign key (member) references users
)

Output:
-- Sample data for the 'users' table
INSERT INTO users (usr, pwd, name, email, city, timezone)
VALUES
  (1, 'password1', 'User1', 'user1@example.com', 'City1', -5.0),
  (2, 'password2', 'User2', 'user2@example.com', 'City2', 3.5),
  (3, 'password3', 'User3', 'user3@example.com', 'City3', 0.0),
  (4, 'password4', 'User4', 'user4@example.com', 'City4', -7.0),
  (5, 'password5', 'User5', 'user5@example.com', 'City5', 1.0),
  (6, 'password6', 'User6', 'user6@example.com', 'City6', -2.5),
  (7, 'password7', 'User7', 'user7@example.com', 'City7', 5.5),
  (8, 'password8', 'User8', 'user8@example.com', 'City8', -4.0),
  (9, 'password9', 'User9', 'user9@example.com', 'City9', 2.5),
  (10, 'password10', 'User10', 'user10@example.com', 'City10', 6.0);

-- Sample data for the 'follows' table
INSERT INTO follows (flwer, flwee, start_date)
VALUES
  (1, 2, '2023-01-01'),
  (2, 3, '2023-02-01'),
  (3, 1, '2023-03-01'),
  (4, 1, '2023-04-01'),
  (5, 3, '2023-05-01'),
  (6, 2, '2023-06-01'),
  (7, 4, '2023-07-01'),
  (8, 5, '2023-08-01'),
  (9, 6, '2023-09-01'),
  (10, 7, '2023-10-01');

-- Sample data for the 'tweets' table
INSERT INTO tweets (tid, writer, tdate, text, replyto)
VALUES
  (1, 1, '2023-01-05', 'This is a sample tweet.', NULL),
  (2, 2, '2023-01-06', 'Another tweet here.', 1),
  (3, 3, '2023-01-07', 'Replying to tweet 1.', 1),
  (4, 4, '2023-01-08', 'Tweet from user 4.', NULL),
  (5, 5, '2023-01-09', 'A tweet from user 5.', 2),
  (6, 6, '2023-01-10', 'Tweeting away.', NULL),
  (7, 7, '2023-01-11', 'Hello, Twitter!', 1),
  (8, 8, '2023-01-12', 'Tweeting some more.', 4),
  (9, 9, '2023-01-13', 'User 9's tweet.', 2),
  (10, 10, '2023-01-14', '10th tweet in the list.', 3);

-- Sample data for the 'hashtags' table
INSERT INTO hashtags (term)
VALUES
  ('#sample'),
  ('#example'),
  ('#test'),
  ('#socialmedia'),
  ('#data'),
  ('#programming'),
  ('#fun'),
  ('#followback'),
  ('#travel'),
  ('#food');

-- Sample data for the 'mentions' table
INSERT INTO mentions (tid, term)
VALUES
  (1, '#sample'),
  (2, '#example'),
  (3, '#test'),
  (4, '#socialmedia'),
  (5, '#data'),
  (6, '#programming'),
  (7, '#fun'),
  (8, '#followback'),
  (9, '#travel'),
  (10, '#food');

-- Sample data for the 'retweets' table
INSERT INTO retweets (usr, tid, rdate)
VALUES
  (1, 2, '2023-01-10'),
  (2, 3, '2023-01-11'),
  (3, 1, '2023-01-12'),
  (4, 5, '2023-01-13'),
  (5, 4, '2023-01-14'),
  (6, 7, '2023-01-15'),
  (7, 6, '2023-01-16'),
  (8, 10, '2023-01-17'),
  (9, 8, '2023-01-18'),
  (10, 9, '2023-01-19');

-- Sample data for the 'lists' table
INSERT INTO lists (lname, owner)
VALUES
  ('Sample List 1', 1),
  ('Sample List 2', 2),
  ('Sample List 3', 3),
  ('Sample List 4', 4),
  ('Sample List 5', 5),
  ('Sample List 6', 6),
  ('Sample List 7', 7),
  ('Sample List 8', 8),
  ('Sample List 9', 9),
  ('Sample List 10', 10);

-- Sample data for the 'includes' table
INSERT INTO includes (lname, member)
VALUES
  ('Sample List 1', 2),
  ('Sample List 2', 3),
  ('Sample List 3', 1),
  ('Sample List 4', 4),
  ('Sample List 5', 5),
  ('Sample List 6', 6),
  ('Sample List 7', 7),
  ('Sample List 8', 8),
  ('Sample List 9', 9),
  ('Sample List 10', 10);```

Action: After receiving this repsonse, we alterted the hashtag and mentions tbale to fit requirements. 

End of use 2
