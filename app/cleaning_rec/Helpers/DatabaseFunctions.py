from django.db import connection
import sqlalchemy as db
from cleaning_rec.Helpers.ExceptionLogging import UberExceptionLogging
from sqlalchemy import create_engine, orm
from sqlalchemy.schema import FetchedValue
import mysql.connector
import json
import numpy as np

UberLogString = []

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

#Load Exception Messages
ExceptionMessages = objUberExceptionLogging.load_exception_success("Exception")

#Load the Success Messages
SuccessMessages = objUberExceptionLogging.load_exception_success("Success")

#Perform the database functions to send the data to database.
class dbFunction:
    
    def __init__(self):
        try:
            #Get the fields of the Database Configuration from the Config File
            GenConfig = open('/app/cleaning_rec/Config/config.json')
            genconf = json.load(GenConfig)
            
            DBConfig = open('/app/cleaning_rec/Config/DBConfig.json')
            dbconf = json.load(DBConfig)

            global DBConnector, UserName, Password, ServerOrEndPoint, DatabaseName, AuthenticationPlugin, engine
            DBConnector = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["DBConnecter"]
            UserName = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["UserName"]
            Password = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["Password"]
            ServerOrEndPoint = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["ServerOrEndPoint"]
            DatabaseName = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["DatabaseName"]
            AuthenticationPlugin = dbconf["DBConfigs"][genconf["configs"]["DBName"]]["AuthPlugin"]
            
            #AuthPlugin = auth_plugin=mysql_native_password
            #engine = create_engine(f"{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}", encoding='utf8')
        except:
            objUberExceptionLogging.UberLogException(ExceptionMessages["Exceptions"]["Database_config"], True, True)

        UberLogString.append(SuccessMessages["Messages"]["database_config"])
        UberLogString.append("Connecting to Database")

    def send_DB_records(self, final_df):
        
        try:
            # Create SQLAlchemy engine to connect to MySQL Database
            engine = create_engine(f"{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}?{AuthenticationPlugin}", encoding='utf8')
            print("Connecting to Database")

            UberLogString.append("Sending Records to database....")
            print("Sending Records to database....")

            # Convert dataframe to sql table                                   
            final_df.to_sql('core_ubertempcleaningrecords', engine, if_exists='append', index=False)
            
            self.process_and_save_cleaning_records(final_df)
        except:
            objUberExceptionLogging.UberLogException("ERROR: Cleaning Records could not be sent to UberTempCleaningRecords.", False, False) 
        finally:
            UberLogString.append("Records sent to database successfully")
            print("Records sent to database successfully")

        return UberLogString
    
    def process_and_save_cleaning_records(self, final_df):
        
        try:
            # Create SQLAlchemy engine to connect to MySQL Database
            engine = create_engine(f"{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}?{AuthenticationPlugin}", encoding='utf8')
            UberLogString.append("Transferring records to UberCleaningRecords....")
            driver_ids = self.get_driver_ids()
            certificate_ids = self.get_certificate_ids()
            
            for driverid, dval in driver_ids.items():
                final_df["Driver_name"] = np.where(final_df['Driver_name']== driverid, dval, final_df["Driver_name"])

            for certificateid, cval in certificate_ids.items():
                final_df["Driver_certificate_number"] = np.where(final_df['Driver_certificate_number']== certificateid, cval, final_df["Driver_certificate_number"])
            
            cleaning_records_df = final_df

            # Convert dataframe to sql table    
            cleaning_records_df.rename(columns={'Driver_name':'driver_id_id', 'Driver_certificate_number': 'driver_certificate_id', 
                                                'Passenger_hightouch_surfaces_cleaned': 'passenger_high_touch_surfaces',
                                                'Driver_hightouch_surfaces_cleaned':'driver_high_touch_surfaces'}, inplace = True)                                 
            cleaning_records_df.to_sql('core_ubercleaningrecords', engine, if_exists='append', index=False)
            
        except:
            objUberExceptionLogging.UberLogException("ERROR: Cleaning Records could not be sent to UberCleaningRecords.", False, False) 
        finally:
            engine = None
            
    def save_dataframe_to_db(self, final_df, table_name):
        try:
            # Create SQLAlchemy engine to connect to MySQL Database
            engine = create_engine(f"{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}?{AuthenticationPlugin}", encoding='utf8')
            UberLogString.append("Sending Records to database....")
            # Convert dataframe to sql table                                   
            final_df.to_sql(table_name, engine, if_exists='append', index=False)
        except:
            objUberExceptionLogging.UberLogException(f"ERROR: Records can't be sent to {table_name}.", False, False) 
            

    def get_db_connection(self):
        try:
            engine = db.create_engine(f"{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}?{AuthenticationPlugin}", encoding='utf8')
            connection = engine.connect()
            return connection
        except:
            objUberExceptionLogging.UberLogException(f"ERROR: Connection cannot be established with the database.", False, False) 
        

    def get_driver_ids(self):
        driver = {}
        try:
            conn = self.get_db_connection()
            metadata = db.MetaData()
            uber_driver = db.Table('core_uberdriver', metadata, autoload=True, autoload_with=conn)
            query = db.select([uber_driver]) 
            query = db.select([uber_driver]) 
            ResultProxy = conn.execute(query)
            ResultSet = ResultProxy.fetchall()

            for rec in ResultSet[:3]:
                driver[rec[2]] = rec[0]
            
            return driver
        except:
            objUberExceptionLogging.UberLogException(f"ERROR: Connection cannot be established with the database.", False, False) 

    def get_certificate_ids(self):
        certificate = {}
        try:
            engine = db.create_engine(f"{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}?{AuthenticationPlugin}", encoding='utf8')
            connection = engine.connect()
            result= connection.execute("SELECT * FROM core_uberdrivercpvvcertificate")
            
            for row in result:
                certificate[row[1]] = row[2]
            
            return certificate
        except:
            objUberExceptionLogging.UberLogException(f"ERROR: Connection cannot be established with the database.", False, False) 
