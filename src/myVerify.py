import urllib2, os

def verifyFileSize(url):
    """
    When attempting to download netcdf files, first check if a file with the
    same name as the file to be downloaded exists in the target directory. If so
    call, verifyFileSize(url) on the file which will return True if the file
    is the same size as the file to be downloaded. False otherwise. Not exactly
    the best validation form for netcdf files but its the best we could do. :/
    """
    
    # Get file name from url
    filename = os.path.basename(url)
    
    # Get 'content-length' header from URL
    req_info = urllib2.urlopen(url)
    req_info.headers.keys()
    contentLength = req_info.headers['content-length']
    
    # Get size of file
    fileSize = os.path.getsize(filename)

    # Returns true if existing file and url file are same size
    return contentLength == fileSize
