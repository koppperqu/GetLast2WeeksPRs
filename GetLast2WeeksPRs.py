from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

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
twoweeksago = datetime.today().date() - timedelta(days=14)

for index,eachName in enumerate(names):
    html = urlopen(links[index])
    soup=BeautifulSoup(html.read(), "html.parser")
    allMeets = soup.find('div',id='meet-results').findAll('div')
    prMeets=[]
    for eachMeet in allMeets:
        if (eachMeet.find('tr',class_='highlight')!=None):
            print(eachName + ' pr\'d in the ' + eachMeet.find('a').text + ' on ' +eachMeet.find('span').text.strip())
        inputDate = eachMeet.find_parent().find('span').text.strip()
        format="%b %d, %Y"
        meetDay = datetime.strptime(inputDate,format).date()

testurl = 'https://www.tfrrs.org/athletes/8280699/Wis_Stevens_Point/Joseph_Adams.html'

html = urlopen(testurl)
soup=BeautifulSoup(html.read(), "html.parser")
prMeets[0].find_parent().find('span').text.strip()
allMeets = soup.find('div',id='meet-results').findAll('div')

inputDate = a[0].find('span').text.strip()
format="%b %d, %Y"
datetime.strptime(inputDate,format).date()