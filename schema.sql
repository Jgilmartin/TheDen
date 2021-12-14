DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS comments;

CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	password TEXT NOT NULL,
	profile_id INTEGER NOT NULL,
	FOREIGN KEY (profile_id) REFERENCES profile(id)
);

CREATE TABLE profile (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	screenname TEXT NOT NULL,
	user_id INTEGER NOT NULL,
	follower_list TEXT NOT NULL,
	following_list TEXT NOT NULL,
	post_list TEXT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users (id)
);


CREATE TABLE posts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	text_content TEXT NOT NULL,
	num_likes INTEGER NOT NULL,
	num_dislikes INTEGER NOT NULL,
	comment_list TEXT NOT NULL,
	date_posted TEXT NOT NULL,
	author_id INTEGER NOT NULL,
	FOREIGN KEY (author_id) REFERENCES profile(id)
);


CREATE TABLE comments (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	text_content TEXT NOT NULL,
	num_likes INTEGER NOT NULL,
	num_dislikes INTEGER NOT NULL,
	author_id INTEGER NOT NULL,
	date_posted TEXT NOT NULL,
	parent_post_id INTEGER NOT NULL,
	FOREIGN KEY (author_id) REFERENCES profile (id),
	FOREIGN KEY (parent_post_id) REFERENCES posts (id)
);