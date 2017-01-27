#!python3

import httplib2
import os
import datetime
import argparse as AP
import Settings as S
import warnings
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

Flags = AP.ArgumentParser(parents=[tools.argparser]).parse_args()

def GetCredentials():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        CredentialStore = Storage(S.CredentialFilePath)
        Credentials = CredentialStore.get()
    
    if not Credentials or Credentials.invalid:
        AuthenticationFlow = client.flow_from_clientsecrets(S.CalendarClientSecretFile, S.CalendarScope)
        AuthenticationFlow.user_agent = S.ApplicationName
        Credentials = tools.run_flow(AuthenticationFlow, CredentialStore, Flags)

    return Credentials

def Main():
    Credentials = GetCredentials()
    HTTPAuthorization = Credentials.authorize(httplib2.Http())
    CalendarService = discovery.build('calendar', 'v3', http = HTTPAuthorization)
    CurrentTime = datetime.datetime.utcnow().isoformat() + S.CalendarTimeZone

    CalendarEvents = CalendarService.events().list(
        calendarId = S.CalendarId,
        timeMin = CurrentTime,
        maxResults = S.CalendarMaxEvents,
        singleEvents = True,
        orderBy = 'startTime').execute()

    RetrievedEvents = CalendarEvents.get('items', [])

    if not RetrievedEvents:
        print('No upcoming events found.')

    for SingleEvent in RetrievedEvents:
        EventLocation = ''
        EventDescription = ''
        
        EventSummary = SingleEvent['summary']

        if 'location' in SingleEvent:
            EventLocation = SingleEvent['location']

        if 'description' in SingleEvent:
            EventDescription = SingleEvent['description']
            
        EventStartTime = SingleEvent['start'].get('dateTime', SingleEvent['start'].get('date'))
        EventEndTime = SingleEvent['end'].get('dateTime', SingleEvent['start'].get('date'))

        print('Summary: ' + EventSummary)
        print('Location: ' + EventLocation)
        print('Description: ' + EventDescription)
        print('Start time: ' + EventStartTime)
        print('End time: ' + EventEndTime)

if __name__ == '__main__':
    Main()
        

