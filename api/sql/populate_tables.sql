INSERT INTO user (id,username,phone_number,password)
  VALUES ('1','rwolande','16302127926','junk'),
  ('2','aripaws','1666','junk2'),
  ('3','ducky','1600','junk3');

INSERT INTO squad (id,name)
  VALUES ('1','squiddish squad'),
  ('2','some group'),
  ('3','lame group');

INSERT INTO user_squad (user_id,squad_id)
  VALUES ('1','1'),
  ('2','1'),
  ('3','1'),
  ('1','2'),
  ('2','2'),
  ('2','3'),
  ('3','3');
  