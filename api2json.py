from GroupMeAnalysis import GroupMeAnalysis
import json

if __name__ == '__main__':
    app = GroupMeAnalysis.GroupMeAnalysis()
    msgs = app.getAllMessages(input('Group chat name to import: '))

    with open(input('Output file name: ') + '.json', 'w') as f:
        json.dump(msgs, f, indent=4)
