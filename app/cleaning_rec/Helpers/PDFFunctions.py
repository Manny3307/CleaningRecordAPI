from Helpers.ExceptionLogging import UberExceptionLogging
from Helpers.AWSHelperFunctions import AWSHelperFunctions
import json
import os, ntpath, sys, traceback
from shutil import copyfile
import glob
import pandas as pd
from datetime import datetime as dt, timedelta, time
import pdfkit

UberLogString = []

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

#Load Exception Messages
ExceptionMessages = objUberExceptionLogging.load_exception_success("Exception")

#Load the Success Messages
SuccessMessages = objUberExceptionLogging.load_exception_success("Success")

class PDFFunctions:
    
    def __init__(self) -> None:
        
        try:
        # Load the Config JSON file from the config folder and read the respective values
            ConfigJSON = open('../Config/config.json')
            ConfigData = json.load(ConfigJSON)

            # Get The Base Path from the Config File.
            global BasePath, HTMLHeaderTemplate, HTMLFooterTemplate, FinalHTMLResult, HTMLFolder, CSVFolder
            BasePath = ConfigData["configs"]["BasePath"]
            HTMLHeaderTemplate = ConfigData["configs"]["HTMLHeaderTemplate"]
            HTMLFooterTemplate = ConfigData["configs"]["HTMLFooterTemplate"]
            FinalHTMLResult = ConfigData["configs"]["FinalHTMLResult"]
            HTMLFolder = ConfigData["configs"]["HTMLFolder"]
            CSVFolder = ConfigData["configs"]["CSVFolder"]
        except:
            objUberExceptionLogging.UberLogException(ExceptionMessages["Exceptions"]["general_config"], True, True)
    
    #Get the Current path name to Name the PDF
    def GetCurrentPathName(self, folderName):
        try:
            UberPDFCleaningRecord = os.path.join(BasePath, folderName)
            #CurrentUberCleaningRecordFolder = f"D:\\Uber Cleaning Record\\{folderName}"
            CompleteFileName = f"{UberPDFCleaningRecord}/Cleaning-record-{folderName}.pdf"
            return CompleteFileName
        except:
            objUberExceptionLogging.UberLogException("ERROR: Cleaning record PDF file name cannot be correctly formed.", True, True)


    #Create the resultant PDF and save it in Folder Name entered by the User.
    def create_PDF(self, folderName):
        UberLogString.append("Begin to write the PDF file from the resultant HTML!!!")
        try:
            #Create PDF from UberCleanTimeHTML.html to upload into Uber Portal.
            TemplatePath = os.path.join(BasePath, folderName, HTMLFolder)
            pdfkit.from_file( f"{TemplatePath}/{FinalHTMLResult}", self.GetCurrentPathName(folderName))
            PDF_FileName = self.GetCurrentPathName(folderName)
            
            UberLogString.append(f"'{PDF_FileName}' written successfully from the resultant HTML file!!!")
            UberLogString.append(f"Uploading '{PDF_FileName}' to AWS Cloud!!!")
            
            self.UploadPDFToAWSCloudS3(PDF_FileName)    
            UberLogString.append(f"'{PDF_FileName}' uploaded to AWS Cloud successfully!!!")
        except:
            objUberExceptionLogging.UberLogException("ERROR: PDF file cannot be created, please check if the PDF file is already open!!!", True, True)

        return UberLogString
    
    #Upload the cleaning records PDF to AWS Cloud.
    def UploadPDFToAWSCloudS3(self, Destination_Path):
        try:
            AWSHelper = AWSHelperFunctions()
            AWSHelper.upload_file_to_s3(Destination_Path)
        except:
            objUberExceptionLogging.UberLogException("ERROR: Please check the internet connection, cleaning records can't be uploaded!!!", True, True)