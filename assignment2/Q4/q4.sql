/*
Find the id and name of users who have no tweets 
and follow every user followed by John Doe. T
he match for John Doe should be case-insensitive.
*/

--users who have no tweets = users not in {users who have tweets}
SELECT u.usr, u.name
FROM users u
WHERE 
    u.usr  NOT IN (
        SELECT writer
        FROM tweets
    ) 
INTERSECT

--users who follows every user followed by JD 
--division
--B = all users followed by JD
--A = all users followed by a particular user u1
-- output u1 if B-A is empty (B is a subset of A)
SELECT u1.usr, u1.name
FROM users u1
WHERE NOT EXISTS(
    SELECT f1.flwee
    FROM follows f1, users u2
    WHERE f1.flwer = u2.usr AND lower(u2.name) = 'john doe'

    EXCEPT 

    SELECT f2.flwee 
    FROM follows f2
    WHERE f2.flwer = u1.usr 
);


--TEST CODE
-- --every user followed by JD
-- SELECT f.flwee
-- FROM follows f, users u2
-- WHERE f.flwer = u2.usr AND lower(u2.name) = 'john doe';

-- --follower who follows all users followed by JD
-- select flwer from follows where flwee = 2
-- intersect 
-- select flwer from follows where flwee = 18
-- intersect
-- select flwer from follows where flwee = 29;
