
import sqlite3 as sq
import pprint
import sys
import datetime as dt
import getpass

conn = None
c = None

def connect(path):
    global conn, c
    conn = sq.connect(path)
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    conn.commit()
    return

def signup():
    #user input for account creation
    name = input("Enter your name: ")
    #check if email is valid: emails should have @ and period (.)
    while True:
        email = input("Enter your email: ")
        if "@" not in email or "." not in email:
            print("Invalid email. Please enter a valid email")
        else:
            break

    phone = input("Enter your phone number: ")
    password = getpass.getpass("Enter your password: ") #password non-visible at time of typing

    # name = 'Taran' 
    # email = 'tpurewal@ualberta.ca' 
    # phone = '780-123-4567' 
    # password = 'this works' 

    rec_sql = 'SELECT * FROM users u ORDER BY u.usr DESC' 
    c.execute(rec_sql)
    record = c.fetchone()
    if record:
        user_id = record[0] + 1 #assign (largest user ID + 1) to new user
    else:
        user_id = 1    

    #insert new user into users table
    ins_sql = 'INSERT INTO users (usr, name, email, phone, pwd) VALUES (?, ?, ?, ?, ?)'
    c.execute(ins_sql, (user_id, name, email, phone, password))
    conn.commit()

    print("Signup successful. Your user ID is "+ str(user_id) + "\n")
    actions(user_id)

def login():
    #user input for login information
    user_id = input("Enter user ID: ")
    password = getpass.getpass("Enter password: ") #password non-visible at time of typing
    # uid = 4
    # password = "pass1"

    #check if user is in the database, with correct password
    c.execute(f'SELECT * FROM users u WHERE u.usr == ? AND u.pwd == ?', (user_id, password))
    record = c.fetchone()
   
    if record is not None:
        print("Logged in Successfully!\n") #go to actions screen
        actions(record[0]) #record[0] is the user ID
    else:
        print("Login failed! \n") #back to login screen

#ACTION 1: Tweet Search
def tweet_search(usr):
    print("**** Tweet Search ****")
    # get a list of keywords (comma seperated) from user input
    keywords = input("Enter keywords: ")
    keyword_list = keywords.split(',')

    #retrieve tweets that contain the keywords
    searched_tweets = get_searched_tweets(keyword_list)

    #no tweets found
    if len(searched_tweets) == 0:
        print("No tweets match your search.")
        return

    start_index = 0

    while True:
        print("--Tweets found--")
        tweet_count = print_5_rows(searched_tweets, start_index, True)

        #options: select tweet, show more tweets, back
        print("1-" + str(tweet_count) + ".Select Tweet")
        print("6.Back")
        if start_index < len(searched_tweets) - 5:
            print("7.Show More Tweets")
        print()

        #user input to select option
        try:
            ch = int(input("Enter your choice: "))
        except:
            print("Please select one of the options")
            continue
        if ch >= 1 and ch <= tweet_count:
            select_tweet(usr, searched_tweets[start_index + ch - 1][1])
        elif ch == 6:  #back to actions screen
            print()
            return 
        elif ch == 7 and start_index < len(searched_tweets) - 5:
            start_index += 5
        else:
            print("Please select one of the options")
        print()
        
def get_searched_tweets(keyword_list):
    #format: type (tweet or retweet), tid, date, time, text

    t_sql = ""
    params = []
    for keyword in keyword_list:
        if t_sql != "":
            t_sql += " union\n"
        # if keyword is a hashtag, search for tweets with that hashtag
        if keyword[0] == "#" and len(keyword) > 1:
            t_sql += """
                SELECT 'tweet' AS type, t.tid, t.tdate, t.ttime, t.text, 0 AS spam
                FROM hashtag_mentions hm
                JOIN tweets t ON hm.tid = t.tid
                WHERE LOWER(hm.term) = ?
            """
            params.append(keyword.lower())
        else: # find tweets with text containing keyword
            t_sql += """
                SELECT 'tweet' AS type, tid, tdate, ttime, text, 0 AS spam
                FROM tweets
                WHERE LOWER(text) LIKE ? OR
                      LOWER(text) LIKE ? OR
                      LOWER(text) LIKE ? OR
                      LOWER(text) LIKE ?
            """
            params.append(keyword.lower() + ' %')          # Keyword is first word
            params.append('% ' + keyword.lower() + ' %')   # Keyword is in the middle
            params.append('% ' + keyword.lower())          # Keyword is last word
            params.append(keyword.lower())                 # Keyword is only word
            
    t_sql += "\n order by tdate desc, ttime desc;"

    c.execute(t_sql, params)
    searched_tweets = c.fetchall()

    return searched_tweets

