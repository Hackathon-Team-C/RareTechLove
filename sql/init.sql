GRANT ALL PRIVILEGES ON db.* TO 'user'@'%';

FLUSH PRIVILEGES;

DROP DATABASE IF EXISTS raretechlovedb;
CREATE DATABASE raretechlovedb;
USE raretechlovedb;

DROP TABLE IF EXISTS user_mst;
CREATE TABLE user_mst
(
  user_cd INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(255) NOT NULL,
  pw VARCHAR(255) NOT NULL,
  slack_name VARCHAR(255) NOT NULL,
);

DROP TABLE IF EXISTS article_mst;
CREATE TABLE article_mst
(
  artile_cd INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  artile_url VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL,
  artile_rank VARCHAR(255) NOT NULL,
  artile_title VARCHAR(21844) NOT NULL
);

DROP TABLE IF EXISTS q_count_tbl;
CREATE TABLE q_count_tbl
(
  q_cd INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  q_cnt INT NULL,
  a_cnt INT NULL,
);

DROP TABLE IF EXISTS question_tbl;
CREATE TABLE question_tbl
(
  ts_cd INT NOT NULL AUTO_INCREMENT,
  artile_cd INT NOT NULL,
  user_cd INT NOT NULL,
  quetion_thred VARCHAR(21844) NOT NULL,
  ts timestamp DEFAULT NOT NULL,
  qa_dist BOOLEAN NOT NULL,
);
