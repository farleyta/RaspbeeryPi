CREATE TABLE beverages (
  id UUID UNIQUE NOT NULL,
  name VARCHAR NOT NULL,
  created TIMESTAMP
);

INSERT into beverages (id, name, created) VALUES ('00000000-0000-0000-0000-000000000000', 'Debug', '2017-10-26 05:19:22.149948');
INSERT into beverages (id, name, created) VALUES ('4cee422a-5f3e-4159-9cf4-f4beab98c08f', 'Dead Grasshopper IPA', '2017-10-14 07:59:16.062841');
INSERT into beverages (id, name, created) VALUES ('68725d44-bec8-405a-acda-b558e4a141d5', 'Water', '2017-10-22 18:15:12.195767');
INSERT into beverages (id, name, created) VALUES ('843c059a-76ad-41d1-b3f1-2647785651d4', 'Water', '2017-10-26 10:05:48.548142');
