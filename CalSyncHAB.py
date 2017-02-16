import httplib2
import os
import datetime
import argparse as AP
import Settings as S
import warnings
import requests
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
    CurrentTime = datetime.datetime.utcnow().isoformat() + 'Z'

    CalendarEvents = CalendarService.events().list(
        calendarId = S.CalendarId,
        timeMin = CurrentTime,
        maxResults = S.CalendarMaxEvents,
        singleEvents = True,
        orderBy = 'startTime').execute()

    RetrievedEvents = CalendarEvents.get('items', [])

    if not RetrievedEvents:
        print('No upcoming events found.')

    EventCounter = 0

    for SingleEvent in RetrievedEvents:
        EventSummary = ''
        EventLocation = ''
        EventDescription = ''
        EventStartTime = None
        EventEndTime = None

        EventCounter += 1

        if 'summary' in SingleEvent:
            EventSummary = SingleEvent['summary']

        if 'location' in SingleEvent:
            EventLocation = SingleEvent['location']

        if 'description' in SingleEvent:
            EventDescription = SingleEvent['description']

        if 'start' in SingleEvent:
            EventStartTime = SingleEvent['start'].get('dateTime', SingleEvent['start'].get('date'))

        try:
            datetime.datetime.strptime(EventStartTime, '%Y-%m-%dT%H:%M:%S' + S.CalendarTimeZone)
        except ValueError:
            EventStartTime = EventStartTime + 'T00:00:00' + S.CalendarTimeZone

        if 'end' in SingleEvent:
            EventEndTime = SingleEvent['end'].get('dateTime', SingleEvent['end'].get('date'))

        try:
            datetime.datetime.strptime(EventEndTime, '%Y-%m-%dT%H:%M:%S' + S.CalendarTimeZone)
        except ValueError:
            EventEndTime = EventEndTime + 'T00:00:00' + S.CalendarTimeZone            

        if S.OpenHABPort.strip() != '':
            TrimmedHostAndPort = S.OpenHABHostName.strip() + ':' + S.OpenHABPort.strip()
        else:
            TrimmedHostAndPort = S.OpenHABHostName.strip()        

        CalendarEventSummaryItemURL = 'http://' + TrimmedHostAndPort + '/rest/items/' + S.OpenHABItemPrefix + 'Event' + str(EventCounter) + '_Summary'
        OpenHABResponse = requests.post(CalendarEventSummaryItemURL, data = '', allow_redirects = True)
        OpenHABResponse = requests.post(CalendarEventSummaryItemURL, data = EventSummary.encode('utf-8'), allow_redirects = True)

        CalendarEventLocationItemURL = 'http://' + TrimmedHostAndPort + '/rest/items/' + S.OpenHABItemPrefix + 'Event' + str(EventCounter) + '_Location'
        OpenHABResponse = requests.post(CalendarEventLocationItemURL, data = '', allow_redirects = True)
        OpenHABResponse = requests.post(CalendarEventLocationItemURL, data = EventLocation.encode('utf-8'), allow_redirects = True)

        CalendarEventDescriptionItemURL = 'http://' + TrimmedHostAndPort + '/rest/items/' + S.OpenHABItemPrefix + 'Event' + str(EventCounter) + '_Description'
        OpenHABResponse = requests.post(CalendarEventDescriptionItemURL, data = '', allow_redirects = True)
        OpenHABResponse = requests.post(CalendarEventDescriptionItemURL, data = EventDescription.encode('utf-8'), allow_redirects = True)

        CalendarEventStartTimeItemURL = 'http://' + TrimmedHostAndPort + '/rest/items/' + S.OpenHABItemPrefix + 'Event' + str(EventCounter) + '_StartTime'
        OpenHABResponse = requests.post(CalendarEventStartTimeItemURL, data = 'UNDEF', allow_redirects = True)
        OpenHABResponse = requests.post(CalendarEventStartTimeItemURL, data = EventStartTime, allow_redirects = True)
    
        CalendarEventEndTimeItemURL = 'http://' + TrimmedHostAndPort + '/rest/items/' + S.OpenHABItemPrefix + 'Event' + str(EventCounter) + '_EndTime'
        OpenHABResponse = requests.post(CalendarEventEndTimeItemURL, data = 'UNDEF', allow_redirects = True)
        OpenHABResponse = requests.post(CalendarEventEndTimeItemURL, data = EventEndTime, allow_redirects = True)

if __name__ == '__main__':
    Main()
