import json
import os,sys
import pandas as pd
from datetime import datetime as dt, timedelta
import random
import ast
from sqlalchemy import create_engine
from time import sleep
from json import dumps

import redis
import websocket
import time
import boto3

AWSConfig = open('./Config/AWSConfig.json')
awsconf = json.load(AWSConfig)

AWS_ACCESS_KEY_ID = awsconf["AWS_configs"]["AWS_ACCESS_KEY_ID"]
AWS_ACCESS_KEY_SECRET = awsconf["AWS_configs"]["AWS_ACCESS_KEY_SECRET"]
AWS_S3_REGION_NAME = awsconf["AWS_configs"]["AWS_S3_REGION_NAME"]

print(AWS_ACCESS_KEY_ID)
print(AWS_ACCESS_KEY_SECRET)
print(AWS_S3_REGION_NAME)


def aws_session():
    return boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_ACCESS_KEY_SECRET,
                                region_name=AWS_S3_REGION_NAME)

def upload_file_to_s3(bucket_name, file_path):
    session = aws_session()
    s3_resource = session.resource('s3')
    file_dir, file_name = os.path.split(file_path)

    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_file(
      Filename=file_path,
      Key=file_name,
    )

    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    return s3_url

#s3_url = upload_file_to_s3('cleaningrecordsrideshare', './CSV/UberTripData.csv')

#print(s3_url) 


def download_file_from_s3(bucket_name, s3_key, destination_path):
    session = aws_session()
    s3_resource = session.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    bucket.download_file(Key=s3_key, Filename=destination_path)

download_file_from_s3('cleaningrecordsrideshare', 'UberTripData.csv', './CSV/data_download.csv')


'''GenConfig = open('./Config/config.json')
genconf = json.load(GenConfig)

DBConfig = open('./Config/DBConfig.json')
dbconf = json.load(DBConfig)

DBConnector = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["DBConnecter"]

print(DBConnector)
'''
'''engine = create_engine('postgresql://postgres:mal486@172.18.0.2:5432/app')
engine.execute("INSERT INTO core_uberdriver(driver_first_name,driver_last_name,driver_email) VALUES('Manmeet','Arora','Manmeet@manny.com')")
'''#print(engine.logging_name)
'''ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1:8000/appmsg/")
for i in range(10):
    ws.send(json.dumps({'value': f'Hi - {i}'}))

'''
'''publisher = redis.Redis(host = 'localhost', port = 6379)
message=""
channel = "test"
while(message!="exit"):
 message = input("")
 send_message = "Python : " + message
 publisher.publish(channel, send_message)
'''



'''

path = "./Config/FolderStructure.json"
folders = {}
folder1 = {}
with open(path, 'r') as f:
    folders = json.load(f)

print(folders["folder_name"])
folder1["Temp1"] = folders["folder_name"]
print(folder1)
'''
'''
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

for e in range(100):
    data = {'number' : e}
    producer.send('mallory', value=data)
    #sleep(5)
/*'''
'''

f = open('./Config/config.json')
data = json.load(f)

#print(data["configs"]["BasePath"])
#print(data["configs"]["HTMLHeaderTemplate"])

f.close()
'''

#print(os.name)
#print(sys.platform)
#print(os.getcwd())

#foldertoCreate = input("Please Enter the name of the Folder")
'''
foldertoCreate = "/Temps"
# Load the Config JSON file from the config folder and read the respective values
#FolderConfigJSON = open('./Config/folder_config.json')
#CreateConfigData = json.load(FolderConfigJSON)

# Get The Base Path from the Config File.
CreateBasePath = "/Uber Cleaning Record"
BuildPath = "/UberBuild"
CreateHTMLHeaderTemplate = "UberCleaningRecordHeaderTemplate.html"
CreateHTMLFooterTemplate = "UberCleaningRecordFooterTemplate.html"
CreateHTMLFolder = "HTML"
CreateCSVFolder = "CSV"
'''
'''
#print(os.path.exists('/Uber Cleaning Record'))
files = os.listdir(CreateBasePath)
pathfile=os.path.dirname(CreateBasePath)
#print(pathfile)
mypath = os.path.join(CreateBasePath, "Temp")
#print(mypath)
#files = os.listdir(mypath)
#print(files)
'''
'''
folderName = input("Please Enter the name of the Folder: ")

#dirName = CreateBasePath + folderName
#CSVDirName = dirName + CreateCSVFolder
dirName = os.path.join(CreateBasePath, folderName)

# Create target Directory
if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Directory " , dirName ,  " Created ") 
    
    HTMLDirName = os.path.join(dirName, CreateHTMLFolder)
    #Create "HTML" directory
    if not os.path.exists(HTMLDirName):
        os.makedirs(HTMLDirName)
        print("Directory " , HTMLDirName ,  " Created ")
    else:
        print("Directory " , HTMLDirName ,  " already exists")  
    
    CSVDirName = os.path.join(dirName, CreateCSVFolder)
    #Create "CSV" directory
    if not os.path.exists(CSVDirName):
        os.makedirs(CSVDirName)
        print("Directory " , CSVDirName ,  " Created ")
    else:
        print("Directory " , CSVDirName ,  " already exists")      
else:
    print("Directory " , dirName ,  " already exists")  

'''

