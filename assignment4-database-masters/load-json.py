import sys
import json
from pymongo import MongoClient

def load_json(json_file, port):

    client = MongoClient(f"mongodb://localhost:{port}/")
    db = client['291db']
    batch_size = 5000

    if 'tweets' in db.list_collection_names():
        db['tweets'].drop()

    collection = db['tweets']
    
    batch = []
    with open(json_file, 'r') as file:
        #process each line to avoid loading the entire JSON file into memory
        for line in file:
            tweet = json.loads(line.strip())
            batch.append(tweet)

            if len(batch) >= batch_size:
                collection.insert_many(batch)
                batch.clear()

        #insert any remaining tweets which are less than the batch size
        if len(batch) > 0:
            collection.insert_many(batch)
    
    print(f"Database loaded.")
    

if __name__ == '__main__':
    #get json file name, mongodb server port number from cmd line args
    json_file = sys.argv[1]
    port = sys.argv[2]
    # Load JSON file
    load_json(json_file, port)

    pass
