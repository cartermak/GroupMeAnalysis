from dotenv import load_dotenv
import requests
import json
import os


class GroupMeAnalysis():
    baseURL = 'https://api.groupme.com/v3'

    def __init__(self):
        load_dotenv()
        self.token = os.getenv('GROUPME_TOKEN')

        self.getAllMessages('ASEN Class of 2022')

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

            retMsgs = requests.get(self.baseURL + '/groups/' + groupId + '/messages',
                                   params={'limit': '100', 'before_id': msgs[-1]['id'], 'token': self.token}).json()['response']['messages']

            retMsgs.sort(key=lambda k: k['created_at'])

            # print([msg['created_at'] for msg in retMsgs])

            print('Received ' + str(len(retMsgs)) + ' messages')

            msgs = msgs + retMsgs

            if len(msgs) > 1000:
                break

        # Write data to file
        with open(input('Output file name: ') + '.json', 'w') as f:
            json.dump(msgs, f, indent=4)


if __name__ == '__main__':
    app = GroupMeAnalysis()
