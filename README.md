This project is for my guild on Throne and Liberty. The goal is to create a discord application that our server can use to retrieve past sales of items in our server to see what things are selling for. 
api.js is the file used to pull data from TLDB's api and devalue the data into readable data
dp.py is used to process that data from the json and match server id with server names, item id with item names and trait id with trait names then saves a copy of that file locally.
Servertsort.py is used to save csv files for each server in their specific folder timestamped. 
