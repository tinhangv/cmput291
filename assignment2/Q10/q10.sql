/*
Using the view created in the previous question, find the id of top users in terms of 
(1) the number of followers, and 
(2) the number of times their tweets are retweeted on average. 
Indicate those users with 'top in followers' and 'top in retweets'.
*/

--tStat (writer, tdate, ttime, text, rep_cnt, ret_cnt, sim_cnt)


WITH 
RankedUserFlwers AS (
    SELECT f.flwee, RANK() OVER (ORDER BY COUNT(*) DESC) AS rank
    FROM follows f
    GROUP BY f.flwee
),
AveRetCnt AS(
    --average times retweeted
    SELECT writer, AVG(ret_cnt) ave_rets
    FROM (
        --times retweeted
        SELECT t.writer, ret_cnt
        FROM tStat t
        GROUP BY t.writer, t.tdate, t.ttime, t.text
        )
    GROUP BY writer
)
--top in followers
SELECT flwee, "top in followers"
FROM RankedUserFlwers
WHERE rank = 1

UNION

--top in average retweet times
SELECT writer, "top in retweets"
FROM AveRetCnt
WHERE ave_rets = (SELECT max(ave_rets) FROM AveRetCnt);




