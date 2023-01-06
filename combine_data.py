'''
Scraper unfortunately stopped after 30 pages, so I had to run it again 
so it could scrape the remaining 20 pages. I saved the data in two separate files,
naukri_data.json and naukri_data1.json. I then wrote a script to combine the two files into one.
'''

import json

with open("naukri_data.json", "r") as f:
    data = json.load(f)

with open("naukri_data1.json", "r") as f:
    data2 = json.load(f)

data.extend(data2)

with open("naukri_data_all.json", "w") as f:
    json.dump(data, f, indent=4)

