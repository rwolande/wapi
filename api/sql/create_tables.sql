CREATE TABLE user (
  id int(11) NOT NULL AUTO_INCREMENT,
  username varchar(255) NOT NULL,
  phone_number varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  last_login_at datetime NOT NULL,
  image_source varchar(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY phone_number (phone_number)
);

CREATE TABLE squad (
  id int(11) NOT NULL AUTO_INCREMENT,
  start_image_source varchar(255) NOT NULL,
  current_image_source varchar(255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE user_squad (
  user_id int(11) NOT NULL,
  squad_id int(11) NOT NULL,
  KEY user_fk (user_id),
  KEY squad_fk (squad_id),
  CONSTRAINT squad_fk FOREIGN KEY (squad_id) REFERENCES squad (id) ON DELETE CASCADE,
  CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES user (id)
);

-- CREATE TABLE event (
--   id int(11) NOT NULL AUTO_INCREMENT,
--   user_id varchar(255) DEFAULT NULL,
--   short_desc varchar(255) DEFAULT NULL,
--   description varchar(255) DEFAULT NULL,
--   start_date datetime DEFAULT NULL,
--   end_date datetime DEFAULT NULL,
--   max_volunteers_needed int(11) DEFAULT NULL,
--   current_num_volunteers int(11) DEFAULT NULL,
--   close_date datetime DEFAULT NULL,
--   creator_id int(11) DEFAULT NULL,
--   created_date datetime DEFAULT NULL,
--   last_updated_date datetime DEFAULT NULL,
--   pic_url varchar(255) DEFAULT NULL,
--   street_addr varchar(255) DEFAULT NULL,
--   city varchar(255) DEFAULT NULL,
--   state varchar(255) DEFAULT NULL,
--   zipcode varchar(10) DEFAULT NULL,
--   organization varchar(255) DEFAULT NULL,
--   lat float(20,17) DEFAULT NULL,
--   lon float(20,17) DEFAULT NULL,
--   PRIMARY KEY (id),
--   KEY creator_id (creator_id),
--   CONSTRAINT event_ibfk_1 FOREIGN KEY (creator_id) REFERENCES user (id)
-- );