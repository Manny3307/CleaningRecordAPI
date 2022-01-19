from bs4 import BeautifulSoup
import pdftotree
import glob
from datetime import datetime, timedelta
import pandas as pd
import os

def formDate(row):
    trip_date_time = ""
    if len(row.findChildren()) <= 5:
        getspanchild = row.findChildren()
        tripdatetime = ""
        for gsc in getspanchild:
            tripdatetime += f"{gsc.text},"
            
        tripdatetime1 = tripdatetime.split(',') 
        temp = tripdatetime1[2]
        triptime = temp[:2] + ":" + temp[2:] 
        
        if tripdatetime1[3] == "AM" or tripdatetime1[3] == "PM":
            trip_date_time = f"{tripdatetime1[1]} {tripdatetime1[0]}, 2022 {triptime} {tripdatetime1[3]}"

    return trip_date_time

def clean_alt_list(list_):
    list_ = str(list_)
    list_ = list_.replace('\\x00', '')
    list_ = list_.replace('[', '')
    list_ = list_.replace(']', '')
    list_ = list_.replace("'", "")
    return list_

root_file_name = "../../Uber_Statements/10Jan-17Jan_2022/*.pdf" 
pdffiles = glob.glob(root_file_name)

root_Uber_Statements_html_path = f"{root_file_name.split('*')[0]}HTML"

if not os.path.exists(root_Uber_Statements_html_path):
    os.makedirs(root_Uber_Statements_html_path)
    print(f"HTML folder {root_Uber_Statements_html_path} created successfully!!!!")
else:
    print("HTML folder already exists!!!!")

htmlfiles = []
for pdf_file in pdffiles:
    pdf_file_name = pdf_file.split('/')
    html_file_name = f"{root_Uber_Statements_html_path}/{pdf_file_name[len(pdf_file_name) - 1]}".replace("pdf","html")
    htmlfiles.append(html_file_name)
    pdftotree.parse(pdf_file, html_path=f"{html_file_name}", model_type=None, model_path=None, visualize=False)
    if os.path.exists(html_file_name):
        print(f"{html_file_name} created successfully!!!!!")
    else:
        print(f"There was problem while creating {html_file_name}, Please try again!!!!!")

html_files = htmlfiles

DateFormat = '%d %b, %Y %I:%M %p'
data = []
for html_file in html_files:
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        spans = soup.findAll('span', {'class' : 'ocrx_line'})
        #print(spans)
        for row in spans:
            if len(row.findChildren()) >= 4:
                if formDate(row) != None and formDate(row) != "":
                    data.append([formDate(row)])


root_Uber_Statements_csv_path = f"{root_file_name.split('*')[0]}CSV"

if not os.path.exists(root_Uber_Statements_csv_path):
    os.makedirs(root_Uber_Statements_csv_path)
    print(f"CSV folder {root_Uber_Statements_csv_path} created successfully!!!!")
else:
    print("CSV folder already exists!!!!")

uber_csv_file = f"{root_Uber_Statements_csv_path}/UberTripRecords.csv"


df = pd.DataFrame({'DateTimeTrip': data})
df["DateTimeTrip"] = df["DateTimeTrip"].apply(lambda x: clean_alt_list(x))
print(df["DateTimeTrip"])
df.to_csv(uber_csv_file, index=False)

if os.path.exists(uber_csv_file):
    print(f"{uber_csv_file} created successsfully!!!!!")
else:
    print(f"{uber_csv_file} can't be created, please try again!!!!!")
