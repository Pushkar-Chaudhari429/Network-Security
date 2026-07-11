from pymongo import MongoClient
uri = "mongodb+srv://meetpushkarchaudhari_db_user:Pushkar123@cluster0.lmm14yt.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Connected successfully")
    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)