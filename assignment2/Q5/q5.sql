/*
For every user who has a tweet such that the tweet is retweeted by 
at least three of the user's followers, 
list the id of the user, the date, the time, and the text of the tweet.
*/

SELECT t.writer, t.tdate, t.ttime, t.text
FROM tweets t, retweets r, follows f
WHERE 
    t.writer = f.flwee AND r.retweeter = f.flwer AND 
    r.writer = t.writer AND r.tdate = t.tdate AND r.ttime = t.ttime

GROUP BY t.writer, t.tdate, t.ttime, t.text
HAVING count(DISTINCT f.flwer) >= 3;
