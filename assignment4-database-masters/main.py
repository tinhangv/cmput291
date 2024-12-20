from pymongo import MongoClient
import sys
from pprint import pprint
from datetime import datetime

# 1: Tweet Search
def tweetSearch(col):
    print("\n**** Tweet Search ****")

    # get a list of keywords (comma seperated) from user input
    keywords = input("Enter keywords: ")
    keyword_list = keywords.split(',')
    results = []
    seen_ids = set()

    # find tweets matching keywords
    for word in keyword_list:
        for rgx in (f'\\b#?{word}\\b', f'^#?{word}\\b', f'\\b#?{word}$', f'^#?{word}$'):
            matches = col.find({"content": {"$regex": rgx, "$options": "im"}},
                                {"_id":1, "id":1, "date":1, "content":1, "user":1})
            for tweet in matches:
                if tweet['_id'] not in seen_ids:
                    seen_ids.add(tweet['_id'])
                    results.append(tweet)

    print()
    if(len(results) == 0):
        print("No tweets found.")
    else:
        show_tweet_fields(results, col)

# 2: User Search
def userSearch(col):
    print("\n**** User Search ****")
    # get a keyword from the user
    keyword = input("Enter a keyword to search users: ")
    results = []

    for rgx in (f'\\b{keyword}\\b', f'^{keyword}\\b', f'\\b{keyword}$', f'^{keyword}$'):
        # search for all users whose displayname or location contain the keyword
        # exclude the id in the user field result and only include the user field
        results += col.find({"$or": [{"user.displayname": {"$regex": rgx, "$options": "i"}},
                                    {"user.location": {"$regex": rgx, "$options": "i"}}]
                            }, {"_id": 0, "user": 1})
        
    # remove duplicates from the search and display unique users only 
    unique_users = {}
    for user in results:
        unique_users[user["user"]["username"]] = user["user"]
    users = unique_users.values()
    listed_users = list(users)

    print()
    if len(listed_users) == 0:
        print("No users found.")
    else: show_user_fields(listed_users, col)
    

# 3: List Top Tweets
def listTopTweets(col):
    print("\n**** List Top Tweets ****")

    # get field to sort by from user input
    while True:
        print("Select which field to sort by:")
        print("1: Retweet Count")
        print("2: Like Count")
        print("3: Quote Count")
        choice = input('Choice: ')
        if choice == '1':
            field = "retweetCount"
            break
        elif choice == '2':
            field = "likeCount"
            break
        elif choice == '3':
            field = "quoteCount"
            break
        else:
            print("Invalid choice. Please select a number between 1 and 3.")

    n = getN("\nEnter number of tweets to list: ")
    
    # find specefied number of tweets sorted by specefied field
    results = col.aggregate([
        {"$sort": {
            field: -1
        }},
        {"$limit": n}
    ])

    # prepare list of tweets for displaying
    results_list = []

    for tweet in results:
        results_list.append(tweet)

    print()

    show_tweet_fields(results_list, col)

# 4: List Top Users
def listTopUsers(col):
    print("\n**** List Top Users ****")

    # get top n users by tweet count
    n = getN("\nEnter number of users to list: ")

    # find specefied number of users sorted by followersCount
    results = col.aggregate([
        {"$group": {
            "_id": "$user.id",
            "followersCount": {"$max": "$user.followersCount"}
        }},
        {"$sort": {
            "followersCount": -1
        }},
        {"$limit": n}
    ])

    # prepare list of users for displaying
    results_list = []

    for user in results:
        u = col.find_one({"user.id": user["_id"]})
        results_list.append(u["user"])

    print()

    show_user_fields(results_list, col)

    