def select_tweet(uid, tid):
    #get retweet count, reply count 
    c.execute('SELECT COUNT(*) FROM retweets WHERE tid = ?;', (tid,))
    retweet_cnt = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM tweets WHERE replyto_tid = ?;', (tid,))
    reply_cnt = c.fetchone()[0]

    #get tweet information
    print(f"**** Tweet {tid} selected ****")
    print("Retweets:", retweet_cnt, ", Replies:", reply_cnt, "\n")

    #options: reply, retweet, back
    while True:
        #list options to user
        print("1. Reply to Tweet")
        print("2. Retweet")
        print("3. Back")

        #user input to select option
        try:
            ch = int(input("Enter your choice: "))
        except:
            print("Please select one of the options")
            continue
        if ch == 1: #Reply to tweet
            send_tweet(uid, tid)
        elif ch == 2: #Retweet
            retweet(uid, tid)
        elif ch == 3: #back to follower list
            return
        else: 
            print("Please select one of the options")
        print()

def retweet(uid, tid):
    #check if user has already retweeted the tweet
    # (can only retweet once because of unique constraint on (tid, retweeter_id) in retweets table)
    c.execute('SELECT * FROM retweets WHERE tid = ? AND retweeter_id = ?;', (tid, uid))
    if c.fetchone() is not None:
        print("You have already retweeted this tweet")
        return
    #get writer of the tweet to be retweeted
    c.execute('SELECT writer_id FROM tweets WHERE tid = ?;', (tid,))
    writer_id = c.fetchone()[0]
    #insert retweet into retweets table
    c.execute('INSERT INTO retweets VALUES (?, ?, ?, 0, date("now"));', (tid, uid, writer_id))
    conn.commit()
    print("Retweeted successfully")

#ACTION 2: User Search
def user_search(usr):
    print("**** User Search ****")
    #get keyword from user input
    keyword = input("Enter keyword: ").lower()

    #retrieve all users with name containing keyword, ordered by length ascending
    c.execute('''
        SELECT usr, name
        FROM users
        WHERE LOWER(name) LIKE '%' || LOWER(?) || '%'
        ORDER BY LENGTH(name) ASC;
    ''', (keyword,))
    users_list = c.fetchall()

    #no users found
    if len(users_list) == 0:
        print("No users match your search.")
        return
    
    #options: select a user, list more followers, back
    start_index = 0
    while True:
        print("--Users found--")
        # Display followers starting from the current start_index
        users_count = print_5_rows(users_list, start_index, numbered=True)
        print()
        #options: select tweet, show more tweets, back
        print("1-" + str(users_count) + ".Select User")
        print("6.Back to Home")
        if start_index < len(users_list) - 5:
            print("7.Show More Users")
        print()
        
        #user input to select option
        try:
            ch = int(input("Enter your choice: "))
        except:
            print("Please select one of the options")
            continue
        if ch >= 1 and ch <= users_count:
            select_user(usr, users_list[start_index + ch - 1][0])
        elif ch == 6:  #back to actions screen
            print()
            return 
        elif ch == 7 and start_index < len(users_list) - 5:
            start_index += 5
        else:
            print("Please select one of the options")
        print()
 
def select_user(u1, u2):
    #u1: user logged in, u2: user selected
    #get tweet count, following count, follower count of a user
    c.execute('SELECT COUNT(*) FROM tweets WHERE writer_id = ?;', (u2,))
    tweet_cnt = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM follows WHERE flwer = ?;', (u2,))
    following_cnt = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM follows WHERE flwee = ?;', (u2,))
    follower_cnt = c.fetchone()[0]

    #get tweets of a user ordered by date and time of tweet descending
    c.execute('SELECT "tweet" as type, t.tid, t.tdate, t.ttime, t.text, 0 as spam FROM tweets t WHERE writer_id = ? ORDER BY tdate DESC, ttime DESC;', (u2,))
    tweets_list = c.fetchall()

    #print user information
    print(f"**** User {u2} selected ****")
    print("Tweets:", tweet_cnt, ", Following:", following_cnt, ", Followers:", follower_cnt)
    
    #print tweets of a user (3 if more than 3)
    print_5_rows(tweets_list[:min(3, len(tweets_list))], 0, numbered=False)
    tweet_index = min(3, len(tweets_list))-1 #index of last tweet printed

    #options: follow user, see more tweets, back to follower list
    while True:
        print()
        #list options to user
        print("1. Follow User")
        if tweet_index < len(tweets_list)-1:
            print("2. See More Tweets")
        print("3. Back")

        #user input to select option
        try:
            ch = int(input("Enter your choice: "))
        except:
            print("Please select one of the options")
            continue
        if ch == 1: #follow user
            follow_user(u1, u2)
        elif ch == 2 and tweet_index < len(tweets_list)-1: #see more tweets if there are more
            tweet_index += print_3_rows(tweets_list, tweet_index+1, numbered=False)
        elif ch == 3: #back to follower list
            return
        else: 
            print("Please select one of the options")
        print()

