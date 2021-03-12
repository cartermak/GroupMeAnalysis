import matplotlib.pyplot as plt
import json

if __name__ == '__main__':

    # Load data file
    with open(input('Name of file to import (without .json): ') + '.json','r') as f:
        msgs = json.load(f)
    
    # Get most liked message
    likes = [len(msg['favorited_by']) for msg in msgs]
    idx_max_likes = likes.index(max(likes))
    msg_max_likes = msgs[idx_max_likes]

    # Remove list of likes because the whole point is that it's long but we don't want to see it
    msg_max_likes.pop('favorited_by')

    # Print results
    print('Most liked message: ')
    print(json.dumps(msg_max_likes,indent=4))

    # Plot histogram of likes
    plt.hist(likes,bins=100,log=True)
    plt.show()