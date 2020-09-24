# import the modules we will need to this project
from bs4 import BeautifulSoup
import requests


# Create a function that will be used later to check connection status

def check_response(resp_obj):
    # if the requests object returns 200 we have a connection
    try:
        if resp_obj.status_code == 200:
            print(f"Connection OK: {resp_obj.status_code}")
    except:
        # If we are not able to access the page what was the HTTP error code
        # 4xx: CLient Server, 5xx: Server Error will be the most common
        print(f"Error: Not 200 return value was: {resp_obj}")

# Convert the address to a raw string 
url_sbw = r"https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"

# Using requests and get access the address
page_sbw = requests.get(url_sbw)

# call our function from above and print the connection status
check_response(page_sbw)


# Using bs4 we can create the Soup
soup = BeautifulSoup(page_sbw.text, 'html.parser')
type(soup)


# soup.body will access all of the HTML within the body tags <body>...</body>
# The table is conatined there so no reason to return all of the information within the header, too
body_tag = soup.body
# confirm the element type
type(body_tag)


# Here we use find_all looking for the tag table and attribute class name 'wikitable'
tables = body_tag.find_all('table',{'class': 'wikitable'})
print(type(tables))
# Check the length of variable tables it should contain 4 tables
print(f"Returns the four tables we want {len(tables)}")

# from the four tables we want index 1
sb_table = tables[1]
sb_table

# Using find_all() to access the first header which is a bs4 element tag 
print(type(sb_table.find_all('th')[0]))
print('='*45)

# We can convert the tag to a string and remove the tags/angle brackets
print(sb_table.find_all('th')[0].string.rstrip("\n"))
print('='*45)
print("If we do not utilize .sting.rstrip(\'\\n')")
print(sb_table.find_all('th')[0])

# Pritning all of the headers
sb_table.find_all('th')

headerNames = []
for i in range(len(sb_table.find_all('th'))):
    try:
        # Check if .contents is . than 1
        if len(sb_table.find_all('th')[i].contents) > 1:
            convert = list(sb_table.find_all('th')[i].contents)
            name = convert[0].rstrip("\n") + convert[2].rstrip("\n`")
            headerNames.append(name)
        else:
            name = sb_table.find_all('th')[i].string.rstrip("\n")
            headerNames.append(name)
    except:
        pass

# Print our list of clean headers
print(headerNames)

# Create a Python dictionary called winnerObj and add the `keys'
winnerObj = {}

for name in headerNames:
    winnerObj[name] = []
    
print(winnerObj)


import numpy as np

j = 0

# 9 columns by 58 rows = 522 
while j < len(sb_table.find_all('td')):     

    i = 0
    # 9 columns
    while i < len(winnerObj.keys()):
        try:
            # Check if index is even or 5. If True its an 'a' tag
            if i % 2 == 0 or i == 5:                           
                winnerObj[headerNames[i]].append(sb_table.find_all('td')[j].find('a').string)
            else:
                # Its not an 'a' tag so we find 'span'
                winnerObj[headerNames[i]].append(sb_table.find_all('td')[j].find('span').string)
                if winnerObj[headerNames[i]][-1] == "To be determined":
                    print(f"It is and i is {i} and j is {j}")
            i += 1
            j += 1
        
        except:
            # Using Numpy nan function 
            winnerObj[headerNames[i]].append(np.nan)
            i += 1
            j += 1

# Print the dictionary created. Each header is a key and each value for the respected header is contained within a list
print(winnerObj)