def getN(message):
    # helper function to get a positive integer from user input
    while True:
        try:
            n = int(input(message))
            if n > 0:
                return n
            else:
                print("Invalid input. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def show_tweet_fields(results, col):
    # For each tweet in results, displays the id, date, content, 
    # and username of the person who posted it.
    # Allows the user to select a tweet and see all fields.
    # results: (type list) A list of tweet objects (as dictionaries)

    for item in results:
        item.pop("_id", None)
    # print required tweet fields
    for i in range(1, len(results)+1):
        tweet = results[i-1]
        if tweet.get("date"):
            try:
                date_obj = datetime.fromisoformat(tweet["date"])
                formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError: formatted_date = tweet["date"]
        else:
            formatted_date = "N/A"
        print(f"Tweet {i} || id: {tweet['id']}, date: {formatted_date}, content: {tweet['content']}, username: {tweet['user']['username']}\n")
    
    # handle user input to see more fields or go back
    while True:
        print("Select 1 of the following options")
        if len(results) > 0:
            print(f"1-{len(results)}: print full tweet data")
        print(f"{len(results)+1}: Back")
        choice = getN("Enter your choice: ")
        if 1 <= choice <= len(results):
            selected_tweet = results[choice - 1]
            print("\nAll fields of the selected tweet:")
            print(selected_tweet)
        elif choice == (len(results)+1):
            break
        else:
            print(f"Invalid choice. Please select a number between 1 and {len(results)}.")

    
def show_user_fields(results, col):
    # For each user in results, displays the  username, displayname, and followersCount.
    # results must not have duplicates.
    # Allows the user to select a user and see all fields.
    # results: (type list) A list of user objects (as dictionaries)

    # print required tweet fields
    for i in range(1, len(results)+1):
        user = results[i-1]
        location = user.get("location")
        print(f"User {i} || username: {user['username']}, displayname: {user['displayname']},followersCount: {user['followersCount']}, location: {location}")
    
    # handle user input to see more fields or go back
    while True:
        print("Select 1 of the following options")
        if len(results) > 0:
            print(f"1-{len(results)}: print full user data")
        print(f"{len(results)+1}: Back")
        choice = getN("Enter your choice: ")
        if 1 <= choice <= len(results):
            selected_user = results[choice - 1]
            print("\nAll fields of the selected user:")
            print(selected_user)
        elif choice == (len(results)+1):
            break
        else:
            print(f"Invalid choice. Please select a number between 1 and {len(results)}.")


# 5: Compose Tweet
def composeTweet(col):

    print("\n**** Compose Tweet ****")

    # get tweet content from user input
    content = input("Enter tweet content: ")

    # insert tweet into database
    # date field: system date, username: "291user", all other fields null
    tweet = {
        "url": None,
        "date": datetime.now().isoformat(),
        "content": content,
        "renderedContent": content,
        "id": None,
        "user": {
            "username": "291user",
            "displayname": None,
            "id": None,
            "description": None,
            "rawDescription": None,
            "descriptionUrls": None,
            "verified": None,
            "created": None,
            "followersCount": None,
            "friendsCount": None,
            "statusesCount": None,
            "favouritesCount": None,
            "listedCount": None,
            "mediaCount": None,
            "location": None,
            "protected": None,
            "linkUrl": None,
            "linkTcourl": None,
            "profileImageUrl": None,
            "profileBannerUrl": None,
            "url": None
        },
        "outlinks": None,
        "tcooutlinks": None,
        "replyCount": None,
        "retweetCount": None,
        "likeCount": None,
        "quoteCount": None,
        "conversationId": None,
        "lang": None,
        "source": None,
        "sourceUrl": None,
        "sourceLabel": None,
        "media": None,
        "retweetedTweet": None,
        "quotedTweet": None,
        "mentionedUsers": None
    }
    col.insert_one(tweet)
    print("Tweet successfully posted.")

def main():
    
    #get mongodb server port number from cmd line args
    port = sys.argv[1] 

    #connect to database
    client = MongoClient(f"mongodb://localhost:{port}/")
    db = client['291db']
    col = db["tweets"]

    #loop for main menu
    print("Welcome to twitter")
    while True:
        print("\nPlease select 1 of the following options:")
        print("1: Tweet Search")
        print("2: User Search")
        print("3: List Top Tweets")
        print("4: List Top Users")
        print("5: Compose Tweet")
        print("6: Exit")
        choice = input('Choice: ')

        if choice == '1':
            tweetSearch(col)
        elif choice == '2':
            userSearch(col)
        elif choice == '3':
            listTopTweets(col)
        elif choice == '4':
            listTopUsers(col)
        elif choice == '5':
            composeTweet(col)
        elif choice == '6':
            print("Exiting program.")
            break

if __name__ == '__main__':
    main()
