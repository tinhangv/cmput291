-- Populate the users table
INSERT INTO users (usr, name, email, phone, pwd) VALUES
(1, 'Alice', 'alice@example.com', 1234567890, 'password123'),
(2, 'Bob', 'bob@example.com', 2345678901, 'securepass'),
(3, 'Charlie', 'charlie@example.com', 3456789012, 'charlie123'),
(4, 'Dana', 'dana@example.com', 4567890123, 'danapass'),
(5, 'Eve', 'eve@example.com', 5678901234, 'evepass'),
(6, 'Frank', 'frank@example.com', 6789012345, 'frankpass'),
(7, 'Grace', 'grace@example.com', 7890123456, 'gracepass'),
(8, 'Heidi', 'heidi@example.com', 8901234567, 'heidipass'),
(9, 'Ivan', 'ivan@example.com', 9012345678, 'ivanpass'),
(10, 'Judy', 'judy@example.com', 1234567809, 'judypass');

-- Populate the follows table
INSERT INTO follows (flwer, flwee, start_date) VALUES
(1, 2, '2024-01-01'),
--(1, 3, '2024-01-02'),
(2, 4, '2024-01-03'),
(3, 5, '2024-01-04'),
(4, 1, '2024-01-05'),
(5, 6, '2024-01-06'),
(7, 1, '2024-01-07'),
--(8, 3, '2024-01-08'),
(9, 4, '2024-01-09'),
(10, 5, '2024-01-10');

-- Populate the lists table
INSERT INTO lists (owner_id, lname) VALUES
(1, 'Favorites'),
(2, 'Tech Tweets'),
(3, 'Funny Tweets'),
(4, 'Inspirations'),
(5, 'Daily Reads'),
(6, 'Top Picks'),
(7, 'Motivation'),
(8, 'Jokes'),
(9, 'News'),
(10, 'Quotes');

-- Populate the tweets table with regular tweets and replies (hashtags stored directly in text)
INSERT INTO tweets (tid, writer_id, text, tdate, ttime, replyto_tid) VALUES
(101, 1, 'Hello World! #welcome', '2024-02-01', '12:00:00', NULL),
(102, 2, 'Happy to be here! #happy', '2024-02-02', '13:00:00', NULL),
(103, 3, 'Learning SQL! #learning #tech', '2024-02-03', '14:00:00', NULL),
(104, 4, 'This is a reply to tweet 1 #reply', '2024-02-04', '15:00:00', 101),
(105, 5, 'Another day in paradise #paradise', '2024-02-05', '16:00:00', NULL),
(106, 6, 'Replying to tweet 3 #reply #learning', '2024-02-06', '17:00:00', 103),
(107, 7, 'Good morning everyone! #morning', '2024-02-07', '18:00:00', NULL),
(108, 8, 'Starting a new project today #project', '2024-02-08', '19:00:00', NULL),
(109, 9, 'Big news coming soon! #news', '2024-02-09', '20:00:00', NULL),
(110, 10, 'Excited to learn SQL #sql', '2024-02-10', '21:00:00', NULL);

-- Populate hashtag_mentions table
INSERT INTO hashtag_mentions (tid, term) VALUES
(101, '#welcome'),
(102, '#happy'),
(103, '#learning'),
(103, '#tech'),
(104, '#reply'),
(105, '#paradise'),
(106, '#reply'),
(106, '#learning'),
(107, '#morning'),
(108, '#project'),
(109, '#news'),
(110, '#sql');

-- Populate retweets table
INSERT INTO retweets (tid, retweeter_id, writer_id, spam, rdate) VALUES
(101, 2, 1, 0, '2024-03-01'),
(102, 3, 2, 0, '2024-03-02'),
(103, 4, 3, 1, '2024-03-03'),
(105, 1, 5, 0, '2024-03-04'),
(106, 6, 6, 0, '2024-03-05'),
(107, 7, 7, 0, '2024-03-06'),
(108, 8, 8, 1, '2024-03-07'),
(109, 9, 9, 0, '2024-03-08'),
(110, 10, 10, 0, '2024-03-09');

