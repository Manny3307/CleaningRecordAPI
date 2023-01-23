import json
import os,sys
from fpdf.html import HTML2FPDF
import pandas as pd
import numpy as np
from datetime import datetime as dt, timedelta
import random
import ast
from sqlalchemy import create_engine
import sqlalchemy as db
from time import sleep
from json import dumps
import redis
import websocket
import time
import boto3
from pathlib import Path
from fpdf import FPDF, HTMLMixin
from confluent_kafka import Producer, Consumer
from time import sleep
import PyPDF2 as pypdf

'''
class ExampleProducer:
    broker = "localhost:9092"
    topic = "appmsg"
    producer = None

    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': self.broker,
            'socket.timeout.ms': 100,
            'api.version.request': 'false',
            'broker.version.fallback': '0.9.0',
        }
        )

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(
                msg.topic(), msg.partition()))

    def send_msg_async(self, msg):
        print("Send message asynchronously")
        self.producer.produce(
            self.topic,
            msg,
            callback=lambda err, original_msg=msg: self.delivery_report(err, original_msg
                                                                        ),
        )
        self.producer.flush()

    def send_msg_sync(self, msg):
        print("Send message synchronously")
        self.producer.produce(
            self.topic,
            msg,
            callback=lambda err, original_msg=msg: self.delivery_report(
                err, original_msg
            ),
        )
        self.producer.flush()'''

'''example_producer = ExampleProducer()
message = "Cleaning Records generation initiated"
example_producer.send_msg_sync(message)
'''
'''

class ExampleConsumer:
    broker = "localhost:9092"
    topic = "appmsg"
    group_id = "consumer-1"

    def start_listener(self):
        consumer_config = {
            'bootstrap.servers': self.broker,
            'group.id': self.group_id,
            'auto.offset.reset': 'largest',
            'enable.auto.commit': 'false',
            'max.poll.interval.ms': '86400000'
        }

        consumer = Consumer(consumer_config)
        consumer.subscribe([self.topic])

        try:
            while True:
                print("Listening")
                # read single message at a time
                msg = consumer.poll(0)
                

                if msg is None:
                    sleep(5)
                    continue
                if msg.error():
                    print("Error reading message : {}".format(msg.error()))
                    continue
                # You can parse message and save to data base here
                print(msg.value())
                consumer.commit()

        except Exception as ex:
            print("Kafka Exception : {}", ex)

        finally:
            print("closing consumer")
            consumer.close()

#RUNNING CONSUMER FOR READING MESSAGE FROM THE KAFKA TOPIC
my_consumer = ExampleConsumer()
my_consumer.start_listener()'''


# Import the required Module
#import tabula
# Read a PDF File
#df = tabula.read_pdf("/home/manny/Uber_Statements/20Dec-2Jan_2021/dec27-jan3.pdf", pages='all')

# convert PDF into CSV
#tabula.convert_into("/home/manny/Uber_Statements/20Dec-2Jan_2021/dec27-jan3.pdf", "/home/manny/Uber_Statements/20Dec-2Jan_2021/dec27-jan3.csv", output_format="csv", pages='all')
#print(df)

#print(df["Processed"][:3])
#list1 = []
#for item in df[2]:
#    print(item)
    



#getdatetime('71    Fri, Dec 3TipA$5.00A$5.00\r5 11 PMDec 3 5 10 P')


#.apply(lambda x: self.UberSplitDateTime(x, random.randint(lower_time_range,upper_time_range)))

#Mon, Dec 27 A$33.72\n3 38 AMDec 27 3 37 AM
#Mon, Dec 27 A$7.25A$7.254 56 AMDec 27 4 31 AMA$26.50
#Sat, Jan 1A$18.96A$18.965 35 AMJan 1 5 35 AMA$875.63
#"24 Aug, 2021 04:15 PM"

def getdatetime(str):
    test = str[31:]
    test1 = test[:14]
    if "Dec" not in test1:
        test1 = "Dec " + test1

    if "Dec Jan" in test1:
        test1 = test1.replace("Dec Jan", "Jan")

    if "AMA" in test1:
        test1 = test1.replace("AMA", "AM")
    finalstr = test1.split(" ")
    print(finalstr)
    #finalstr1 = f"{finalstr[1]} {finalstr[0]}, 2021 {finalstr[2]}:{finalstr[3]} {finalstr[4]}"

    #if "Jan" in finalstr1:
    #    finalstr1 = finalstr1.replace("2021", "2022")

    return finalstr
    #print(finalstr)
#print(getdatetime("Mon, Dec 27 A$7.25A$7.254 56 AMDec 27 4 31 AMA$26.50"))
#print(getdatetime("Sat, Jan 1A$18.96A$18.965 35 AMJan 1 5 35 AMA$875.63"))
#print(getdatetime("Mon, Dec 27 A$33.72\n3 38 AMDec 27 3 37 AM"))

#######

#df = pd.read_csv('/home/manny/Uber_Statements/20Dec-2Jan_2021/DateTimeTrips.csv')
#df["DateTimeTrip"] = df["DateTimeTrip"].str.replace("UberX", " ")
#print(df["DateTimeTrip"])
#print(df["DateTimeTrip"].apply(lambda x: getdatetime(x)))
lines = []
with open('/home/manny/Uber_Statements/20Dec-2Jan_2021/DateTimeTrips_1.txt') as f:
    for num, line in enumerate(f, 1):
        str1 = line.split(" ") 
        AMPM = str1[4].split("\\")[0] 
        finalstr = f"{str1[1]} {str1[0]}, 2021 {str1[2]}:{str1[3]} {AMPM}" 
        if "Jan" in finalstr:
            finalstr = finalstr.replace("2021", "2022")
        lines.append(finalstr[:20])
        #print(lines)

