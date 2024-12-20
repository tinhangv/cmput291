/*
Find the top 3 tweets with the largest number of retweets. 
In case of ties, return all ties. 
For each tweet, return the id of the writer, the date, the time, and the text of the tweet. 
*/

WITH RankedTweets AS (
    SELECT t.writer, t.tdate, t.ttime, t.text,
           RANK() OVER (ORDER BY COUNT(*) DESC) AS rank
    FROM tweets t, retweets r
    WHERE t.writer = r.writer AND t.tdate = r.tdate AND t.ttime = r.ttime
    GROUP BY t.writer, t.tdate, t.ttime, t.text
),
TopRankedTweets AS (
    SELECT writer, tdate, ttime, text, rank
    FROM RankedTweets
    WHERE 
        rank = 1 OR
        (rank = 2 AND (SELECT COUNT(*) FROM RankedTweets WHERE rank = 1) < 3) OR
        (rank = 3 AND (SELECT COUNT(*) FROM RankedTweets WHERE rank = 1)
            + (SELECT COUNT(*) FROM RankedTweets WHERE rank = 2) < 3)
)

SELECT writer, tdate, ttime, text
FROM TopRankedTweets
ORDER BY rank;


-- --all retweets grouped, and their counts
-- SELECT writer, tdate, ttime, count(*) as rcount
-- FROM retweets
-- GROUP BY writer, tdate, ttime
-- ORDER BY count(*) DESC;