'''
FolderConfigJSON = open('./Config/folder_config.json')
ConfigData = json.load(FolderConfigJSON)

#HTMLFilestoCopy = ConfigData['folder_configs']['HTMLFiles']['HTMLFilesToCopy']['CleaningRecordHeader']
#print(f"Uber Cleaning Header Template = {HTMLFilestoCopy}")

#Set the Upper and Lower Limit for Time Substraction
lower_time_range = 2
upper_time_range = 8 

#Calculate the clean time for Uber Trips
def UberSplitDateTime(UberDateTime, TimeInMinutes):
    x = UberDateTime.split()
    UberTime = x[3]
    UberTime = dt.strptime(UberTime, '%H:%M')
    CleanTime = UberTime - timedelta(minutes = TimeInMinutes)
    FinalDateandCleanTime = x[0] + " " + x[1] + " " + x[2] + " " + CleanTime.strftime("%H:%M") + " " + x[4]
    return FinalDateandCleanTime 

#print(UberSplitDateTime("July 9, 2021 05:10 PM",5))

#df = pd.read_csv("./CSV/UberTripData.csv")
#print(df.head(5))

#df1 = pd.DataFrame()


DataFrameConf = open('./Config/DataFrameConfig.json')
dataconf = json.load(DataFrameConf)

#for (k, v) in dataconf.items():
#    if v["IsEval"] == True:
#        df1[v["dfColumn"]] = eval(v["Value"])
#    else:
#        df1[v["dfColumn"]] = v["Value"]


#print(df1)
#df1.to_csv("test.csv",index=False)
   
import mysql.connector
   

# Usefull Code 
# Credentials to database connection
hostname="manny-uber-records.cwl0oxqn3sec.us-east-2.rds.amazonaws.com"
dbname="manny_uber_records_2021"
uname="admin"
pwd="mallory_486"

# Create dataframe
df = pd.DataFrame(data=[[111,'Thomas','35','United Kingdom'],
		[222,'Ben',42,'Australia'],
		[333,'Harry',28,'India']],
		columns=['id','name','age','country'])

# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine("mysql+mysqlconnector://angel:Angel_486@localhost/manny_uber_records_2021?auth_plugin=mysql_native_password")
print("connected")

# Convert dataframe to sql table                                   
#df.to_sql('UberCleaningRecords', con=engine, index=False)
engine.execute("select * from UberCleaningRecords").fetchall()

import pandas as pd
from sqlalchemy import create_engine
 
# set your parameters for the database
user = "user"
password = "password"
host = "abc.efg.hij.rds.amazonaws.com"
port = 3306
schema = "db_schema"
 
# Connect to the database
conn_str = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4'.format(
    user, password, host, port, schema)
db = create_engine(conn_str, encoding='utf8')
connection = db.raw_connection()
 
# define parameters to be passed in and out
parameterIn = 1
parameterOut = "@parameterOut"
try:
    cursor = connection.cursor()
    cursor.callproc("storedProcedure", [parameterIn, parameterOut])
    # fetch result parameters
    results = list(cursor.fetchall())
    cursor.close()
    connection.commit()
finally:
    connection.close() 
    '''

'''
#Create an environment for Uber Records
RUN conda create --name uberrecords python=3.9.6
RUN pip install pandas matplotlib seaborn scikit-learn
SHELL ["/bin/bash", "--login", "-c"]
RUN conda activate uberrecords
'''