-- Populate include table to add tweets to lists
INSERT INTO include (owner_id, lname, tid) VALUES
(1, 'Favorites', 101),
(2, 'Tech Tweets', 103),
(3, 'Funny Tweets', 105),
(4, 'Inspirations', 107),
(5, 'Daily Reads', 109),
(6, 'Top Picks', 102),
(7, 'Motivation', 106),
(8, 'Jokes', 104),
(9, 'News', 108),
(10, 'Quotes', 110);


-- Add 10 tweets for Alice (User 1)
INSERT INTO tweets (tid, writer_id, text, tdate, ttime, replyto_tid) VALUES
(116, 1, 'Excited to start the weekend!', '2024-02-16', '13:00:00', NULL),
(117, 1, 'Studying new programming techniques #programming', '2024-02-17', '14:00:00', NULL),
(118, 1, 'Had a great coding session today!', '2024-02-18', '15:00:00', NULL),
(119, 1, 'Just finished a new project', '2024-02-19', '16:00:00', NULL),
(120, 1, 'Taking a break to recharge', '2024-02-20', '17:00:00', NULL),
(121, 1, 'Catching up on my reading', '2024-02-21', '18:00:00', NULL),
(122, 1, 'Exploring new tech trends #techtrends', '2024-02-22', '19:00:00', NULL),
(123, 1, 'Working on a cool project', '2024-02-23', '20:00:00', NULL),
(124, 1, 'Taking a short break', '2024-02-24', '21:00:00', NULL),
(125, 1, 'Reflecting on goals and achievements', '2024-02-25', '22:00:00', NULL);

-- Add hashtags for Alice's tweets
INSERT INTO hashtag_mentions (tid, term) VALUES
(117, '#programming'),
(122, '#techtrends');

-- Add 12 tweets for Bob (User 2)
INSERT INTO tweets (tid, writer_id, text, tdate, ttime, replyto_tid) VALUES
(126, 2, 'Exploring new places today! #travel', '2024-02-21', '18:00:00', NULL),
(127, 2, 'Diving deeper into AI', '2024-02-22', '19:00:00', NULL),
(128, 2, 'Love working on tech projects #techlife', '2024-02-23', '20:00:00', NULL),
(129, 2, 'Taking a break for a snack', '2024-02-24', '21:00:00', NULL),
(130, 2, 'Coding is my happy place', '2024-02-25', '22:00:00', NULL),
(131, 2, 'Learning something new today! #education', '2024-02-26', '23:00:00', NULL),
(132, 2, 'Feeling inspired by new ideas', '2024-02-27', '09:00:00', NULL),
(133, 2, 'Late-night coding session #latenightcoding', '2024-02-28', '10:00:00', NULL),
(134, 2, 'Can''t wait to share my new project!', '2024-02-29', '11:00:00', NULL),
(135, 2, 'Taking a quick break from work', '2024-03-01', '12:00:00', NULL),
(136, 2, 'Improving my skills every day #selfimprovement', '2024-03-02', '13:00:00', NULL),
(137, 2, 'Just had a great brainstorming session', '2024-03-03', '14:00:00', NULL);

-- Add hashtags for Bob's tweets
INSERT INTO hashtag_mentions (tid, term) VALUES
(126, '#travel'),
(128, '#techlife'),
(131, '#education'),
(133, '#latenightcoding'),
(136, '#selfimprovement');

-- Add 7 followers to Charlie (usr = 3)
INSERT INTO follows (flwer, flwee, start_date) VALUES
(1, 3, '2024-03-01'),  -- Alice follows Charlie
(2, 3, '2024-03-02'),  -- Bob follows Charlie
(4, 3, '2024-03-03'),  -- Dana follows Charlie
(5, 3, '2024-03-04'),  -- Eve follows Charlie
(6, 3, '2024-03-05'),  -- Frank follows Charlie
(7, 3, '2024-03-06'),  -- Grace follows Charlie
(8, 3, '2024-03-07');  -- Heidi follows Charlie


