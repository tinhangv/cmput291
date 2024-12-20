/* Find the id of users who have at least 1 follower, 
and at least 1 tweet included in a favorites list.
*/

--users with at least 1 follower
SELECT flwee
FROM follows

INTERSECT

--users with at least 1 tweet in someone's favorites list
SELECT writer
FROM includes;