def follow_user(u1, u2):
    #check if u1 is already following u2
    c.execute('SELECT * FROM follows WHERE flwer = ? and flwee = ?;', (u1, u2))
    if c.fetchone() is not None:
        print("You are already following this user")
        return
    #follow user if not already following
    c.execute('INSERT INTO follows VALUES (?, ?, date("now"));', (u1, u2))
    conn.commit()
    print(f"Followed user {u2} successfully")

#ACTION 3: Send Tweet
def send_tweet(usr, replyto_tid=None):
    #get tweet text from user input
    tweet_text = input("Enter tweet: ")

    tweet_list = tweet_text.split()  #list of words in the tweet
    hashtag_list = []                #list of hashtags in the tweet

    for word in tweet_list:
        word = word.lower()
        if word[0] == "#" and len(word) > 1:
            if word in hashtag_list:
                print("Invalid tweet. No repeat hashtags.")
                return
            hashtag_list.append(word)

    rec_sql = 'SELECT * FROM tweets t ORDER BY t.tid DESC'
    c.execute(rec_sql)
    record = c.fetchone()
    tweet_id = record[0] + 1   #assign new tweet with tid = (largest tweet ID + 1) 

    #set tweet date and time to current date and time
    tweet_date = dt.datetime.now().strftime('%Y-%m-%d')
    tweet_time = dt.datetime.now().strftime('%X')

    #insert tweet into tweets table
    ins_sql = 'INSERT INTO tweets (tid, writer_id, text, tdate, ttime, replyto_tid) VALUES (?, ?, ?, ?, ?, ?)'
    c.execute(ins_sql, (tweet_id, usr, tweet_text, tweet_date, tweet_time, replyto_tid))
    conn.commit()

    #insert hashtags into hashtag_mentions table
    for hashtag in hashtag_list:
        ins_sql = 'INSERT INTO hashtag_mentions (tid, term) VALUES (?, ?)'
        c.execute(ins_sql, (tweet_id, hashtag))
        conn.commit()

    if replyto_tid is None:
        print("Tweet successful!")
    else:
        print("Reply successful!")
    print()
    
#ACTION 4: List Followers
def follower_list(usr):
    #get list of (id, name) of followers of a user
    c.execute('''
        SELECT u.usr, u.name 
        FROM users u, follows f 
        WHERE flwee = ? and u.usr = f.flwer;
        ''', (usr,)
    )
    flwer_list = c.fetchall()

    #no followers 
    if len(flwer_list) == 0:
        print("You have 0 followers.")
        return

    #options: select a follower, list more followers, back
    start_index = 0
    while True:
        print("**** Followers ****\n")
        # Display followers starting from the current start_index
        flwer_count = print_5_rows(flwer_list, start_index, numbered=True)

        #options: select tweet, show more tweets, back
        print("1-" + str(flwer_count) + ".Select Follower")
        print("6.Back to Home")
        if start_index < len(flwer_list) - 5:
            print("7.Show More Followers")
        print()
        
        #user input to select option
        try:
            ch = int(input("Enter your choice: "))
        except:
            print("Please select one of the options")
            continue
        if ch >= 1 and ch <= flwer_count:
            select_user(usr, flwer_list[start_index + ch - 1][0])
        elif ch == 6:  #back to actions screen
            print()
            return 
        elif ch == 7 and start_index < len(flwer_list) - 5:
            start_index += 5
        else:
            print("Please select one of the options")
        print()

def print_5_rows(table, start_index, numbered=False):
    # Prints at most 5 rows from table starting at start_index.
    # Returns the number of rows printed.
    # table: (type list) a table to be printed, 5 rows at a time, as a list of tuples.
    # start_index: (type int) the index to begin printing from.
    # numbered: (type bool) if True, the rows will be printed with a number 1-5 
    # at the beginning of the line.

    if not table: return 0 # table is empty
    current = start_index
    i = 0

    # Print headers
    if len(table[0]) == 2:  # user (usr, name)
        headers = ["User ID", "Name"]
        print("{:<10} {:<20}".format(*headers))
        print("-" * 30)
    elif len(table[0]) == 6:  # tweet/retweet (type, tid, trdate, ttime, text, spam)
        headers = ["Type", "Tweet ID", "Date", "Time", "Text", "Spam"]
        print("{:<10} {:<10} {:<12} {:<8} {:<50} {:<5}".format(*headers))
        print("-" * 100)

    while current < len(table) and i < 5:
        if numbered:
            print(str(i+1) + ".", end="")
        row = table[current]
        if len(row) == 2:  # user (usr, name)
            print("{:<10} {:<20}".format(row[0], row[1]))
        elif len(row) == 6:  # tweet/retweet (type, tid, trdate, ttime, text, spam)
            spam = "Spam" if row[5] else ""
            print("{:<10} {:<10} {:<12} {:<8} {:<50} {:<5}".format(row[0], row[1], row[2], row[3], row[4], spam))
        
        current += 1
        i += 1

    return i

