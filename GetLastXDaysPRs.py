from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from itertools import groupby

value=''
while not value.isdigit():
    value = input("enter number of days since meet you want prs from add 1 for safey :) ")
    if value.isdigit():
        numerical_value = int(value)
    else:
        print("Invalid input. Please enter a valid number.")


daysToRemove = numerical_value
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

sortedDictByDate = {k: list(g) for k, g in groupby(sorted(initalDictionary, key=lambda x: x[4], reverse=True), key=lambda x: x[4])}
for eachDate,meetsAtDate in sortedDictByDate.items():
    sortedByMeet = {k: list(g) for k, g in groupby(sorted(meetsAtDate, key=lambda x: x[1]), key=lambda x: x[1])}
    for eachMeet,prs in sortedByMeet.items():
        print('\n\n\n')
        print (eachMeet + ' date ' + prs[0][4].strftime(format))
        for eachPR in prs:
            print (eachPR[0] + " pr'd in the " + eachPR[2] + " with a " + eachPR[3])

input('enter to close')
