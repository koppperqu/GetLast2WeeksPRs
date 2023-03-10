from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from itertools import groupby
import json


daysToRemove = 14
mensTrackURL = 'https://www.tfrrs.org/teams/tf/WI_college_m_Wis_Stevens_Point.html'
html = urlopen(mensTrackURL)
soup=BeautifulSoup(html.read(), "html.parser")
womensTrackURL = 'https://www.tfrrs.org'+soup.find('a',text='Women\'s Track & Field')['href']

#This functon takes the input ur and finds the roster section on the page then grabs all the names and tffrs links and returns them as a dictionary as key value pairs name is the key
def getAthletesNamesAndTffrsLinks(url):
    html = urlopen(url)
    soup=BeautifulSoup(html.read(), "html.parser")
    athleteLinks = soup.find('h3',text='ROSTER').find_parent().find('tbody').findAll('a')
    names=[]
    tffrsLink=[]
    for eachLink in athleteLinks:
        nameParts=eachLink.getText().split(', ')
        names.append(nameParts[1]+' '+nameParts[0])
        tffrsLink.append('https://www.tfrrs.org'+eachLink['href'])
    return(names,tffrsLink)

men,menTffrsLink = getAthletesNamesAndTffrsLinks(mensTrackURL)
women,womenTffrsLink = getAthletesNamesAndTffrsLinks(womensTrackURL)
names = men+women
links = menTffrsLink + womenTffrsLink
twoweeksago = datetime.today().date() - timedelta(daysToRemove)
initalDictionary = []
for index,eachName in enumerate(names):
    html = urlopen(links[index])
    soup=BeautifulSoup(html.read(), "html.parser")
    allMeets = soup.find('div',id='meet-results').findAll('div')
    prMeets=[]
    for eachMeet in allMeets:
        if (eachMeet.find('tr',class_='highlight')!=None):
            prMeets.append(eachMeet)
    for eachPRMeet in prMeets:
        inputDate = eachPRMeet.find('span').text.strip()
        #Special case for dates like April 13-14, 2021
        if '-' in inputDate:
            split = inputDate.split('-')
            split2 = split[1].split(',')
            inputDate = split[0] +','+split2[1]
        format="%b %d, %Y"
        meetDate = datetime.strptime(inputDate,format).date()
        if(meetDate>twoweeksago):
            #!!!RECENTPR!!!
            #Need to grab the athlete name, meet name, event, pr, meet date
            meetName = eachPRMeet.find('thead').find('a').text.strip()
            allPRsAtPRMeet = eachPRMeet.findAll('tr', class_='highlight')
            for eachPRatPRMeet in allPRsAtPRMeet:
                eventName = eachPRatPRMeet.find('td').text.strip()
                pr = eachPRatPRMeet.find('a').text.strip()
                initalDictionary.append((eachName,meetName,eventName,pr,meetDate))
                print(eachName)

prepForJSON=[]
sortedDictByDate = {k: list(g) for k, g in groupby(sorted(initalDictionary, key=lambda x: x[4], reverse=True), key=lambda x: x[4])}
for eachDate,meetsAtDate in sortedDictByDate.items():
    sortedByMeet = {k: list(g) for k, g in groupby(sorted(meetsAtDate, key=lambda x: x[1]), key=lambda x: x[1])}
    for eachMeet,prs in sortedByMeet.items():
        listOfPRS = []
        uniqueNames=[]
        uniqueNameCount=0
        for eachPR in prs:
            if (eachPR[0] not in uniqueNames):
                uniqueNames.append(eachPR[0])
                uniqueNameCount+=1;
            listOfPRS.append({"athletename":eachPR[0],"eventname":eachPR[2],"pr":eachPR[3]})
        jsonMeetOBJ = {"meetname":eachMeet,
                       "meetdate":prs[0][4].strftime(format),
                       "numberofprs":len(prs),
                       "uniqueprs":uniqueNameCount,
                       "prsatmeet":listOfPRS}
        prepForJSON.append(jsonMeetOBJ)

f = open('recentPRs.json', "w")
f.write(json.dumps(prepForJSON, indent=4))
f.close()
print('DONE')
input()