import sqlite3
import base64

connection = sqlite3.connect('database.db')

def file_to_BLOB(filename):
	with open(filename, "rb") as file:
		blobData = file.read()
	return blobData

with open('schema.sql') as f:
	connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, password, profile_id) VALUES (?, ?, ?)", ('bofa', 'deez', 69))
cur.execute("INSERT INTO users (username, password, profile_id) VALUES (?, ?, ?)", ('sugo', 'deez', 72))

cur.execute("INSERT INTO profile (pfp, screenname, user_id, follower_list, following_list, post_list, bio) VALUES (?, ?, ?, ?, ?, ?, ?)", (file_to_BLOB("expics/pfp1.jpg"), 'bofadeezSlayer', 420, '2,', '2,', '1,', 'i like ballz'))
cur.execute("INSERT INTO profile (pfp, screenname, user_id, follower_list, following_list, post_list, bio) VALUES (?, ?, ?, ?, ?, ?, ?)", (file_to_BLOB("expics/pfp2.jpg"), 'ChoccyMilkFan', 421, '1,', '2,', '2,', 'choccymilk > bofa milk'))



cur.execute("INSERT INTO posts (media_content, text_content, num_likes, num_dislikes, comment_list, date_posted, author_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (file_to_BLOB("expics/ak_killua.jpg"), 'I hate everyone', 10, 1000, '1,', '12/31/2011', '1,'))
cur.execute("INSERT INTO posts (media_content, text_content, num_likes, num_dislikes, comment_list, date_posted, author_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (file_to_BLOB("expics/choccymilk.jpg"), 'imagine a world without da yummy milk :(', 100000, 1, '2,', '12/31/2011', '2,'))

cur.execute("INSERT INTO comments (media_content, text_content, num_likes, num_dislikes, parent_post_id, date_posted, author_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (file_to_BLOB("expics/ak_killua.jpg"), 'this post is great', 10, 1000, '1,', '12/31/2011', '12,'))

connection.commit()
connection.close()