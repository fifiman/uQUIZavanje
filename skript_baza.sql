BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "quiz_user" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"is_staff"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"email"	varchar(255) NOT NULL UNIQUE,
	"age"	integer,
	"is_active"	bool NOT NULL,
	"first_name"	varchar(50) NOT NULL,
	"last_name"	varchar(50) NOT NULL,
	"level"	integer NOT NULL,
	"picture"	text,
	"is_moderator"	bool NOT NULL,
	"wants_moderator"	bool NOT NULL,
	"exp"	integer NOT NULL,
	"ranking"	integer NOT NULL
);
CREATE TABLE IF NOT EXISTS "quiz_game" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"player_one_pts"	integer NOT NULL,
	"player_two_pts"	integer NOT NULL,
	"player_three_pts"	integer NOT NULL,
	"player_four_pts"	integer NOT NULL,
	"winner_id"	integer,
	"player_four_id"	integer,
	"player_one_id"	integer,
	"player_three_id"	integer,
	"player_two_id"	integer,
	"cur_question"	integer NOT NULL,
	"game_state"	integer NOT NULL,
	"num_answers"	integer NOT NULL,
	"num_players"	integer NOT NULL,
	"num_questions"	integer NOT NULL,
	FOREIGN KEY("winner_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("player_four_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("player_three_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("player_one_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("player_two_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "quiz_gamequestions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"index"	integer NOT NULL,
	"game_id"	integer NOT NULL,
	"question_id"	integer NOT NULL,
	"p1_pts"	integer NOT NULL,
	"p2_pts"	integer NOT NULL,
	"p3_pts"	integer NOT NULL,
	"p4_pts"	integer NOT NULL,
	FOREIGN KEY("game_id") REFERENCES "quiz_game"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("question_id") REFERENCES "quiz_question"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "quiz_report" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"report_text"	text NOT NULL,
	"reported_id"	integer NOT NULL,
	"reporter_id"	integer NOT NULL,
	FOREIGN KEY("reported_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("reporter_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "quiz_gameanswers" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"answer_index"	integer NOT NULL,
	"correct"	bool NOT NULL,
	"game_id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"question_index"	integer NOT NULL,
	FOREIGN KEY("game_id") REFERENCES "quiz_game"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"action_time"	datetime NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag">=0),
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "quiz_friendship" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"first_friend_id_id"	integer NOT NULL,
	"second_friend_id_id"	integer NOT NULL,
	"accepted"	bool NOT NULL,
	FOREIGN KEY("first_friend_id_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("second_friend_id_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "quiz_question" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"question"	text NOT NULL,
	"is_valid"	bool NOT NULL,
	"answer_one"	text NOT NULL,
	"answer_two"	text NOT NULL,
	"answer_three"	text NOT NULL,
	"answer_four"	text NOT NULL,
	"correct"	integer NOT NULL,
	"category_id"	integer NOT NULL,
	FOREIGN KEY("category_id") REFERENCES "quiz_category"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "quiz_category" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	varchar(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "quiz_user_user_permissions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "quiz_user_groups" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "quiz_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	varchar(150) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL
);
INSERT INTO "quiz_user" ("id","password","last_login","is_superuser","username","is_staff","date_joined","email","age","is_active","first_name","last_name","level","picture","is_moderator","wants_moderator","exp","ranking") VALUES (1,'pbkdf2_sha256$150000$DlYDmCBUuvqo$hJxVn6M2UF/3+JmNMAjzyWoLq/NG6FbQ/Gz7oriAc5o=','2019-06-07 16:46:54.700541',1,'admin',1,'2019-05-25 15:56:59.238026','admin@admin.com',NULL,1,'','',2,'quiz/avatar2.jpg',0,0,364,80);
INSERT INTO "quiz_user" ("id","password","last_login","is_superuser","username","is_staff","date_joined","email","age","is_active","first_name","last_name","level","picture","is_moderator","wants_moderator","exp","ranking") VALUES (3,'pbkdf2_sha256$150000$ugEFm51yl6VF$916H+ztQsaiI7j78WPw9PfcKguh6CQylwlDadVd09lI=','2019-06-07 16:53:39.466101',0,'Marko',0,'2019-05-28 00:04:02.596367','marko@gmail.com',21,1,'Marko','Stefanovic',20,'quiz/avatar17.jpg',1,0,0,1000);
INSERT INTO "quiz_user" ("id","password","last_login","is_superuser","username","is_staff","date_joined","email","age","is_active","first_name","last_name","level","picture","is_moderator","wants_moderator","exp","ranking") VALUES (9,'pbkdf2_sha256$150000$SgakBTaBMaBG$RzjlIjiH03csFUDU3RKg7A9gdWntEN4G9W1rCD4Drww=','2019-05-30 14:39:30.530141',0,'Kole',0,'2019-05-30 14:39:20.925903','k@k.com',21,1,'Kole','Kole',0,'quiz/default_avatar.jpg',0,0,0,-1);
INSERT INTO "quiz_user" ("id","password","last_login","is_superuser","username","is_staff","date_joined","email","age","is_active","first_name","last_name","level","picture","is_moderator","wants_moderator","exp","ranking") VALUES (12,'pbkdf2_sha256$150000$qsw0oqCiawYL$jJualQLOn0/aywXGaICeafdLnu9nI0FTpqoFDB8I4QI=','2019-05-30 15:43:50.629227',0,'Danlo',0,'2019-05-30 15:07:22','danlo@jovanovic.com',NULL,1,'Danilo','Jovanovic',0,'quiz/avatar5.jpg',0,0,0,-1);
INSERT INTO "quiz_user" ("id","password","last_login","is_superuser","username","is_staff","date_joined","email","age","is_active","first_name","last_name","level","picture","is_moderator","wants_moderator","exp","ranking") VALUES (13,'pbkdf2_sha256$150000$fCrbM29IuS5h$CMu4jHI3jydw9Mjmj1ZTPuf7mGYuai+auQ8AobEbw3k=',NULL,0,'Cone',0,'2019-05-30 15:08:10','nemanja@jovanovic.com',21,1,'Nemanja','Jovanovic',0,'quiz/default_avatar.jpg',0,0,0,-1);
INSERT INTO "quiz_user" ("id","password","last_login","is_superuser","username","is_staff","date_joined","email","age","is_active","first_name","last_name","level","picture","is_moderator","wants_moderator","exp","ranking") VALUES (14,'pbkdf2_sha256$150000$1EWaOyMRpSCU$Ry2zYDoPNwgXQu3ItxgSTlmXZpNEPjcEphTsP2Dowy4=','2019-05-30 20:49:19.918600',0,'Velimir',0,'2019-05-30 15:25:45.352997','velimir@stefanovic.com',21,1,'Velimir','Stefanovic',0,'quiz/default_avatar.jpg',0,0,0,-1);
INSERT INTO "quiz_user" ("id","password","last_login","is_superuser","username","is_staff","date_joined","email","age","is_active","first_name","last_name","level","picture","is_moderator","wants_moderator","exp","ranking") VALUES (15,'pbkdf2_sha256$150000$M7Aukxe4Wuy2$JEuuCsNbfmU9mt8AgdDEbcpJ1gh+hw/2vCbN0L+iWzc=','2019-06-07 21:14:32.857182',0,'NemanjaJov',0,'2019-05-31 14:29:08.165166','nema.jov97@gmail.com',22,1,'Nemanja','Jovanovic',3,'quiz/avatar11.jpg',0,1,447,119);
INSERT INTO "quiz_user" ("id","password","last_login","is_superuser","username","is_staff","date_joined","email","age","is_active","first_name","last_name","level","picture","is_moderator","wants_moderator","exp","ranking") VALUES (16,'pbkdf2_sha256$150000$FJnp7bdcBo4y$vRQyNnP6d0C5Z1Du6ikZrQAL9eDc+656y1I97hTqIFo=','2019-06-03 11:28:18.111172',0,'temp',0,'2019-06-03 11:28:17.532880','temp@hotmail.com',21,0,'temp','temp',0,'quiz/default_avatar.jpg',0,0,0,-1);
INSERT INTO "quiz_user" ("id","password","last_login","is_superuser","username","is_staff","date_joined","email","age","is_active","first_name","last_name","level","picture","is_moderator","wants_moderator","exp","ranking") VALUES (18,'pbkdf2_sha256$150000$uGzb9F81JqOD$PNbHkHHbB+MqRNET8DsZh9w3sFohrMblRfKEwx9XtZU=','2019-06-07 20:40:42.464366',1,'admin2',1,'2019-06-03 11:36:43.472116','asda@asd.com',NULL,1,'','',0,'quiz/default_avatar.jpg',0,0,0,-1);
INSERT INTO "quiz_user" ("id","password","last_login","is_superuser","username","is_staff","date_joined","email","age","is_active","first_name","last_name","level","picture","is_moderator","wants_moderator","exp","ranking") VALUES (19,'pbkdf2_sha256$150000$dB8K7h2a5VAM$+Udr4OxnH7f480DAIS8GRfR69/5ct9xG8hJOMJANkNs=','2019-06-03 13:07:57.487601',1,'admin3',1,'2019-06-03 13:07:53.393142','asda@asdad.com',NULL,1,'','',0,'quiz/default_avatar.jpg',0,0,0,-1);
INSERT INTO "quiz_report" ("id","report_text","reported_id","reporter_id") VALUES (1,'Zbog da jedeš govna',16,15);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (1,'2019-05-25 16:09:14.734468','1','Sport',1,'[{"added": {}}]',7,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (2,'2019-05-25 16:09:24.187405','2','General Knowledge',1,'[{"added": {}}]',7,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (3,'2019-05-25 16:09:32.554034','3','Geography',1,'[{"added": {}}]',7,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (4,'2019-05-25 16:09:46.090790','4','History',1,'[{"added": {}}]',7,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (5,'2019-05-25 16:10:47.343325','1','Question:Koliko se utakmica igra u NBA sezoni ? Answers: 82 72 62 92',1,'[{"added": {}}]',8,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (6,'2019-05-25 16:11:49.816332','2','Question:Glavni grad Estonije je ... Answers: Talin Moskva Riga Vilnus',1,'[{"added": {}}]',8,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (7,'2019-05-25 16:12:48.350388','3','Question:Koje godine je rodjen Karl Marks ? Answers: 1918 1818 1848 1888',1,'[{"added": {}}]',8,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (8,'2019-05-25 17:15:14.503243','2','Mrcko Level: 10 Rating: 1000',2,'[{"changed": {"fields": ["level", "picture", "ranking"]}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (9,'2019-05-30 12:34:06.349876','5','Petar Level: 0',1,'[{"added": {}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (10,'2019-05-30 12:34:42.802168','6','Nikola Level: 0',1,'[{"added": {}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (11,'2019-05-30 12:35:34.283628','7','Zivorad Level: 0',1,'[{"added": {}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (12,'2019-05-30 12:36:12.034540','8','Ivan Level: 0',1,'[{"added": {}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (13,'2019-05-30 12:36:26.760238','4','d Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (14,'2019-05-30 14:49:51.196764','10','Sale Level: 0',1,'[{"added": {}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (15,'2019-05-30 15:03:48.401898','11','Robert Level: 0',1,'[{"added": {}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (16,'2019-05-30 15:04:24.443942','11','Robert Level: 0',2,'[{"changed": {"fields": ["first_name", "last_name", "email"]}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (17,'2019-05-30 15:06:22.494645','8','Ivan Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (18,'2019-05-30 15:06:22.635321','6','Nikola Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (19,'2019-05-30 15:06:22.682201','5','Petar Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (20,'2019-05-30 15:06:22.729083','10','Sale Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (21,'2019-05-30 15:06:22.791577','7','Zivorad Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (22,'2019-05-30 15:06:43.597338','22','admin Level: 0 Ivan Level: 0',3,'',10,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (23,'2019-05-30 15:06:43.644256','21','admin Level: 0 Zivorad Level: 0',3,'',10,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (24,'2019-05-30 15:06:43.691097','20','admin Level: 0 Petar Level: 0',3,'',10,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (25,'2019-05-30 15:06:43.753638','19','admin Level: 0 Nikola Level: 0',3,'',10,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (26,'2019-05-30 15:06:43.800521','17','Marko Level: 0 admin Level: 0',3,'',10,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (27,'2019-05-30 15:06:43.843787','16','admin Level: 0 Marko Level: 0',3,'',10,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (28,'2019-05-30 15:07:06.822920','8','Ivan Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (29,'2019-05-30 15:07:06.916678','2','Mrcko Level: 10 Rating: 1000',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (30,'2019-05-30 15:07:06.963525','6','Nikola Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (31,'2019-05-30 15:07:07.026031','5','Petar Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (32,'2019-05-30 15:07:07.072958','11','Robert Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (33,'2019-05-30 15:07:07.119828','10','Sale Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (34,'2019-05-30 15:07:07.166696','7','Zivorad Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (35,'2019-05-30 15:07:23.067849','12','Danlo Level: 0',1,'[{"added": {}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (36,'2019-05-30 15:07:50.113043','12','Danlo Level: 0',2,'[{"changed": {"fields": ["first_name", "last_name", "email"]}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (37,'2019-05-30 15:08:10.634850','13','Cone Level: 0',1,'[{"added": {}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (38,'2019-05-30 15:08:33.036278','13','Cone Level: 0',2,'[{"changed": {"fields": ["first_name", "last_name", "email"]}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (39,'2019-05-30 15:23:44.880036','13','Cone Level: 0',2,'[{"changed": {"fields": ["age"]}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (40,'2019-05-30 15:25:45.599653','14','Velimir Level: 0',1,'[{"added": {}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (41,'2019-05-30 20:51:28.323910','3','Marko Level: 20 Rating: 1000',2,'[{"changed": {"fields": ["level", "ranking"]}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (42,'2019-06-03 11:35:00.080369','17','admin2 Level: 0',1,'[{"added": {}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (43,'2019-06-03 11:35:50.290335','17','admin2 Level: 0',3,'',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (44,'2019-06-07 15:31:22.158968','6','Music',1,'[{"added": {}}]',7,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (45,'2019-06-07 15:31:30.763354','7','Film',1,'[{"added": {}}]',7,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (46,'2019-06-07 16:38:37.142230','15','NemanjaJov Level: 3',2,'[{"changed": {"fields": ["wants_moderator"]}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (47,'2019-06-07 16:43:46.443572','15','NemanjaJov Level: 3',2,'[{"changed": {"fields": ["wants_moderator"]}}]',6,1);
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","action_flag","change_message","content_type_id","user_id") VALUES (48,'2019-06-07 16:46:31.997847','15','NemanjaJov Level: 3',2,'[{"changed": {"fields": ["wants_moderator"]}}]',6,1);
INSERT INTO "quiz_friendship" ("id","first_friend_id_id","second_friend_id_id","accepted") VALUES (23,1,12,1);
INSERT INTO "quiz_friendship" ("id","first_friend_id_id","second_friend_id_id","accepted") VALUES (24,12,1,1);
INSERT INTO "quiz_friendship" ("id","first_friend_id_id","second_friend_id_id","accepted") VALUES (25,3,1,1);
INSERT INTO "quiz_friendship" ("id","first_friend_id_id","second_friend_id_id","accepted") VALUES (26,3,12,0);
INSERT INTO "quiz_friendship" ("id","first_friend_id_id","second_friend_id_id","accepted") VALUES (27,1,3,1);
INSERT INTO "quiz_friendship" ("id","first_friend_id_id","second_friend_id_id","accepted") VALUES (29,15,1,1);
INSERT INTO "quiz_friendship" ("id","first_friend_id_id","second_friend_id_id","accepted") VALUES (31,1,15,1);
INSERT INTO "quiz_friendship" ("id","first_friend_id_id","second_friend_id_id","accepted") VALUES (37,15,3,0);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (202,'Koje godine je rodjen Leo Messi?',1,'1987','1990','1986','1988',1,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (203,'Koje godine su se spojile NBA i ABA(American Basketball Association)?',1,'1966','1976','1986','1996',2,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (204,'Koja reprezentacija je osvojila prvo svetsko prvenstvo u fudbalu?',1,'Brazil','Argentina','Urugvaj','Paragvaj',3,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (205,'Koji NBA tim ima najvise sampionskih titula?',1,'Boston Celtics','LA Lakers','Golden State Warriors','Milwaukee Bucks',1,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (206,'U kom timu je Kristijano Ronaldo zapoceo svoju profesionalnu karijeru?',1,'Real Madrid','Mancester junajted','Sporting','Porto',3,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (207,'Koliko ukupno olimpijskih medalja ima Majkl Felps?',1,'30','28','26','24',2,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (208,'Koji tim ima najvise osvojenih titula u Premier ligi(od njenog osnivanja 1992)?',1,'Liverpul','Celsi','Mancester junajted','Arsenal',3,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (209,'Koji je jedini tim u Premier ligi koji je imao savrsenu sezonu(sezonu bez poraza)?',1,'Liverpul','Arsenal','Mancester junajted','Mancester siti',2,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (210,'Kako se zove izumitelj kosarke?',1,'Dzejms Nejsmit','Dzejms Harden','Dzejms Lebron','Dzejms Bond',1,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (211,'Koje godine je FK Partizan igrao finale Lige Sampiona?',1,'1946','1956','1966','Nikad',3,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (212,'Koliko inca iznosi precnik kosarkaskog obruca?',1,'17','18','19','20',2,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (213,'Koji broj se na tabli za pikado nalazi izmedju 9 i 5?',1,'17','3','16','12',4,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (214,'Stadion San Siro nalazi se u kom italijanskom gradu?',1,'Napulj','Torino','Rim','Milano',4,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (215,'Kako se zove jedini osvajac Vimbldona koji je na turniru ucestvovao zahvaljujuci pozivnici (wild card)?',1,'Goran Ivanisevic','Stanislas Vavrinka','Boris Beker','Huan Martin del Potro',1,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (216,'Artur Konan Dojl, autor prica o Serloku Holmsu, bio je golman kog engleskog fudbalskog kluba?',1,'Portsmouth','Port Vale','Vimbledon','Chelsea',1,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (217,'Koja dva fudbalska kluba igraju derbi koji se popularno naziva Old Firm?',1,'Liverpul i Mancester Junajted','Liverpul i Everton','Seltik i Rendzers','Aston Vila i Birmingem Siti',3,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (218,'Koliko igraca cini tim u hokeju (ukljucujuci i golmana)?',1,'5','6','7','8',2,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (219,'Koliko poena iznosi najveci teoretski moguci brejk u snukeru?',1,'100','126','148','155',4,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (220,'Jedina drzava koja je osvojila medalju na zimskim ali ne i na letnjim olimpijskim igrama je?',1,'Luksemburg','San Marino','Lihtenstajn','Farska ostrva',3,20);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (221,'Koji reper sa Jamajke je 1995 izdao pesmu "Bombastic"?',1,'Shaggy','Sean Paul','Shuggy','Shrek th rapper',1,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (222,'Dopunite naslov pesme grupe U2: "Hold me, Thrill Me, Kiss me ..."',1,'Feel me','Beat me','Kill me','Miss me',3,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (223,'Koje godine su Bitlsi (The Beatles) izdali pesmu "Hey Jude"?',1,'1963','1964','1966','1968',4,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (224,'Koji Svedski DJ je 2004te izdao pesmu "Call on me"?',1,'Avicii','Sweedish House Mafia','Eric Prydz','Tiesto',3,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (225,'Tekst  "Since you''ve gone I''ve been lost without a trace /I dream at night I can only see your face" je deo koje Stingove pesme?',1,'Every breath you take','Shape of my heart','Desert rose','Englishman in New York',1,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (226,'Tekst "They told him don''t you ever come around here / Don''t want to see your face, you better disappear" je deo koje Majkl Dzeksonove pesme?',1,'Bad','They don''t care about us','Beat it','Smooth criminal',3,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (227,'Koje godine je preminuo reper Mac Miller?',1,'1998','2008','2017','2018',4,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (228,'Koje godine je grupa Queen izdala pesmu "Bohemian rhapsody"?',1,'1974','1975','1976','1977',2,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (229,'Koje godine je rodjen reper Snoop Dogg?',1,'1967','1971','1974','1973',2,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (230,'Gde se nalazi Rock''n''roll kuca slavnih?',1,'Springfild','Nju Jork','Klivland','Hjuston',3,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (231,'Koji proizvodjac gitara proizvodi model Stratocaster?',1,'Gibson','Ibanez','Yamaha','Fender',4,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (232,'Sa kojom pevacicom narodne muzike je Oliver Mandic snimio duet?',1,'Lepa Brena','Ceca','Ana Bekuta','Dragana Mirkovid',2,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (233,'Koji kompozitor je autor 4 godisnja doba?',1,'Johan Sebastian Bah','Djuzepe Verdi','Antonio Vivaldi','Nikolo Paganini',3,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (234,'Koji kompozitor je autor simfonijske poeme Vltava?',1,'Antonjin Dvorzak','Bedzih Smetana','Edvard Grig','Aleksandar Borodin',2,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (235,'U kojoj grupi je pevao Bon Scott?',1,'AC/DC','Led Zeppelin','Deep Purple','Whitesnake',1,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (236,'Kom gradu je Mocart posvetio svoju 38. simfoniju?',1,'Parizu','Becu','Hamburgu','Pragu',4,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (237,'Evrovizijsku naslovnu temu komponovao je koji kompozitor?',1,'Ludvig van Betoven','Mark-Andre Ter Stegen','Mark-Antoan Sarpentjer','Petar-Iljic Cajkovski',3,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (238,'Ime grupe ABBA je akronim nastao od imena Agneta, Bjorn, Ani i?',1,'Boris','Beri','Beni','Bili',3,21);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (239,'Koji je najseverniji glavni grad na svet?',1,'Otava','Rejkjavik','Ulanbator','Helsinki',1,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (240,'Koja od ovih drzava ima tri glavna grada?',1,'Juznoafricka republika','Holandija','Izrael','Bolivia',1,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (241,'Koji je drugi po povrsini najveci kontinent na svetu?',1,'Afrika','Severna Amerika','Juzna Amerika','Evvropa',1,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (242,'Koja zemlja ima najduzu obalu na svetu?',1,'Australia','Kanada','Indonezija','Grcka',2,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (243,'Kako se zove glavni grad Jordan-a?',1,'Abu dabi(Abu Dhabi)','Kito(Quito)','Aman(Amman)','Dakar(Dakar)',3,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (244,'Kako se zove glavni grad Gane',1,'Beirut(Beirut)','Manila(Manilla)','Akra(Accra)','Kinsasa(Kinshasa)',3,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (245,'Kako se zove glavni grad Nigerije?',1,'Gitega(Gitega)','Harare(Harare)','Abudza(Abuja)','Aman(Amman)',3,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (246,'Koji je bio glavni grad Obale slonovace od 1933 do 1983 godine?',1,'Daloa','Kumasi','Abidjan','San Pedro',3,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (247,'Koji je bio glavni grad Zapadne Nemacke od 1949 do 1990',1,'Zapadni Berlin','Bon','Stutgart','Bremen',3,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (248,'Koji je bio glavni grad Kine od 1945 do 1949?',1,'Nanking','Chang''an','Kaifeng','Hangzhou',1,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (249,'Koji je najveca kontinenalna zemlja na svetu?',1,'Mongolija','Kazahstan','Cad','Nigerija',2,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (250,'Koja zemlja ima najvise jezera na svetu?',1,'Kanada','Sjedinjene Americke Drzave','Finska','Rusija',1,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (251,'Rijad je glavni grad koje drzave?',1,'Libija','Sirija','Jemen','Saudijska Arabija',4,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (252,'Koji je najveci grad na svetu, gledano po povrsini koju zauzima?',1,'Bombaj','Sangaj','Hulunbuir','London',3,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (253,'Koliko drzava postoji na africkom kontinentu?',1,'63','47','54','59',3,22);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (254,'Koja istorijska licnost je zivela od 1758 do 1794?',1,'Fernando Magelan','Maksimilijan Robespijer','Frencis Bejkon','Napoleon',1,23);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (255,'Kako se zove Portugalski istrazivac koji je poznat kao prvi Evropljanin koji je doplovio do Indije kroz Rt Dobre Nade?',1,'Amerigo Vespuci','Vasko Da Gama','Francisko Pizaro','Bartolomeo Dijaz',2,23);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (256,'Kako se zove prvi istrazivac koji je tvrdio da Kolumbo nije doplovio do istocne Azije, vec do novog(do tada nepoznatog) sveta?',1,'Amerigo Vespuci','Marko Polo','Bartolomeo Dijaz','Francisko Pizaro',1,23);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (257,'U kom gradu je izvrsen atentat na Abrahama Linkolna?',1,'Vasington DC','Nju Jork','Atlanta','Ricmond',2,23);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (258,'U kom gradu je izvrsen atentat na Dzona F. Kenedija?',1,'Nju Jork','Nju Orleans','Dalas','Vasington DC',3,23);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (259,'Ko je prvi demokratski izabrani predsednik Rusije?',1,'Mihail Gorbacov','Nikita Hruscov','Boris Jeljcin','Vladimir Putin',3,23);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (260,'Koliko godina je trajao stogodisnji rat?',1,'100','96','106','116',4,23);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (261,'Koliko je trajao Anglo-Zanzibarski rat, najkraci rat u istoriji?',1,'2 dana','16 sati','38 minuta','5 minuta',3,23);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (262,'Kako se zvao prvi Zemljin vestacki satelit?',1,'Sputnjik','Vostok','Mir','Lajka',1,23);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (263,'Koliko britanskih kolonija je formiralo Sjedinjene Americke Drzave?',1,'12','13','24','50',2,23);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (264,'Kralj Pir, po kome je nazvana pobeda uz velike gubitke, vladao je kojom antickom drzavom?',1,'Lidija','Tesalija','Epir','Persija',3,23);
INSERT INTO "quiz_question" ("id","question","is_valid","answer_one","answer_two","answer_three","answer_four","correct","category_id") VALUES (265,'Bitka na Somi bila je najveca bitka kog rata?',1,'Prvi svetski rat','Drugi svetski rat','Stogodisnji rat','Rat za spansko nasledje',1,23);
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('casxy9eho0okj2shlz4bhvwohfnvktdp','MjJjZjkzMTY0YjMxYzQ4Mzk1ZTdlZjE2ZTkwZjNmNTQ3OWI1MGMwYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjOGE4ZGM4OWE3MWJmZjRkOTI0ZDU4MTEzYTNhNmU3NDRhMWI2ZmFlIn0=','2019-06-11 00:33:58.133229');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('4e5g4zpgq0lpvis9uasu3fk5d09tvk97','MjJjZjkzMTY0YjMxYzQ4Mzk1ZTdlZjE2ZTkwZjNmNTQ3OWI1MGMwYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjOGE4ZGM4OWE3MWJmZjRkOTI0ZDU4MTEzYTNhNmU3NDRhMWI2ZmFlIn0=','2019-06-12 13:07:49.269485');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('0krecxkrmbg0l535dnkvzclni88luczp','MjJjZjkzMTY0YjMxYzQ4Mzk1ZTdlZjE2ZTkwZjNmNTQ3OWI1MGMwYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjOGE4ZGM4OWE3MWJmZjRkOTI0ZDU4MTEzYTNhNmU3NDRhMWI2ZmFlIn0=','2019-06-13 11:08:04.654728');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('96nduyiruqd6wn8b5d501orqtak33w5z','MmE3ODkxMzUxZmQ1NDUxNzQwZWFkMmI3MTMwNTkzYjkxZmQxYzkzNzp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3N2I5MTljNWQzMjZjNWNjNDdhOTBlZWZmMDJjZWZhNjJhNDkxNzE5In0=','2019-06-13 21:26:49.941793');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('ftqezpb9f9wx9f4bfdaj5rcmdjmddzpi','YTRkYjc5MGNlY2NhMTQ5ZGRmY2Y1Yjc1NmI0NGI3ZTNjYjlmMjdkMTp7Il9hdXRoX3VzZXJfaWQiOiIxNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNTFlZGE0NWFmOWU2MTc3MDI2YTI3NmQ1NjA5MTBjNWQzNDgzNjUwNiJ9','2019-06-14 21:48:42.131412');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('5qa96lsvye732l167sqx45bopuc8g9je','YzdlOWMwMGQ4ZGRhMzhhNDcyM2E4ZGFjNzE2ZGU2ODc2MDVmMzU4ZDp7Il9hdXRoX3VzZXJfaWQiOiIxOCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZGMyYzdiN2E0MjBhNWQ5NGRmNTJmODJiNTljZTU3MjdhZjY3NmVmYSJ9','2019-06-17 11:37:03.280199');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('bl976n0xm1bthpk3zdbc8431j5yb95bf','MjJjZjkzMTY0YjMxYzQ4Mzk1ZTdlZjE2ZTkwZjNmNTQ3OWI1MGMwYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjOGE4ZGM4OWE3MWJmZjRkOTI0ZDU4MTEzYTNhNmU3NDRhMWI2ZmFlIn0=','2019-06-17 12:54:38.212139');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('ovbvsk7o6gfahyp56hc3hyg9rkppustb','NDk3NWViNmE0ZjVjZjA4ZWJkZGIxMzcxM2RkZTA1OWNiYTcwY2VmOTp7Il9hdXRoX3VzZXJfaWQiOiIxOSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNWRmZDIwNTA3NjBjYjc1ZTQwNjdmZThmMmI5ODU1NTE0YTUwOTU5OSJ9','2019-06-17 13:07:57.497228');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('4s896n2nobxqlf4kuo5c96g9o8ynbwgl','MjJjZjkzMTY0YjMxYzQ4Mzk1ZTdlZjE2ZTkwZjNmNTQ3OWI1MGMwYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjOGE4ZGM4OWE3MWJmZjRkOTI0ZDU4MTEzYTNhNmU3NDRhMWI2ZmFlIn0=','2019-06-17 18:34:30.385408');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('ixgnsyqcqacpwzik265w304mg7mc1lcr','MmE3ODkxMzUxZmQ1NDUxNzQwZWFkMmI3MTMwNTkzYjkxZmQxYzkzNzp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3N2I5MTljNWQzMjZjNWNjNDdhOTBlZWZmMDJjZWZhNjJhNDkxNzE5In0=','2019-06-17 18:35:15.043002');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('9nvk5otfyxm578pdfa0ihjqs89ro57yt','MmE3ODkxMzUxZmQ1NDUxNzQwZWFkMmI3MTMwNTkzYjkxZmQxYzkzNzp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3N2I5MTljNWQzMjZjNWNjNDdhOTBlZWZmMDJjZWZhNjJhNDkxNzE5In0=','2019-06-18 20:02:53.603120');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('jz7fxqa5x90u1la4e7m7m11e0rvkvnl0','MjJjZjkzMTY0YjMxYzQ4Mzk1ZTdlZjE2ZTkwZjNmNTQ3OWI1MGMwYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjOGE4ZGM4OWE3MWJmZjRkOTI0ZDU4MTEzYTNhNmU3NDRhMWI2ZmFlIn0=','2019-06-18 20:06:24.338834');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('82cv2id2obvyywid7tr4xq4cbegghyv4','MjJjZjkzMTY0YjMxYzQ4Mzk1ZTdlZjE2ZTkwZjNmNTQ3OWI1MGMwYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjOGE4ZGM4OWE3MWJmZjRkOTI0ZDU4MTEzYTNhNmU3NDRhMWI2ZmFlIn0=','2019-06-18 20:44:43.489746');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('kjtbz2a77rth0zsz8jux3o256t3bwy4d','YTRkYjc5MGNlY2NhMTQ5ZGRmY2Y1Yjc1NmI0NGI3ZTNjYjlmMjdkMTp7Il9hdXRoX3VzZXJfaWQiOiIxNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNTFlZGE0NWFmOWU2MTc3MDI2YTI3NmQ1NjA5MTBjNWQzNDgzNjUwNiJ9','2019-06-21 15:45:08.938356');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('97yo337ftpnwxsrioeibceijno90r9kw','MmE3ODkxMzUxZmQ1NDUxNzQwZWFkMmI3MTMwNTkzYjkxZmQxYzkzNzp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3N2I5MTljNWQzMjZjNWNjNDdhOTBlZWZmMDJjZWZhNjJhNDkxNzE5In0=','2019-06-21 16:53:39.533599');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('i51xqza5g20qsrm7dol9s6zaucusoi67','YzdlOWMwMGQ4ZGRhMzhhNDcyM2E4ZGFjNzE2ZGU2ODc2MDVmMzU4ZDp7Il9hdXRoX3VzZXJfaWQiOiIxOCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZGMyYzdiN2E0MjBhNWQ5NGRmNTJmODJiNTljZTU3MjdhZjY3NmVmYSJ9','2019-06-21 20:40:42.471524');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('ig8v5hrwlrtzq8u2ggteb844l0yse9zp','YTRkYjc5MGNlY2NhMTQ5ZGRmY2Y1Yjc1NmI0NGI3ZTNjYjlmMjdkMTp7Il9hdXRoX3VzZXJfaWQiOiIxNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNTFlZGE0NWFmOWU2MTc3MDI2YTI3NmQ1NjA5MTBjNWQzNDgzNjUwNiJ9','2019-06-21 21:14:32.922681');
INSERT INTO "quiz_category" ("id","name") VALUES (20,'Sport');
INSERT INTO "quiz_category" ("id","name") VALUES (21,'Music');
INSERT INTO "quiz_category" ("id","name") VALUES (22,'Geography');
INSERT INTO "quiz_category" ("id","name") VALUES (23,'History');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (13,4,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (14,4,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (15,4,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (16,4,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (17,5,'add_session','Can add session');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (18,5,'change_session','Can change session');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (19,5,'delete_session','Can delete session');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (20,5,'view_session','Can view session');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (21,6,'add_user','Can add user');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (22,6,'change_user','Can change user');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (23,6,'delete_user','Can delete user');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (24,6,'view_user','Can view user');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (25,7,'add_category','Can add category');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (26,7,'change_category','Can change category');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (27,7,'delete_category','Can delete category');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (28,7,'view_category','Can view category');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (29,8,'add_question','Can add question');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (30,8,'change_question','Can change question');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (31,8,'delete_question','Can delete question');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (32,8,'view_question','Can view question');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (33,9,'add_game','Can add game');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (34,9,'change_game','Can change game');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (35,9,'delete_game','Can delete game');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (36,9,'view_game','Can view game');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (37,10,'add_friendship','Can add friendship');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (38,10,'change_friendship','Can change friendship');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (39,10,'delete_friendship','Can delete friendship');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (40,10,'view_friendship','Can view friendship');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (41,11,'add_gamequestions','Can add game questions');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (42,11,'change_gamequestions','Can change game questions');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (43,11,'delete_gamequestions','Can delete game questions');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (44,11,'view_gamequestions','Can view game questions');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (45,12,'add_gameanswers','Can add game answers');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (46,12,'change_gameanswers','Can change game answers');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (47,12,'delete_gameanswers','Can delete game answers');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (48,12,'view_gameanswers','Can view game answers');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (49,13,'add_report','Can add report');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (50,13,'change_report','Can change report');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (51,13,'delete_report','Can delete report');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (52,13,'view_report','Can view report');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (2,'auth','permission');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (3,'auth','group');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (4,'contenttypes','contenttype');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (5,'sessions','session');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (6,'quiz','user');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (7,'quiz','category');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (8,'quiz','question');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (9,'quiz','game');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (10,'quiz','friendship');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (11,'quiz','gamequestions');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (12,'quiz','gameanswers');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (13,'quiz','report');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (1,'contenttypes','0001_initial','2019-05-25 15:56:24.259704');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (2,'contenttypes','0002_remove_content_type_name','2019-05-25 15:56:24.572368');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (3,'auth','0001_initial','2019-05-25 15:56:25.766730');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (4,'auth','0002_alter_permission_name_max_length','2019-05-25 15:56:25.860929');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (5,'auth','0003_alter_user_email_max_length','2019-05-25 15:56:25.993088');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (6,'auth','0004_alter_user_username_opts','2019-05-25 15:56:26.113212');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (7,'auth','0005_alter_user_last_login_null','2019-05-25 15:56:26.223268');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (8,'auth','0006_require_contenttypes_0002','2019-05-25 15:56:26.326261');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (9,'auth','0007_alter_validators_add_error_messages','2019-05-25 15:56:26.408205');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (10,'auth','0008_alter_user_username_max_length','2019-05-25 15:56:26.526833');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (11,'auth','0009_alter_user_last_name_max_length','2019-05-25 15:56:26.663856');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (12,'auth','0010_alter_group_name_max_length','2019-05-25 15:56:26.798683');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (13,'auth','0011_update_proxy_permissions','2019-05-25 15:56:26.917255');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (14,'quiz','0001_initial','2019-05-25 15:56:27.089477');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (15,'admin','0001_initial','2019-05-25 15:56:27.532725');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (16,'admin','0002_logentry_remove_auto_add','2019-05-25 15:56:27.666759');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (17,'admin','0003_logentry_add_action_flag_choices','2019-05-25 15:56:27.868539');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (18,'sessions','0001_initial','2019-05-25 15:56:27.993732');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (19,'quiz','0002_user_is_moderator','2019-05-25 15:58:42.055048');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (20,'quiz','0003_user_wants_moderator','2019-05-25 16:08:04.121448');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (21,'quiz','0004_auto_20190527_1236','2019-05-27 12:36:34.376953');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (22,'quiz','0005_friendship_accepted','2019-05-28 00:04:53.490838');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (23,'admin','0004_auto_20190529_0921','2019-05-29 09:55:43.129618');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (24,'admin','0005_auto_20190529_0949','2019-05-29 09:55:43.317296');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (25,'quiz','0006_auto_20190529_1338','2019-05-29 13:39:01.277238');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (26,'quiz','0007_auto_20190602_1447','2019-06-02 14:47:25.233478');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (27,'quiz','0008_auto_20190602_1511','2019-06-02 15:11:41.756757');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (28,'quiz','0009_auto_20190602_1512','2019-06-02 15:12:22.614672');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (29,'quiz','0010_game_num_questions','2019-06-02 16:00:24.866766');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (30,'quiz','0011_auto_20190602_1621','2019-06-02 16:21:38.805721');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (31,'quiz','0007_report','2019-06-06 14:46:25.383988');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (32,'quiz','0012_merge_20190606_1446','2019-06-06 14:46:25.390362');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (33,'quiz','0013_auto_20190606_2218','2019-06-06 20:18:30.833322');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (34,'quiz','0014_user_exp','2019-06-06 20:46:08.244542');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (35,'quiz','0015_auto_20190607_1739','2019-06-07 20:41:21.977148');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (36,'quiz','0016_auto_20190607_2041','2019-06-07 20:41:22.036238');
CREATE INDEX IF NOT EXISTS "quiz_game_player_two_id_d625b613" ON "quiz_game" (
	"player_two_id"
);
CREATE INDEX IF NOT EXISTS "quiz_game_player_three_id_bed86cc0" ON "quiz_game" (
	"player_three_id"
);
CREATE INDEX IF NOT EXISTS "quiz_game_player_one_id_9a61c5b1" ON "quiz_game" (
	"player_one_id"
);
CREATE INDEX IF NOT EXISTS "quiz_game_player_four_id_65fd01b9" ON "quiz_game" (
	"player_four_id"
);
CREATE INDEX IF NOT EXISTS "quiz_game_winner_id_1e2c5e65" ON "quiz_game" (
	"winner_id"
);
CREATE INDEX IF NOT EXISTS "quiz_gamequestions_question_id_7d548c8c" ON "quiz_gamequestions" (
	"question_id"
);
CREATE INDEX IF NOT EXISTS "quiz_gamequestions_game_id_33ea23da" ON "quiz_gamequestions" (
	"game_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "quiz_gamequestions_game_id_index_2e9f4982_uniq" ON "quiz_gamequestions" (
	"game_id",
	"index"
);
CREATE INDEX IF NOT EXISTS "quiz_report_reporter_id_197546d3" ON "quiz_report" (
	"reporter_id"
);
CREATE INDEX IF NOT EXISTS "quiz_report_reported_id_4ab4c6ec" ON "quiz_report" (
	"reported_id"
);
CREATE INDEX IF NOT EXISTS "quiz_gameanswers_user_id_c86c83fc" ON "quiz_gameanswers" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "quiz_gameanswers_game_id_601b62ce" ON "quiz_gameanswers" (
	"game_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "quiz_gameanswers_game_id_user_id_question_index_ba6aa6aa_uniq" ON "quiz_gameanswers" (
	"game_id",
	"user_id",
	"question_index"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "quiz_friendship_second_friend_id_id_b774ffc0" ON "quiz_friendship" (
	"second_friend_id_id"
);
CREATE INDEX IF NOT EXISTS "quiz_friendship_first_friend_id_id_7f953215" ON "quiz_friendship" (
	"first_friend_id_id"
);
CREATE INDEX IF NOT EXISTS "quiz_question_category_id_eeff11ec" ON "quiz_question" (
	"category_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "quiz_user_user_permissions_permission_id_8f8f7ec6" ON "quiz_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "quiz_user_user_permissions_user_id_7235c5dd" ON "quiz_user_user_permissions" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "quiz_user_user_permissions_user_id_permission_id_25000e8c_uniq" ON "quiz_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "quiz_user_groups_group_id_a91cc2d4" ON "quiz_user_groups" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "quiz_user_groups_user_id_8e7316a7" ON "quiz_user_groups" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "quiz_user_groups_user_id_group_id_65337d94_uniq" ON "quiz_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
COMMIT;
