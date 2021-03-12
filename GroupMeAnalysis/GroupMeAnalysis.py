from dotenv import load_dotenv
import requests
import json
import os


class GroupMeAnalysis():
    baseURL = 'https://api.groupme.com/v3'

    def __init__(self):
        load_dotenv()
        self.token = os.getenv('GROUPME_TOKEN')
        #msgs = self.getAllMessages('Just Me \'n\' the Boiz')

    def groupIdByName(self, groupName):

        # Get list of all groups which the user is a member of
        groups = requests.get(self.baseURL + '/groups',
                              params={'omit': 'memberships', 'token': self.token})

        # Get list of IDs that match that group string
        id = [group['id'] for group in groups.json()['response']
              if group['name'] == groupName]

        # Throw error if group doesn't exist
        if len(id) == 0:
            raise Exception('No group found')
            return 0
        else:
            print('Found group: \"' + groupName + '\" with ID: ' + id[0])
            return id[0]

    def getLastMessage(self, groupId):

        # Request most recent messages, limiting to 1
        message = requests.get(self.baseURL + '/groups/' + groupId + '/messages',
                               params={'limit': '1', 'token': self.token})

        # print(message.json())

        # Extract ID of last message
        msg = message.json()['response']['messages'][0]
        return msg

    def getAllMessages(self, groupName):

        # Get group ID
        groupId = self.groupIdByName(groupName)

        # Get most recent message
        lastMsg = self.getLastMessage(groupId)
        retMsgs = [lastMsg]

        # Start list of messages
        msgs = [lastMsg]

        # Loop while list of returned messages is nonzero
        while len(retMsgs) > 0:
            print('Getting messages...')

            # Get list of messages before the most recent message
            try:
                retMsgs = requests.get(self.baseURL + '/groups/' + groupId + '/messages',
                                       params={'limit': '100', 'before_id': msgs[-1]['id'], 'token': self.token}).json()['response']['messages']
            except:
                break

            print('Last message ID: ' +
                  msgs[-1]['id'] + ' created at: ' + str(msgs[-1]['created_at']))

            # Sort messages in chronological order from newest to oldest
            retMsgs.sort(key=lambda k: k['created_at'], reverse=True)

            print('Received ' + str(len(retMsgs)) +
                  ' messages. Total messages received: ' + str(len(msgs)))

            msgs = msgs + retMsgs

            if len(msgs) > 30000:
                break

        return msgs
