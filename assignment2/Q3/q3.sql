/*
Find the id of users who have at least three different tweets that mention Edmonton 
in tweet text but have no followers. The match for Edmonton is case-insensitive.
*/

SELECT t1.writer
FROM tweets t1, tweets t2, tweets t3
WHERE 
    --same user
    t1.writer = t2.writer AND t1.writer = t3.writer AND t2.writer = t3.writer AND
    --all 3 tweets mention edmonton
    lower(t1.text) LIKE '%edmonton%' AND lower(t2.text) LIKE '%edmonton%' AND lower(t3.text) LIKE '%edmonton%' AND
    --all 3 texts are different
    t1.text <> t2.text AND t1.text <> t3.text AND t2.text <> t3.text 

EXCEPT

--users who have followers (followees)
SELECT flwee
FROM follows;


--test queries

-- select t.writer, t.text
-- from(
--     select writer, count(*)
--     from tweets
--     group by writer
--     having count(*) >=3
--     ) s, tweets t
-- where s.writer = t.writer AND lower(t.text) like '%edmonton%';

-- select count(*) 
-- from follows f, (
--     select t.writer, t.text
--     from(
--         select writer, count(*)
--         from tweets
--         group by writer
--         having count(*) >=3
--         ) s, tweets t
--     where s.writer = t.writer AND lower(t.text) like '%edmonton%'
-- ) u
-- where f.flwee = u.writer
-- group by u.writer;



