import pyrebase
# from google.cloud import storage

config = {
  "apiKey" : "AIzaSyD1teLmwDHaJ4vWUPdI-QqywM4vsb9HVG4",
  "authDomain" : "nodejs-learning-b6d94.firebaseapp.com",
  "databaseURL" : "https://nodejs-learning-b6d94.firebaseio.com",
  "projectId" : "nodejs-learning-b6d94",
  "storageBucket" : "nodejs-learning-b6d94.appspot.com",
  "messagingSenderId" : "972133840846",
  "appId" : "1:972133840846:web:93dc363cb3084da8439d9f",
  "measurementId" : "G-YEJHCFK7SN"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

file = "tumblr_pazrdhHdQM1uvi4xwo1_1280.png"
# format = file[-4:]
dest = "img/wall/" + file
upload_img = storage.child(dest).put(file)
img_url = storage.child(dest).get_url(upload_img['downloadTokens'])
print(img_url)
f = open("url.txt", "w")
f.write(img_url)
f.close()


