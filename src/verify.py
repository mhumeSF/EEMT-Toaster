#!/usr/bin/python

import urllib2, os, sys

# Get URL and Filename
url = sys.argv[1]
filename = url.split('/')[-1]

# Get 'content-length' header from URL
req_info = urllib2.urlopen(url)
req_info.headers.keys()
contentLength = req_info.headers['content-length']

# Get filesize of file
fileSize = os.path.getsize(filename)

print "Length: " + str(contentLength)
print "Size: " + str(fileSize)

# Compare filesize to content-lenght 'header'
if(int(contentLength) == int(fileSize)):
    print "Hoo-ray!"
else:
    print "BoOoOoOo..."