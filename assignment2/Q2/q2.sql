/*
Find the id of users who follow another user (say u2) for at least 90 days 
and that the other user u2 is followed by John Doe for less than 90 days. 
The matches for John Doe should be case-insensitive. 
Hint: Check out Date and Time functions in SQLite as well as built-in scalar functions in SQLite.
*/

--id's of users who follow another user for at least 90 days
SELECT f1.flwer
FROM follows f1, follows f2, users u
WHERE
    --user 1 followed by user 2 for at least 90 days
    julianday('now')-julianday(f1.start_date) >= 90 AND
    --user 2 participates in relation f2...
    f1.flwee = f2.flwee AND
    --with the flwer being john doe
    f2.flwer = u.usr AND lower(u.name) = 'john doe' AND
    --user 2 followed by john doe for less than 90 days
    julianday('now')-julianday(f2.start_date) <90;



