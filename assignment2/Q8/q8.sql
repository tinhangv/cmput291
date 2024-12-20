/*
For each month in 2024 where there was a tweet or reply, 
find 
    the total number of tweets with null in their reply fields, 
    the total number of replies (i.e. tweets where the reply field is not null), 
    the total number of retweets and 
    the sum of those three quantities. 
Hint: you may find outer join useful for this and some of the subsequent queries. You may also find common table expressions useful.
*/


WITH 
u AS (
    --count of [tweets or replies] in each month of 2024 (replies are tweets with non-null reply fields)
    SELECT strftime('%m', t.tdate) month, count(*)-count(t.replyto_w) num_null_replies, count(t.replyto_w) num_replies
    FROM tweets t
    WHERE strftime('%Y', t.tdate) = '2024'
    GROUP BY month
), v AS(
    --count of retweets made in each month of 2024
    SELECT strftime('%m', r.rdate) month, count(*) rcount
    FROM retweets r
    WHERE strftime('%Y', r.rdate) = '2024' 
    GROUP BY month
) 
SELECT u.month, u.num_null_replies, u.num_replies, coalesce(v.rcount,0), u.num_null_replies + u.num_replies + coalesce(v.rcount,0)
FROM u LEFT JOIN v USING (month)
GROUP BY u.month;


--TEST CODE 

--tweets in 2024
-- SELECT * FROM tweets t
-- WHERE strftime('%Y', t.tdate) = '2024'
-- ORDER BY strftime('%m', t.tdate);

--retweets in 2024
-- SELECT * FROM  retweets r
-- WHERE strftime('%Y', r.rdate) = '2024'
-- ORDER BY strftime('%m', r.rdate);