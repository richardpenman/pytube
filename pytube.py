import sys
import re
import urllib2
import urlparse


# regular expression data for each website
video_data = [
    ('youtube.com', '%7C(.*?videoplayback.*?)%2C'),
    ('metacafe.com', '&mediaURL=(.*?)&'),
]

def scrape(url, html=None):
    """Scrape video location from URL. 
    Use html instead of downloading if passed"""

    netloc = urlparse.urlsplit(url).netloc
    for domain, video_re in video_data:
        if domain in netloc:
            if not html:
                print 'Downloading from %s ...' % domain
                html = urllib2.urlopen(url).read()
            search = re.search(video_re, html)
            if search:
                print 'Success!'
                return urllib2.unquote(search.group(1))
            else:
                'Failed to locate video'
                return None
    print 'URL did not match'



if __name__ == '__main__':
    print scrape(sys.argv[1])