df  = pd.DataFrame()
df["DateTimeTrip"] = lines
print(df)
df.to_csv("/home/manny/Uber_Statements/20Dec-2Jan_2021/uber_driving_records.csv")

#"24 Aug, 2021 04:15 PM"

#######

#print(df["Processed"])
#df["Processed"].apply(lambda x: getdatetime(x))
#print(df["Processed"].apply(lambda x: getdatetime(x)))

#print(df.loc[df['Processed'].str.contains("\r", case=False)])
#pokemon_og_games = df.loc[df['Processed'].str.contains("\r", case=False)]
#pokemon_og_games = pokemon_og_games.loc[1:]

#######


'''
pokemon_og_games = df

def encrypt(string, length):
    return ' '.join(string[i:i+length] for i in range(0,len(string),length))

for item in df["Processed"]:
    i = item.split(' ')
    print(f"{i[1]} {i[0]}, 2021 {i[2]} {i[3]}")
'''
#######


#"24 Aug, 2021 04:15 PM"
#Sun, Dec 12 

#print(pokemon_og_games)
'''def getdatetime(str):
    test = str.split('\r')
    test3 = test[1].split(' ')
    test4 = test3[5:] 
    test2 = test4[:6] 
    #print(f"Test2 = {test2}")
    finalstr = f"{test2[1]} {test2[0]}, 2021 {test2[3]}:{test2[4]} {test2[5]}"
    return finalstr
    #print(finalstr)


#pokemon_og_games1 = pokemon_og_games["Processed"].apply(lambda x: getdatetime(x))

#df = df.loc[df['Processed'].str.contains("A", case=False)]
pokemon_og_games['Processed'] = pokemon_og_games['Processed'].str.replace("Dec", " Dec")
pokemon_og_games['Processed'] = pokemon_og_games['Processed'].str.replace("Dec 10" , " Dec 10 ")
pokemon_og_games['Processed'] = pokemon_og_games['Processed'].str.replace("Dec 11" , " Dec 11 ")
pokemon_og_games['Processed'] = pokemon_og_games['Processed'].str.replace("Dec 12" , " Dec 12 ")
pokemon_og_games['Processed'] = pokemon_og_games['Processed'].str.replace("AM" , "AM ")
pokemon_og_games['Processed'] = pokemon_og_games['Processed'].str.replace("PM" , "PM ")
#20, 19 , 18, 17, 11, 12, 10
#print(pokemon_og_games["Processed"].apply(lambda x: getdatetime(x)))
pk1 = pokemon_og_games["Processed"].apply(lambda x: getdatetime(x))
print(pk1)
pk1.to_csv("/home/manny/Uber_Statements/temp1.csv")
#print(pokemon_og_games)
#print()

def formatdatetime(str):
    test = str.split(' ')
    test1 = test[5:] 
    test2 = test1[:6] 
    finalstr = f"{test2[1]} {test2[0]}, 2021 {test2[3]}:{test2[4]} {test2[5]}"
    print(finalstr)
'''

'Sun, Dec 5UberXA$24.15A$24.15\r4 39 PMDec 5 4 39 PMA$881.62'
'Fri, Dec 3UberXA$13.07A$13.07\r4 50 PMDec 3 4'

#formatdatetime('4 50 PM   Dec 3  4 50 PM A$13.07')

#print(pokemon_og_games["Processed"].apply(lambda x: formatdatetime(x)))

#4 50 PM   Dec 3  4 50 PM A$13.07

#"24 Aug, 2021 04:00 PM"
#"24 Aug, 2021 04:15 PM"

'''temp = {'Ritika': 5, 'Sam': 7, 'John': 10, 'Aadi': 8}
#print(temp['Aadi'])


#Get the fields of the Database Configuration from the Config File
GenConfig = open('/home/manny/cleaning_records_API/CleaningRecordAPI/app/cleaning_rec/Config/config.json')
genconf = json.load(GenConfig)

DBConfig = open('/home/manny/cleaning_records_API/CleaningRecordAPI/app/cleaning_rec/Config/DBConfig.json')
dbconf = json.load(DBConfig)

DBConnector = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["DBConnecter"]
UserName = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["UserName"]
Password = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["Password"]
ServerOrEndPoint = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["ServerOrEndPoint"]
DatabaseName = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["DatabaseName"]
AuthenticationPlugin = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["AuthPlugin"]

driver = {}
engine = db.create_engine(f"{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}?{AuthenticationPlugin}", encoding='utf8')
connection = engine.connect()
metadata = db.MetaData()
uber_driver = db.Table('core_uberdriver', metadata, autoload=True, autoload_with=connection)
query = db.select([uber_driver]) 
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet[:3])

for rec in ResultSet[:3]:
    driver[rec[2]] = rec[0]
    
print(driver)

df = pd.read_csv('/home/manny/cleaning_records_API/CleaningRecordAPI/app/cleaning_rec/CSV/UberTripData.csv')

df["Name"] = np.where(df['Name']=='Manmeet', 1, df["Name"])

print(df)
'''



'''import docker

client = docker.DockerClient()
container = client.containers.get("cleaningrecordapi_db_1")
ip_add = container.attrs['NetworkSettings']['Networks']['cleaningrecordapi_default']["IPAddress"]
print(ip_add)
'''
#fpath = Path('cleaningrecord').absolute()



#ROOT_DIR = os.path.abspath("../../cleaningrecord")
#print(ROOT_DIR)

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