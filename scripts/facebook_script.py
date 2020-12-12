import requests
import MySQLdb

db = MySQLdb.connect(
	host = "localhost",
	user = "root",
	passwd = "",
	db = "dbtugasakhir"
)

cr = db.cursor()
cr_i = db.cursor()
cr.execute("select * from wall_sources where source = 'Facebook'")
src_list = cr.fetchall()
url = "https://graph.facebook.com/v9.0/103865104878369/feed?access_token=EAAGmlSiUPsYBACCrFHZBHYkHjlhidF6x3nWG7KEOH12euuUYvc7AphuT8cydKmX6RqPVlSwzg61ZA5W8jjjhDAbxgvsLeQkbzBoOnowPcsex0MHDqk9wl3LVqGtZAedQ6v9jcdhMYtOn1JkRAnInZB9m0ilVCcd9gLD0XAleDSPOiqrubLHb"
resp = requests.get(url = url)
result = resp.json()

for src in src_list:
	print(src[2])
	for post in result['data']:
		if src[2] in post['message']:
			str_date_created = str(post['created_time'])[0:10]
			cr_i.execute("insert into wall_post values(0, '', '" + str_date_created + "', '" + post['message'] + "', 1, '" + '' + "', 'Facebook', " + str(src[3]) + ")")
			print(post['message'])

		print("\n")
		sp_id = post['id'].split('_')
		cr.execute("update wall_sources set last_id = " + sp_id[1] + " where id = " + str(src[0]))

db.commit()
