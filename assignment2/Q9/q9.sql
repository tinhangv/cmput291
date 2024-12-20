/*
Create a view called tStat with columns writer, tdate, ttime, text, rep_cnt, ret_cnt, and sim_cnt; 
the view would include 
for every tweet, 
    the id of the writer, tdate, ttime, text, 
    the number of replies, the number of retweets and the number of tweets that mention the same hashtag mentioned in the tweet. 
Note: To pass github tests, please insert "select * from tStat" after creating your query.
*/

CREATE VIEW tStat (writer, tdate, ttime, text, rep_cnt, ret_cnt, sim_cnt) AS
    SELECT t.writer, t.tdate, t.ttime, t.text, coalesce(t1.rep_cnt,0), coalesce(t2.ret_cnt,0), coalesce(t3.sim_cnt,0)
    FROM 
        --get every tweet
        (SELECT t.writer, t.tdate, t.ttime, t.text 
        FROM tweets t) t

        LEFT JOIN
            --get number of replies (tweets replying to this tweet)
            (SELECT t.writer, t.tdate, t.ttime, t.text, count(*) as rep_cnt
            FROM tweets t, tweets rep
            WHERE (t.writer, t.tdate, t.ttime) = (rep.replyto_w, rep.replyto_d, rep.replyto_t)
            GROUP BY t.writer, t.tdate, t.ttime) t1
            ON (t.writer, t.tdate, t.ttime, t.text) = (t1.writer, t1.tdate, t1.ttime, t1.text)

        LEFT JOIN
            --get number of retweets
            (SELECT t.writer, t.tdate, t.ttime, t.text, count(*) as ret_cnt
            FROM tweets t, retweets r
            WHERE t.writer = r.writer AND t.tdate = r.tdate AND t.ttime = r.ttime
            GROUP BY t.writer, t.tdate, t.ttime) t2
            ON (t.writer, t.tdate, t.ttime, t.text) = (t2.writer, t2.tdate, t2.ttime, t2.text)

        LEFT JOIN
            --get number of tweets mentioning the same hashtag
            (SELECT t.writer, t.tdate, t.ttime, t.text, count(*) as sim_cnt
            FROM tweets t, tweets m, hashtags h
            WHERE 
                --both t and m mention the same hashtag
                t.mention_has = h.term AND m.mention_has = h.term
            GROUP BY t.writer, t.tdate, t.ttime) t3
            ON (t.writer, t.tdate, t.ttime, t.text) = (t3.writer, t3.tdate, t3.ttime, t3.text)
    ORDER BY t.writer;

SELECT * FROM tStat;