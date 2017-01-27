import configparser
import os

ApplicationDir = os.path.dirname(os.path.abspath(__file__))
HomeDir = os.path.expanduser('~')
CredentialDir = os.path.join(HomeDir, '.credentials')

if not os.path.exists(CredentialDir):
    os.makedirs(CredentialDir)

CredentialFilePath = os.path.join(CredentialDir, 'CalSyncHAB.json')
CalSyncHABSettings = os.path.join(ApplicationDir, 'CalSyncHAB.ini')

Settings = configparser.ConfigParser()
Settings.read(CalSyncHABSettings)

ApplicationName = Settings.get('General', 'ApplicationName')

CalendarScope = Settings.get('Calendar', 'CalendarScope')
ClientSecretFile = Settings.get('Calendar', 'ClientSecretFile')

HostName = Settings.get('OpenHAB', 'HostName')
Port = Settings.get('OpenHAB', 'Port')
SSLConnection = Settings.getboolean('OpenHAB', 'SSLConnection')
Username = Settings.get('OpenHAB', 'Username')
Password = Settings.get('OpenHAB', 'Password')
CalendarItemPrefix = Settings.get('OpenHAB', 'CalendarItemPrefix')