def print_3_rows(table, start_index, numbered=False):
    # Prints at most 3 rows from table starting at start_index.
    # Returns the number of rows printed.
    # table: (type list) a table to be printed, 3 rows at a time, as a list of tuples.
    # start_index: (type int) the index to begin printing from.
    # numbered: (type bool) if True, the rows will be printed with a number 1-3 
    # at the beginning of the line.

    if not table: return 0 # table is empty
    current = start_index
    i = 0

    # Print headers
    if len(table[0]) == 2:  # user (usr, name)
        headers = ["User ID", "Name"]
        print("{:<10} {:<20}".format(*headers))
        print("-" * 30)
    elif len(table[0]) == 6:  # tweet/retweet (type, tid, trdate, ttime, text, spam)
        headers = ["Type", "Tweet ID", "Date", "Time", "Text", "Spam"]
        print("{:<10} {:<10} {:<12} {:<8} {:<50} {:<5}".format(*headers))
        print("-" * 100)

    while current < len(table) and i < 3:
        if numbered:
            print(str(i+1) + ".", end="")
        row = table[current]
        if len(row) == 2:  # user (usr, name)
            print("{:<10} {:<20}".format(row[0], row[1]))
        elif len(row) == 6:  # tweet/retweet (type, tid, trdate, ttime, text, spam)
            spam = "Spam" if row[5] else ""
            print("{:<10} {:<10} {:<12} {:<8} {:<50} {:<5}".format(row[0], row[1], row[2], row[3], row[4], spam))
        
        current += 1
        i += 1

    return i

def get_flwer_tweets(usr):
    #format: type (tweet or retweet), tid, date, time, text
    t_sql = """
        with rt as
        (select *
        from retweets r join tweets t using (tid)),

        flwers as 
        (select flwee from follows
        where flwer = ?)

        SELECT "tweet" as type, tid, tdate, ttime, text, 0 as spam
        FROM tweets t
        WHERE t.writer_id in flwers

        union

        SELECT "retweet" as type, tid, tdate, ttime, text, spam
        FROM rt 
        where rt.retweeter_id in flwers
        ORDER BY tdate DESC, ttime DESC
    """
    c.execute(t_sql, (usr,))
    tweets = c.fetchall()
    
    return tweets

def actions(usr):
    #successful login from login() or signup()
    #list tweets and retweets of followed users
    start_index = 0
    
    #loop for the 5 user actions
    while True:

        tweets = get_flwer_tweets(usr) 

        print("**** Home Screen ****")
        print_5_rows(tweets, start_index)
        print()
        print("1.Tweet Search")
        print("2.User Search")
        print("3.Send Tweet")
        print("4.List Followers")
        print("5.Log Out")

        #option to print more tweets of followed users if there are more
        if start_index < len(tweets) - 5:
            print("6.Show More Tweets")
        #option to go back to top of the list of tweets
        if start_index > 0:
            print("7.Back to Top")
        print()

        #user input to select action
        try:
            ch = int(input("Enter your choice: "))
        except:
            print("Please select one of the options")
            continue
        if ch == 1:
            tweet_search(usr)
        elif ch == 2:
            user_search(usr)
        elif ch == 3:
            send_tweet(usr)
        elif ch == 4:
            follower_list(usr)
        elif ch == 5:
            print("\nLogged out successfully")
            return
        elif ch == 6 and start_index < len(tweets) - 5:
            start_index += 5
        elif ch == 7 and start_index > 0:
            start_index = 0
        else:
            print("Please select one of the options")
        print()

def main():
    #connect to the database file from command line argument
    path = sys.argv[1] #NOTE: uncomment for final version
    #path = 'test.db' # for testing
    connect(path)

    print("\nWelcome to Twitter!\n")
    #loop for login screen
    while True:
        print("********** Login System **********")
        print("1.Signup")
        print("2.Login")
        print("3.Exit")
        print()
        try:
            ch = int(input("Enter your choice: "))
        except:
            print("Please select one of the options")
            continue
        if ch == 1:
            print()
            signup()
        elif ch == 2:
            print()
            login()
        elif ch == 3:
            print("Exiting...")
            print("Goodbye!")
            break
        else:
            print("Please select one of the options")
    
    conn.close()

if __name__ == '__main__':
    main()
