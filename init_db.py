import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
	connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, password, profile_id) VALUES (?, ?, ?)", ('bofa', 'deez', 69))

cur.execute("INSERT INTO profile (screenname, user_id, follower_list, following_list, post_list) VALUES (?, ?, ?, ?, ?)", ('bofadeezSlayer', 420, '12,', '13,', '21,'))

cur.execute("INSERT INTO posts (text_content, num_likes, num_dislikes, comment_list, date_posted, author_id) VALUES (?, ?, ?, ?, ?, ?)", ('I hate everyone', 10, 1000, '13,', '12/31/2011', '12,'))

cur.execute("INSERT INTO comments (text_content, num_likes, num_dislikes, parent_post_id, date_posted, author_id) VALUES (?, ?, ?, ?, ?, ?)", ('I hate everyone', 10, 1000, '1,', '12/31/2011', '12,'))

connection.commit()
connection.close()