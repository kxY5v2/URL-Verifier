# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 17:07:40 2020

@author: kxY5v2
"""

# Requests Library
import urllib3
# Reading CSV
import pandas as pd
# Array handling
import numpy as np

try:
    # Open file, read as csv
    df = pd.read_csv('ADD YOUR FILE HERE')
    # Print to console if file opened
    print('File Opened \n')
except:
    # File did not open
    print('Error: File Not Opened')


# Array of Broken URL's
brokenLinks = np.array([])

# Loop through CSV, check every URL in df are return status.
for url in df:
    # Allows for arbitrary requests while transparently keeping track of necessary 
    # connection pools for you.
    http = urllib3.PoolManager()
    try:
        # urllib3 requests, get ( like requests.get(), no retires, no connection timer)
        r = http.request('GET', url, retries=False)
        # print url and status
        print(str(url) + ' - ' + str(r.status))
        # if status 404, file not found
        if str(r.status) == "404":
            # add to url and status to array of broken links
            brokenLinks = np.append(brokenLinks, str(url) + ' - 404')
            # continue looping through csv
            continue
    # could not connect
    except urllib3.exceptions.NewConnectionError:
        print('Connection Failed')
        brokenLinks = np.append(brokenLinks, str(url) + ' - Connection Failed')
    # SSL error
    except urllib3.exceptions.SSLError:
        print('SSL Error')
        brokenLinks = np.append(brokenLinks, str(url) + ' - SSL Error')
    # Might work but program doesn't handle redirects
    except  urllib3.exceptions.LocationValueError:
        print('Redirect Failed')
        brokenLinks = np.append(brokenLinks, str(url) + ' - Redirect Failed')
    # Protocol error - stoped attempting to connect
    except urllib3.exceptions.ProtocolError:
        print('Connection Aborted')
        brokenLinks = np.append(brokenLinks, str(url) + ' - Connection Aborted')
    # URL leads to some file (pdf, etc) that is not found
    except FileNotFoundError:
        print('File Not Found')
        brokenLinks = np.append(brokenLinks, str(url) + ' - File Not Found')

# Open and append to file
f = open("broken.txt", "a+")
# Print header to console
print('----------------------Broken Links---------------------')
# Loop through array of broken links
for i in brokenLinks:
    # print url and status, add space to console
    print(i, end=' ')
    # newline
    print()
# prints array to file, no status code
f.write(str(brokenLinks) + "\n")

f.close()

# Notes:
#       If URL ends in .8 or .2, or any other number, it is a duplicate.
#       The Dot number means there is a duplicate, it must be removed.
