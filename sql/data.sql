PRAGMA foreign_keys = ON;

INSERT INTO users(username, fullname, email, password)
VALUES ('awdeorio', 'Andrew DeOrio', 'awdeorio@umich.edu', 
        'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO users(username, fullname, email, password)
VALUES ('jflinn', 'Jason Flinn', 'jflinn@umich.edu', 
        'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'  );

INSERT INTO users(username, fullname, email, password)
VALUES ('michjc', 'Michael Cafarella', 'michjc@umich.edu',
'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO users(username, fullname, email, password)
VALUES ('jag', 'H.V. Jagadish', 'jag@umich.edu', 
'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');



INSERT INTO posts(postid, filename, owner)
VALUES (1, 'fire.jpg', 'awdeorio');

INSERT INTO posts(postid, filename, owner)
VALUES (2, 'fire.jpg', 'jflinn');
 
INSERT INTO posts(postid, filename, owner)
VALUES (3, 'fire.jpg', 'awdeorio');

INSERT INTO posts(postid, filename, owner)
VALUES (4, 'fire.jpg', 'jag');



INSERT INTO comments(commentid, owner, postid, text)
VALUES (1, 'awdeorio', 3, 'do you need help?'); 

INSERT INTO comments(commentid, owner, postid, text)
VALUES (2, 'jflinn', 3, 'sending over some support right now!');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (3, 'michjc', 3, 'hope you are okay');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (4, 'awdeorio', 2, 'reach out if you need anything!');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (5, 'jflinn', 1, 'my friend lives nearby, she will come help');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (6, 'awdeorio', 1, 'I did not know this was happening so close by');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (7, 'jag', 4, 'Im so sorry');


