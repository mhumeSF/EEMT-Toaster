import urllib2, os

def verifyFileSize(url):
    """
    When attempting to download netcdf files, first check if a file with the
    same name as the file to be downloaded exists in the target directory. If so
    call, verifyFileSize(url) on the file which will return True if the file
    is the same size as the file to be downloaded. False otherwise. Not exactly
    the best validation form for netcdf files but its the best we could do. :/
    """
    """
    # Get 'content-length' header from URL
    req_info = urllib2.urlopen(url)
    contentLength = req_info.headers['content-length']

    # Get file name from url
    filename = os.path.basename(url)
    # Get size of local file
    fileSize = os.path.getsize(filename)

    # Returns true if existing file and url file are same size
    return int(contentLength) == int(fileSize)
    """
    return int(os.path.getsize(os.path.basename(url))) == int(urllib2.urlopen(url).headers['content-length'])

if __name__ == '__main__':
    verifyFileSize(url)
