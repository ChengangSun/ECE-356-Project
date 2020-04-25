USE social_network;

INSERT INTO Users (alias, email, gender, password, birthDate, lastLoginDateTime, occupation)
  VALUES ('Bill', 'sopwith@icloud.com', 'Male', 'Bill1', '1990-01-01', now(), 'Dev'),
  ('Olivia', 'dwheeler@comcast.net', 'Male', 'Olivia1', '1987-11-11', now(), 'Teacher'),
  ('Amelia', 'godeke@outlook.com', 'Male', 'Amelia1', '1988-11-14', now(), 'Student'),
  ('Isla', 'ryanshaw@outlook.com', 'Female', 'Isla1', '1998-01-30', now(), 'Student'),
  ('George', 'papathan@sbcglobal.net', 'Female', 'George1', '1997-01-01', now(), 'Student'),
  ('Harry', 'thomasj@yahoo.ca', 'Male', 'Harry1', '1998-11-19', now(), 'Carpenter'),
  ('Ford', 'seemant@me.com', 'Female', 'Ford1', '1998-01-01', now(), 'Doctor');

INSERT INTO Topics (topicName) VALUES ('Politics'), ('American Politics'), ('Canadian Politics'), ('Food');
UPDATE Topics, (SELECT topicId FROM Topics WHERE topicName = 'Politics') as pol
  SET parentID = pol.topicID
  WHERE topicName IN ('American Politics', 'Canadian Politics');
  
INSERT INTO UserGroups (groupName, creatorID)
  VALUES ('School Club', (SELECT userID FROM Users WHERE alias = 'Olivia'));
INSERT INTO Members (groupID, userID, role)
  VALUES ((SELECT last_insert_id()), (SELECT userID FROM Users WHERE alias = 'Olivia'), 'Creator'),
  ((SELECT last_insert_id()), (SELECT userID FROM Users WHERE alias = 'Amelia'), 'Member'),
  ((SELECT last_insert_id()), (SELECT userID FROM Users WHERE alias = 'Isla'), 'Member'),
  ((SELECT last_insert_id()), (SELECT userID FROM Users WHERE alias = 'George'), 'Member');
  
INSERT INTO UserGroups (groupName, creatorID)
  VALUES ('Medical Group', (SELECT userID FROM Users WHERE alias = 'Ford'));
INSERT INTO Members (groupID, userID, role)
  VALUES ((SELECT last_insert_id()), (SELECT userID FROM Users WHERE alias = 'Ford'), 'Creator'),
  ((SELECT last_insert_id()), (SELECT userID FROM Users WHERE alias = 'Olivia'), 'Member'),
  ((SELECT last_insert_id()), (SELECT userID FROM Users WHERE alias = 'George'), 'Member');
  
INSERT INTO UserGroups (groupName, creatorID)
  VALUES ('Construction', (SELECT userID FROM Users WHERE alias = 'Harry'));
INSERT INTO Members (groupID, userID, role)
  VALUES ((SELECT last_insert_id()), (SELECT userID FROM Users WHERE alias = 'Harry'), 'Creator');
  
INSERT INTO FollowsTopic (userID, topicID)
  (SELECT userID, (SELECT topicID FROM Topics WHERE topicName = 'Food') as topicID FROM Users)
  UNION
  (SELECT userID, (SELECT topicID FROM Topics WHERE topicName = 'Politics') as topicID FROM Users WHERE occupation != 'Student')
  UNION
  (SELECT creatorID as userID, topicID FROM UserGroups JOIN Topics WHERE topicName = 'American Politics' OR topicName = 'Canadian Politics');

INSERT INTO FollowsUser (userID, targetUserID)
  (SELECT u1.userID, u2.userID as targetUserID FROM Users u1 JOIN Users u2 WHERE u1.occupation = 'Student' AND u2.occupation = 'Teacher')
  UNION
  (SELECT u1.userID, u2.userID as targetUserID FROM Users u1 JOIN Users u2 WHERE u1.occupation = 'Student' AND u2.occupation = 'Student' AND u1.userID != u2.userID);

