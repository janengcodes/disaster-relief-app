PRAGMA foreign_keys = ON;

INSERT INTO users(username, fullname, email, password)
VALUES ('johnny_appleseed', 'Johnny Appleseed', 'japple@gmail.com', 
        'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO users(username, fullname, email, password)
VALUES ('gravity', 'Jason Halo', 'jhalo@yahoo.com', 
        'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'  );

INSERT INTO users(username, fullname, email, password)
VALUES ('ralph_l', 'Ralph Lauren', 'ralphlauren@rll.com',
'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO users(username, fullname, email, password)
VALUES ('kimmy', 'Kim Davenport', 'kimkim@hello.com', 
'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO users(username, fullname, email, password)
VALUES ('shania_twain', 'Shania Twain', 'shatwain@music.com', 
'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');


INSERT INTO posts(postid, filename, owner)
VALUES (1, 'clothing_drive.jpeg', 'johnny_appleseed');

INSERT INTO posts(postid, filename, owner)
VALUES (2, 'food_drive.jpeg', 'gravity');
 
INSERT INTO posts(postid, filename, owner)
VALUES (3, 'shelter.png', 'johnny_appleseed');

INSERT INTO posts(postid, filename, owner)
VALUES (4, 'volunteers.png', 'kimmy');



INSERT INTO comments(commentid, owner, postid, text)
VALUES (1, 'kimmy', 3, 'thank you for sharing!'); 

INSERT INTO comments(commentid, owner, postid, text)
VALUES (2, 'gravity', 3, 'hope everyone can get what they need');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (3, 'shania_twain', 3, 'this is really helpful');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (4, 'johnny_appleseed', 2, 'is there anything left?');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (5, 'kimmy', 1, 'where is this?');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (6, 'kimmy', 1, 'I did not know this was happening so close by');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (7, 'kimmy', 4, 'Volunteers needed!');


