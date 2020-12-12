import tweepy
import MySQLdb

db = MySQLdb.connect(
	host = "localhost",
	user = "root",
	passwd = "",
	db = "dbtugasakhir"
)

api_key = '0XkJgeSdu5IjPdTNuKIKwJvk6'
api_secret_key = '15XXdj61iw5hz1V900DKFFF1E8Zmxgg1iurFzICSV2cfWLqKY5'
access_token = '1218863029242093568-CBlyZXHvkMOzifpX5XknTPY32GMMZj'
access_token_secret = 'EzYRGCgJdewfMpgf1NSTCRnD9Kly1irSGTTEBysSC3tPZ'

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

cr = db.cursor()
cr_i = db.cursor()
cr.execute("select * from wall_sources where source = 'Twitter'")
src_list = cr.fetchall()

for src in src_list:
	print(src[2])
	tweets = api.search(q = src[2], type = 'recent', since_id = src[4])
	if len(tweets) > 0:
		for tweet in tweets:
			if src[2] in tweet.text:
				d_y = tweet.created_at.year
				d_d = tweet.created_at.day
				d_m = tweet.created_at.month
				cr_i.execute("insert into wall_post values(0, '', '" + str(d_y) + "-" + str(d_m) + "-" + str(d_d) + "', '" + tweet.text + "', 1, '" + tweet.author.name + "', 'Twitter', " + str(src[3]) + ")")
				print(tweet.text)
				print(tweet.id)
				
		print("\n")
		cr.execute("update wall_sources set last_id = " + str(tweets[0].id) + " where id = " + str(src[0]))

db.commit()