#file to test out the implementation of action 4 before adding to main.py

import sqlite3 as sq
import pprint
conn = sq.connect("test2.db")
c = conn.cursor()
c.execute(' PRAGMA foreign_keys=ON; ')
conn.commit()

def print_5_rows(table, start_index, numbered=False):
    # Prints at most 5 rows from table starting at start_index.
    # Returns the number of rows printed.
    # table: (type list) a table to be printed, 5 rows at a time, as a list of tuples.
    # start_index: (type int) the index to begin printing from.
    # numbered: (type bool) if True, the rows will be printed with a number 1-5 
    # at the beginning of the line.

    current = start_index
    i = 0

    while current < len(table) and i < 5:
        if numbered:
            print(str(i+1) + ".", end="")   #NOTE: changed str(i) to str(i+1)
        pprint.pprint(table[current]) # pretty this up later
        current += 1
        i += 1

    return i

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
    c.execute('SELECT * FROM tweets WHERE writer_id = ? ORDER BY tdate DESC, ttime DESC;', (u2,))
    tweets_list = c.fetchall()

    #print user information
    print(f"**** User {u2} selected ****")
    print("Tweets:", tweet_cnt, ", Following:", following_cnt, ", Followers:", follower_cnt)
    
    #print tweets of a user (3 if more than 3)
    for i in range(min(3, len(tweets_list))):
        print(tweets_list[i])
    tweet_index = min(3, len(tweets_list))-1 #index of last tweet printed

    #options: follow user, see more tweets, back to follower list
    while True:
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
            for i in range(tweet_index+1, min(tweet_index+4, len(tweets_list))):
                print(tweets_list[i])
            tweet_index = i
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
    print(f"Followed user {u2} successfully")
            
if __name__ == '__main__':
    #select_user(1,3)
    follower_list(3)
    conn.close()