PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE tStat (
    writer      int,
    tdate       date,
    ttime       time,
    text        text,
    rep_cnt     int,
    ret_cnt     int,
    sim_cnt     int
);
INSERT INTO tStat VALUES(3,'2024-05-12','07:30:25','I love Edmonton',0,0,0);
INSERT INTO tStat VALUES(3,'2024-05-14','12:55:32','GOOOO oilers',0,0,0);
INSERT INTO tStat VALUES(5,'2024-03-01','17:45:22','Go oliers!',0,0,0);
INSERT INTO tStat VALUES(5,'2024-06-01','14:25:33','Looking for a good book to read. Just finished lone #survivor',0,0,1);
INSERT INTO tStat VALUES(5,'2024-07-01','10:10:11','Summer vibes. #vacation',4,1,1);
INSERT INTO tStat VALUES(5,'2024-08-25','18:30:07','Beach day with friends. #beach',0,0,3);
INSERT INTO tStat VALUES(5,'2024-09-08','13:50:55','Learning a new language. #language',0,0,1);
INSERT INTO tStat VALUES(5,'2024-09-20','12:55:27','Trying out a new recipe. #cooking',0,0,3);
INSERT INTO tStat VALUES(5,'2024-11-02','15:30:56','Cooking up a storm in the kitchen! #foodie',0,1,3);
INSERT INTO tStat VALUES(5,'2024-12-18','14:45:50','Baking holiday cookies. #baking',0,1,0);
INSERT INTO tStat VALUES(5,'2024-12-31','23:59:59','New Years Eve celebration. #newyear',0,1,1);
INSERT INTO tStat VALUES(10,'2024-03-10','18:30:12','Happy to be part of the #survivor fan club.',0,1,0);
INSERT INTO tStat VALUES(10,'2024-08-05','09:20:53','Attending a music concert. #music',0,0,1);
INSERT INTO tStat VALUES(10,'2024-08-15','10:35:17','Sightseeing in a new city. #travel',0,0,2);
INSERT INTO tStat VALUES(10,'2024-09-18','15:11:39','Visiting an art exhibition. #art',0,0,2);
INSERT INTO tStat VALUES(10,'2024-10-10','17:45:08','Celebrating a friends birthday. #party',5,1,1);
INSERT INTO tStat VALUES(10,'2024-11-28','16:05:42','Working on a new project. #work',0,0,1);
INSERT INTO tStat VALUES(10,'2024-11-30','23:15:18','Late-night coding session. #programming',0,2,1);
INSERT INTO tStat VALUES(29,'2024-07-20','09:37:13','Great workout session at the gym! #fitness',0,2,1);
INSERT INTO tStat VALUES(29,'2024-09-02','12:15:29','Spending the day at the zoo. #animals',0,0,2);
INSERT INTO tStat VALUES(29,'2024-09-12','11:33:17','Weekend getaway in the mountains. #nature',0,0,0);
INSERT INTO tStat VALUES(29,'2024-10-10','08:40:18','Sunday morning yoga. #yoga',0,3,1);
INSERT INTO tStat VALUES(29,'2024-10-22','14:35:47','Exploring a new hiking trail. #outdoors',0,0,3);
INSERT INTO tStat VALUES(29,'2024-11-05','10:22:10','Sunday brunch with family. #familytime',0,0,1);
INSERT INTO tStat VALUES(29,'2024-11-11','08:14:55','Just finished reading a great book. #reading',0,0,1);
INSERT INTO tStat VALUES(42,'2024-06-15','12:03:19','Enjoying a great hockey game! #oilers',1,1,2);
INSERT INTO tStat VALUES(42,'2024-08-10','12:05:14','Summer road trip. #adventure',0,0,0);
INSERT INTO tStat VALUES(42,'2024-09-05','11:27:50','Watching the sunset by the beach. #relaxation',5,0,2);
INSERT INTO tStat VALUES(42,'2024-10-15','13:05:01','Coffee date with friends. #coffee',0,0,1);
INSERT INTO tStat VALUES(42,'2024-10-20','19:00:55','Attending a Halloween costume party. #halloween',0,0,0);
INSERT INTO tStat VALUES(42,'2024-11-05','11:55:02','Cooking Thanksgiving dinner. #thanksgiving',0,1,1);
INSERT INTO tStat VALUES(42,'2024-11-15','09:05:42','#cozy',0,0,1);
INSERT INTO tStat VALUES(42,'2024-12-01','18:55:28','Getting ready for the holiday season. #holidays',0,0,1);
INSERT INTO tStat VALUES(42,'2024-12-25','12:25:14','Merry Christmas to all! #holiday',1,0,1);
INSERT INTO tStat VALUES(55,'2024-04-05','08:47:59','Just visited beautiful #Edmonton.',0,1,0);
INSERT INTO tStat VALUES(55,'2024-07-02','19:45:12','Picnic by the lake. #relaxation',0,0,2);
INSERT INTO tStat VALUES(55,'2024-07-10','21:45:22','Stargazing night. #stargazing',0,0,1);
INSERT INTO tStat VALUES(55,'2024-09-15','07:32:44','Bird-watching in the park. #nature',0,1,3);
INSERT INTO tStat VALUES(55,'2024-09-22','14:20:45','Hiking in the mountains. #nature',0,0,3);
INSERT INTO tStat VALUES(55,'2024-09-30','07:40:48','Early morning run. #fitness',0,0,2);
INSERT INTO tStat VALUES(55,'2024-10-05','11:50:22','Gardening day! #gardening',0,0,1);
INSERT INTO tStat VALUES(97,'2024-02-12','09:10:45','Edmonton #Oilers had a good game last night.',1,1,2);
INSERT INTO tStat VALUES(97,'2024-07-08','14:45:20','Trying out a new restaurant. #foodie',0,2,0);
INSERT INTO tStat VALUES(97,'2024-08-15','16:18:41','Exploring the city today. #adventure',4,0,1);
INSERT INTO tStat VALUES(97,'2024-11-02','18:20:11','Relaxing by the fireplace. #cozy',0,0,1);
INSERT INTO tStat VALUES(97,'2024-11-15','10:45:30','Studying for exams. #studentlife',0,2,0);
INSERT INTO tStat VALUES(97,'2024-11-18','19:45:30','Movie night with friends. #movienight',0,0,1);
INSERT INTO tStat VALUES(97,'2024-12-05','17:10:38','Attending a holiday charity event. #charity',0,0,1);
INSERT INTO tStat VALUES(97,'2024-12-12','10:40:32','Sunday relaxation time. #chill',2,0,1);
INSERT INTO tStat VALUES(97,'2024-12-18','10:25:35','Baking holiday cookies. #baking',0,0,1);
INSERT INTO tStat VALUES(101,'2024-02-13','14:59:08','#Edmonton #Oilers had a good game last night.',0,0,0);
INSERT INTO tStat VALUES(101,'2024-02-15','09:20:40','#Edmonton #Oilers go oilers',0,0,0);
INSERT INTO tStat VALUES(101,'2024-02-16','16:35:21','#Edmonton #Oilers we will be champion',0,3,0);
INSERT INTO tStat VALUES(107,'2024-02-17','11:15:37','#Edmonton #Oilers we will be champion',0,0,0);
INSERT INTO tStat VALUES(107,'2024-02-18','13:24:06','#Edmonton #Oilers oilers for ever',0,0,0);
INSERT INTO tStat VALUES(107,'2024-02-19','15:52:44','#Edmonton #Oilers go oilers go',0,0,0);
COMMIT;
