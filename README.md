# GroupMe Analysis

This is a quick-and-dirty tool to scrape the list of all messages from a GroupMe group and process them. 

The API interfacing is through the `GroupMeAnalysis` module and the main scripts are `api2json.py`, which allows the user to select a group by name and save all messages to a JSON file, and `analysis.py`, which reads in a JSON file and performs some basic tasks.

The user needs to provide a `.env` file in the project directory with the key `GROUPME_TOKEN`, as shown in `demo.env`. This token can be obtained by defining an application on GroupMe's developer platform.
