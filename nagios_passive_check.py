#!/usr/bin/env python

# this script will poll the TII status page for 4 items and pass the status of those items 
# into Nagios as "passive checks". FYI...Nagios has to be setup correctly in order to receive these updates.
# Script uses BeautifulSoup etree to walk the page for defined X-paths (Yes, you have to know the X-paths 
# ahead of time. Pull these using object inspection on the page being monitored.)

import requests, os, sys, time
from bs4 import BeautifulSoup
from lxml import etree

tiiHost = 'my.monitored_host.com'            # hostname or URL of target (Nagios service target)
tiiUrl = 'https://my.monitored_host.com'     # URL of page to scrape
nagiosHost = 'my.nagios_url.com'             # URL or FQDN of Nagios system
nagiosToken = 'myNagiosToken'                # API key
reSults = {}                                 # dictionary to hold results per check
nOw = time.strftime("%H:%M:%S")
toDay = time.strftime("%Y-%m-%d")
dateStamp = toDay+"_" + nOw

# these hosts need to be setup in Nagios under the tiiHost service specified above
tiiLoginsXpath = '/html/body/div[1]/div[2]/div[3]/div[1]/div[4]/div[2]/div[1]/span[3]'
paperSubsXpath = '/html/body/div[1]/div[2]/div[3]/div[1]/div[4]/div[2]/div[2]/span[2]'
rptProcTimeXpath = '/html/body/div[1]/div[2]/div[3]/div[1]/div[4]/div[2]/div[3]/span[2]'
apiXpath = '/html/body/div[1]/div[2]/div[3]/div[1]/div[4]/div[2]/div[4]/span[2]'

webPage = requests.get(tiiUrl)
soup = BeautifulSoup(webPage.content, "html.parser")
dom = etree.HTML(str(soup))

reSults.update({'tiiLoginsStatus':str(dom.xpath(tiiLoginsXpath)[0].text.split()[0])})
reSults.update({'paperSubsStatus':str(dom.xpath(paperSubsXpath)[0].text.split()[0])})
reSults.update({'rptProcTimeStatus':str(dom.xpath(rptProcTimeXpath)[0].text.split()[0])})
reSults.update({'apiStatus':str(dom.xpath(apiXpath)[0].text.split()[0])})

for key, value in reSults.items():
    if value == 'Operational':
        stAte = '0'                           # possible states:  0:normal; 1:intermittent; 2:degraded; 3:unknown
        coMment = 'SERVICE_NORMAL_' + dateStamp
    else:
        stAte = '3'
        coMment = 'ATTENTION_REQUIRED_' + dateStamp
    nagiosUrl = str('https://' + nagiosHost + '/nrdp/?cmd=submitcmd&token=' + nagiosToken + '&command=PROCESS_SERVICE_CHECK_RESULT%3B' + tiiHost + '%3B' + key + '%3B' + stAte + '%3B' + coMment + '%5Cn&btnSubmit=Submit+Command')
    print(key, value, nagiosUrl)
    r = requests.post(nagiosUrl)
