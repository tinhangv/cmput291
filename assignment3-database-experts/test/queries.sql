/*
sqlite3
.open test.db
*/

/* Home Screen
get_flwer_tweets(usr)
Get all tweets and retweets of followers
*/
WITH tr as (
    SELECT t.tid, t.writer_id, t.text, t.tdate, t.ttime, t.replyto_tid, r.rdate, r.retweeter_id
    FROM tweets t
    LEFT JOIN retweets r on t.tid == r.tid
),

dt as (
    SELECT tid, writer_id, text, tdate, 
    CASE WHEN COALESCE(tdate, '1/1/0001') > COALESCE(rdate, '1/1/0001') THEN tdate 
    ELSE rdate END AS trdate, ttime, replyto_tid, retweeter_id
    FROM tr
)

SELECT dt.text
FROM dt JOIN follows f ON f.flwee == dt.writer_id OR f.flwee == dt.retweeter_id
WHERE flwer == ?
ORDER BY trdate DESC

/* 1
get_searched_tweets(keyword_list)
retrieve all tweets containing the keyword
*/

--if the keyword is a hashtag
select tid, text 
from hashtag_mentions join tweets using (tid)
where lower(term) == lower(?)
union
--if the keyword is not a hashtag
select tid, text from tweets
where lower(text) like '%' || lower(?) || '%'

order by tdate desc;

/* 2
user_search()
retrieve all users with name containing the keyword
*/
SELECT usr, name
FROM users
WHERE LOWER(name) LIKE '%' || LOWER(?) || '%'
ORDER BY LENGTH(name) ASC;


/* 4
follower_list(usr)
Get (id, name) of all followers of a user
*/

SELECT u.usr, u.name 
FROM users u, follows f 
WHERE flwee = ? and u.usr = f.flwer;

/* 2,4
select_user(usr)
Get all information (#tweets, #following, #followers, tweets) of a user 
order by date and time of tweet descending (lastest to oldest)
*/

--get number of tweets of a user
SELECT COUNT(*) FROM tweets WHERE writer_id = ?;

--get number of following of a user
SELECT COUNT(*) FROM follows WHERE flwer = ?;

--get number of followers of a user
SELECT COUNT(*) FROM follows WHERE flwee = ?;

--get tweets of a user ordered by date and time of tweet descending
SELECT * FROM tweets WHERE writer_id = 1 ORDER BY tdate DESC, ttime DESC;

