
#pip3 install lxml
#pip3 install BeautifulSoup4
#pip3 install pandas

import os
import csv
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import re



#we care about seeing which is the oldest i765 form ID we can find (oldest form that is showing form ID)

#check if URL has i765
#return date,status
#valid == i765
def isValid(id):
    #sanchit id at start time: YSC1890067298
    url = "http://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum=" + id

    #pull url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    body = soup.find_all("div", class_="rows text-center");

    #pull detailed text
    status = body[0].find_all('h1')
    status = str(status[0])

    paragraph = body[0].find_all('p')
    paragraph = str(paragraph[0])


    #regex detailed text for "Form I-765"
    if(paragraph.find("I-765",0,len(paragraph)) == -1):
        return (0, 0)
    else:
        comma=2
        counter=5
        while(comma>0):
            char = paragraph[counter]
            if(char==','):
                comma-=1
            counter+=1
        thecount = int(counter)
        date = paragraph[5:thecount]
        return (status[4:-5],date)


def genIDs():
    start = "YSC18900"
    index = 37000
    ids = []
    status = []
    date = []
    while(index>9000):
        if(index%1000==0):
            print ("We at dis index fam: " + str(index))
        current_id = start+str(index)
        result = isValid(current_id)
        if(result != (0,0) ):
            ids.append(current_id)
            status.append(result[0])
            date.append(result[1])
        index -= 1

    ids = np.array(ids)
    status = np.array(status)
    date = np.array(date)
    dataset = pd.DataFrame({'ids': ids, 'status': status, 'date':date}, columns=['IDS', 'STATUS', 'DATE'])
    dataset.to_csv("deportations.csv")


def main():
    print ("Generating IDs Fam")
    genIDs()

if __name__ == "__main__":
    main()