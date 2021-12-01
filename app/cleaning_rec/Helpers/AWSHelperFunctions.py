from cleaning_rec.Helpers.ExceptionLogging import UberExceptionLogging
import json
import boto3
import os

UberLogString = []

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

class AWSHelperFunctions:

    def __init__(self):
        try:
            #Get configurations from AWSConfig.json
            CleanRecConfig = open('/app/cleaning_rec/Config/CleanRecConfig.json')
            cleanrecconf = json.load(CleanRecConfig)
            
            #Load configurations to necessary variables
            global CleanRecKey, CleanRecSec, CleanRecHome, CleanRecFolder, CSVDownloadPath
            CleanRecKey = cleanrecconf["CleanRec_configs"]["CleanRecKey"]
            CleanRecSec = cleanrecconf["CleanRec_configs"]["CleanRecSec"]
            CleanRecHome = cleanrecconf["CleanRec_configs"]["CleanRecHome"]
            CleanRecFolder = cleanrecconf["CleanRec_configs"]["CleanRecFolder"]

            #Get download path of the CSV file to begin the cleaning record process
            GeneralConfig = open('/app/cleaning_rec/Config/config.json')
            genconf = json.load(GeneralConfig)

            CSVDownloadPath = genconf["configs"]["CSVDownloadPath"]
            #CSVDownloadPath

        except:
            objUberExceptionLogging.UberLogException("Can't load the AWS configurations, Please check if the file is in correct location.", True, True)

        UberLogString.append("AWS and CSV path configurations loaded successfully!!!")    

    #Get the AWS Session for provided AWS Credentials
    def aws_session(self):
        try:
            aws_sess = boto3.session.Session(aws_access_key_id=CleanRecKey,
                                    aws_secret_access_key=CleanRecSec,
                                    region_name=CleanRecHome)
            
            if not aws_sess == None:
                UberLogString.append("AWS Session created successfully!!!")

            return aws_sess

        except:
                objUberExceptionLogging.UberLogException("Can't connect to AWS cloud. Kindly check the credentials again or check the connectivity to Internet", True, True)


    #Upload file to AWS S3 Bucket
    def upload_file_to_s3(self, file_path):
        try:
            session = self.aws_session()
            s3_resource = session.resource('s3')
            file_dir, file_name = os.path.split(file_path)

            bucket = s3_resource.Bucket(CleanRecFolder)
            bucket.upload_file(Filename=file_path, Key=file_name,)
            UberLogString.append(f"file {file_name} uploaded successfully!!!")
            
            return UberLogString
        except:
            objUberExceptionLogging.UberLogException("An ERROR occured while uploading the file. Please check if internet is connected or not.", True, True)
     
     #s3_url = upload_file_to_s3('cleaningrecordsrideshare', './CSV/UberTripData.csv')
     #    
    #Upload raw csv from AWS S3 Bucket to the local machine for further processing.
    def download_file_from_s3(self, download_file_name):
        try:
            session = self.aws_session()
            s3_resource = session.resource('s3')
            bucket = s3_resource.Bucket(CleanRecFolder)
            csv_destination_path = f'{CSVDownloadPath}{download_file_name}' 
            bucket.download_file(Key=download_file_name, Filename=csv_destination_path)
            file_name = download_file_name
        except:
            objUberExceptionLogging.UberLogException("An ERROR occured while downloading the file. Please check if internet is connected or not.", True, True)

        UberLogString.append(f"file {file_name} downloaded successfully to {csv_destination_path}.")
        
        return UberLogString

