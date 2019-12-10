CREATE TABLE user (
  id int(11) NOT NULL AUTO_INCREMENT,
  username varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  last_login datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  role int(3) NOT NULL DEFAULT 1,
  PRIMARY KEY (id),
  UNIQUE KEY username (username)
);

CREATE TABLE trip (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  name varchar(255)  NOT NULL DEFAULT '',
  start_date datetime DEFAULT NULL,
  end_date datetime DEFAULT NULL,
  comment varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (id),
  CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);