INSERT INTO Posts (post, userID, topicID)
  VALUES ('Product arrived labeled as Jumbo Salted Peanuts...the peanuts were actually small sized unsalted. Not sure if this was an error or if the vendor intended to represent the product as "Jumbo".', 1, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('This is a confection that has been around a few centuries. It is a light, pillowy citrus gelatin with nuts - in this case Filberts. And it is cut into tiny squares and then liberally coated with powd...', 1, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('If you are looking for the secret ingredient in Robitussin I believe I have found it. I got this in addition to the Root Beer Extract I ordered (which was good) and made some cherry soda. The flavor...', 1, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('Great taffy at a great price. There was a wide assortment of yummy taffy. Delivery was very quick. If your a taffy lover, this is a deal.', 1, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('I got a wild hair for taffy and ordered this five pound bag. The taffy was all very enjoyable with many flavors: watermelon, root beer, melon, peppermint, grape, etc. My only complaint is there was a ...', 1, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('This saltwater taffy had great flavors and was very soft and chewy. Each candy was individually wrapped well. None of the candies were stuck together, which did happen in the expensive version, Fral...', 1, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('This taffy is so good. It is very soft and chewy. The flavors are amazing. I would definitely recommend you buying it. Very satisfying!!', 1, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('Right now I''m mostly just sprouting this so my cats can eat the grass. They love it. I rotate it around with Wheatgrass and Rye too', 1, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('This is a very healthy dog food. Good for their digestion. Also good for small puppies. My dog eats her required amount at every feeding.', 1, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('I don''t know if it''s the cactus or the tequila or just the unique combination of ingredients, but the flavour of this hot sauce makes it one of a kind! We picked up a bottle once on a trip we were on...', 1, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('One of my boys needed to lose some weight and the other didn''t. I put this food on the floor for the chubby guy, and the protein-rich, no by-product food up higher where only my skinny boy can jump. ...', 2, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('My cats have been happily eating Felidae Platinum for more than two years. I just got a new bag and the shape of the food is different. They tried the new food when I first put it in their bowls and n...', 2, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('good flavor! these came securely packed... they were fresh and delicious! i love these Twizzlers!', 2, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('The Strawberry Twizzlers are my guilty pleasure - yummy. Six pounds will be around for a while with my son and I.', 3, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('My daughter loves twizzlers and this shipment of six pounds really hit the spot. It''s exactly what you would expect...six packages of strawberry twizzlers.', 3, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('I love eating them and they are good for watching TV and looking at movies! It is not too sweet. I like to transfer them to a zip lock baggie so they stay fresh so I can take my time eating them.', 4, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('I am very satisfied with my Twizzler purchase. I shared these with others and we have all enjoyed them. I will definitely be ordering more.', 4, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('Twizzlers, Strawberry my childhood favorite candy, made in Lancaster Pennsylvania by Y & S Candies, Inc. one of the oldest confectionery Firms in the United States, now a Subsidiary of the Hershey Com...', 4, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('Candy was delivered very fast and was purchased at a reasonable price. I was home bound and unable to get to a store so this was perfect for me.', 5, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('My husband is a Twizzlers addict. We''ve bought these many times from Amazon because we''re government employees living overseas and can''t get them in the country we are assigned to. They''ve always be...', 5, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('I bought these for my husband who is currently overseas. He loves these, and apparently his staff likes them also.<br />There are generous amounts of Twizzlers in each 16-ounce bag, and this was well ...', 5, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('I can remember buying this candy as a kid and the quality hasn''t dropped in all these years. Still a superb product you won''t be disappointed with.', 5, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('I love this candy. After weight watchers I had to cut back but still have a craving for it.', 5, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('I have lived out of the US for over 7 yrs now, and I so miss my Twizzlers!! When I go back to visit or someone visits me, I always stock up. All I can say is YUM!<br />Sell these in Mexico and you w...', 5, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('Product received is as advertised.<br /><br /><a href="http://www.amazon.com/gp/product/B001GVISJM">Twizzlers, Strawberry, 16-Ounce Bags (Pack of 6)</a>', 6, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('The candy is just red , No flavor . Just plan and chewy . I would never buy them again', 6, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('I was so glad Amazon carried these batteries. I have a hard time finding them elsewhere because they are such a unique size. I need them for my garage door opener.<br />Great deal for the price.', 7, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('I got this for my Mum who is not diabetic but needs to watch her sugar intake, and my father who simply chooses to limit unnecessary sugar intake - she''s the one with the sweet tooth - they both LOVED...', 7, (SELECT topicID FROM Topics WHERE topicName = 'Food')),
  ('I don''t know if it''s the cactus or the tequila or just the unique combination of ingredients, but the flavour of this hot sauce makes it one of a kind! We picked up a bottle once on a trip we were on...', 7, (SELECT topicID FROM Topics WHERE topicName = 'Food'));
