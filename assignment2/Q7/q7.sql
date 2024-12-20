/*
Find the lists that include more than 3 tweets, 
such that at least 50% of the tweets have been retweeted. 
For each such list, return the list name and the owner. 
Hint: You may find common table expressions and subqueries in the FROM clause helpful.
*/


--lists with more than 3 tweets
SELECT lname, owner
FROM includes
GROUP BY lname
HAVING count(*)>3

INTERSECT

--lists where at least 50% of tweets have been retweeted
SELECT i.lname, i.owner
FROM 
    includes i left join retweets r
    ON i.writer = r.writer AND i.tdate = r.tdate AND i.ttime = r.ttime
GROUP BY i.lname
HAVING count(r.retweeter)/count(*) >= 0.5;
