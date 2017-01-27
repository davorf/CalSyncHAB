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
        AuthenticationFlow = client.flow_from_clientsecrets(S.ClientSecretFile, S.CalendarScope)
        AuthenticationFlow.user_agent = S.ApplicationName
        Credentials = tools.run_flow(AuthenticationFlow, CredentialStore, Flags)

    return Credentials

def Main():
    Credentials = GetCredentials()
    HTTPAuthorization = Credentials.authorize(httplib2.Http())
    CalendarService = discovery.build('calendar', 'v3', http = HTTPAuthorization)
    CurrentTime = datetime.datetime.utcnow().isoformat() + 'Z'

    CalendarEvents = CalendarService.events().list(
        calendarId = 'primary',
        timeMin = CurrentTime,
        maxResults = 10,
        singleEvents = True,
        orderBy = 'startTime').execute()

    RetrievedEvents = CalendarEvents.get('items', [])

    if not RetrievedEvents:
        print('No upcoming events found.')

    for SingleEvent in RetrievedEvents:
        EventStartTime = SingleEvent['start'].get('dateTime', SingleEvent['start'].get('date'))
        print(EventStartTime, SingleEvent['summary'])

if __name__ == '__main__':
    Main()
        

