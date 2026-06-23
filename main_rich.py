from engine import SERVER

cloud_flare = SERVER("cloud_flare", ip="1.1.1.1", threshold=90)
Google = SERVER("Google_DNS", ip="8.8.8.8", threshold=90)
Google.check_network()
