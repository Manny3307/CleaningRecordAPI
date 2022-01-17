from cleaning_rec.Helpers.ExceptionLogging import UberExceptionLogging
from cleaning_rec.Helpers.FolderFunctions import FolderFunction
from cleaning_rec.Helpers.DataFrameFunctions import DataFrameFunction
from cleaning_rec.Helpers.DatabaseFunctions import dbFunction
from cleaning_rec.Helpers.HTMLFunctions import HTMLFunctions
from cleaning_rec.Helpers.PDFFunctions import PDFFunctions
from cleaning_rec.Helpers.AWSHelperFunctions import AWSHelperFunctions
from cleaning_rec.Helpers.KafkaHelperFunctions import KafkaFunctions

import time

UberLogString = []

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

#Load Exception Messages
ExceptionMessages = objUberExceptionLogging.load_exception_success("Exception")

#Load the Success Messages
SuccessMessages = objUberExceptionLogging.load_exception_success("Success")

#objKafka = KafkaFunctions()


class UberCleaningRecordBuilder:
    
    def __init__(self) -> None:
        pass


    def execRecordBuilderFunctionality(self, folderName, csv_driver_record_file):
        
        
        #Create Instance of AWSHelperFunctions class
        AWSHelper = AWSHelperFunctions()

        #Download the CSV file containing date and time of completed trips
        AWSLogString = AWSHelper.download_file_from_s3(csv_driver_record_file)        
        UberLogString.append(AWSLogString)
        #objKafka.produce_kafka_message("Establishing connection to AWS and downloaded the file API.")

        #Create an Instance of FolderFunctions Class
        UberFolderFunction = FolderFunction()

        #Create the Uber folder Structure and copy the required files in this folder structure
        FolderLogString = UberFolderFunction.create_folder_structure(folderName, csv_driver_record_file)
        UberLogString.append(FolderLogString)
        #objKafka.produce_kafka_message("Folder Structure Created successfully")

        #Create an Instance of DataFrameFunctions Class
        UberDataFrameFuntion = DataFrameFunction()

        #Get the Final DataFrame with all the data about Cleaning record for the fortnight.
        final_df = UberDataFrameFuntion.create_final_df(folderName)
        UberLogString.append(UberDataFrameFuntion.get_DataFrameFuntions_LogString())
        #objKafka.produce_kafka_message("Final dataframe fetched after populating it.")
        
        #Send the records to database
        datafunctions = dbFunction()
        UberLogString.append(datafunctions.send_DB_records(final_df))
        #objKafka.produce_kafka_message("Data successfully sent to Database")

        #Rename the Final DataFrame colums to match with CPVV standards
        final_df = UberDataFrameFuntion.rename_df_columns()

        #Get the HTML templates from the respective files and concatenate them to form one single HTML file.
        HTMLfunc = HTMLFunctions()
        UberLogString.append(HTMLfunc.HTML_template(final_df, folderName))
        #objKafka.produce_kafka_message("Create the final HTML file from the records.")

        #Create the PDF for the final HTML formed in the HTML folder of the User provided Folder Name.
        objPDFFunction = PDFFunctions()
        UberLogString.append(objPDFFunction.create_PDF(folderName))
        #objKafka.produce_kafka_message("PDF containing the cleaning records created successfully.")

        #Send the Final Log Uber Log file
        objUberExceptionLogging.create_prog_log(UberLogString)