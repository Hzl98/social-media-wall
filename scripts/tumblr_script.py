import requests
import MySQLdb
import pytumblr

db = MySQLdb.connect(
	host = "sql143.main-hosting.eu",
	user = "u522840214_hanzelwp",
	passwd = "m2p+XsvRr6N+",
	db = "u522840214_TAhanzel"
)

client = pytumblr.TumblrRestClient(
    'LuO1Ama1TbgSouATB69fdbnvce6NDViQuT6RS9exqBCq8uLLpe',
    'bVZgrjCTokJ0AMtbTKE89HkDgSCt3QJ2e7Qr1gGGbOJXqDRbi1',
    'Xcdodj1iFYq5dcNzihJAGi057GLx7VG1EXJSmevMt8fjrDly0o',
    '0PWKhhXWvNd0eQx5bQpWvXJru9hhVh8jLD7wHhpGfsRtJBsLD3',
)

cr = db.cursor()
cr_i = db.cursor()
cr.execute("select * from wall_sources where source = 'Tumblr'")
src_list = cr.fetchall()
i = 0
# url = "https://graph.facebook.com/v9.0/103865104878369/feed?access_token=EAAGmlSiUPsYBACCrFHZBHYkHjlhidF6x3nWG7KEOH12euuUYvc7AphuT8cydKmX6RqPVlSwzg61ZA5W8jjjhDAbxgvsLeQkbzBoOnowPcsex0MHDqk9wl3LVqGtZAedQ6v9jcdhMYtOn1JkRAnInZB9m0ilVCcd9gLD0XAleDSPOiqrubLHb"
# resp = requests.get(url = url)
# result = resp.json()

for src in src_list:
	print(src[2])
	print("\n")
	posts = client.posts(src[2], filter = "text")
	print(posts)
	for post in posts['posts']:
		print(post['body'])
		print(len(posts['posts']))
		print(src[4])
		if len(posts['posts']) - i > src[4]:
			
			str_date_created = str(post['date'])[0:10]
			cr_i.execute("insert into wall_post values(0, '', '" + str_date_created + "', '" + post['title'] + "', 1, '" + '' + "', 'Tumblr', " + str(src[3]) + ")")
			print(post['title'])

		print("\n")
		# sp_id = post['id'].split('_')
		cr.execute("update wall_sources set last_id = " + str(len(posts['posts'])) + " where id = " + str(src[0]))
	i = i + 1

db.commit()
