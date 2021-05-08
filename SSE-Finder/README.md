# SSE-FINDER

SSE-FINDER is a web applicaiton for finding possible SSEs from a dataset, identify potential sources of infection for each event, and automatically retrieve location data from an external API. 

# Usage

### SSE-Finder website 

Check it out in the following website
https://sse-finder-comp3297-o.herokuapp.com/

# Assumption 

1. Location Search will always provide the first data from the retrieve information unless it fails with a non-200 status code
2. when an infection is confirmed, that person is immediately isolated and will not attend any subsequent events until no longer infectious

# Admin Account

username: adminse
password: comp3297


# Features

1. Insert case records. (With error detection)
2. Insert event records. (With error detection)
3. View case with associated event records.
4. Search for SSE within specified timeframe
5. View SSE event details with associated cases classified as potential infector/infected.
6. Login and logout


### Features not supported

None