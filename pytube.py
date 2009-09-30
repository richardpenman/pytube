import sys
import re
import urllib2
import urlparse
from optparse import OptionParser


# regular expression data for each website
VIDEO_DATA = [
    ('youtube.com', '%7C(.*?videoplayback.*?)%2C'),
    ('metacafe.com', '&mediaURL=(.*?)&'),
]
# default user agent used to download urls
USER_AGENT = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.13) Gecko/2009080315 Ubuntu/9.04 (jaunty) Firefox/3.0.13'



def scrape(url, html=None, output=None):
    """Scrape video location from given url. 

    Use html instead of downloading if passed.
    Download file to output if passed.
    Return url of video if found, else None
    """
    netloc = urlparse.urlsplit(url).netloc
    for domain, video_re in VIDEO_DATA:
        if domain in netloc:
            if html is None:
                print "Downloading webpage from `%s' ..." % domain
                html = download(url).read()
            search = re.search(video_re, html)
            if search:
                flash_url = urllib2.unquote(search.group(1))
                print "Found flash video `%s'" % flash_url
                if output:
                    print "Downloading flash to `%s' ..." % output
                    open(output, 'wb').write(download(flash_url).read())
                return flash_url
            else:
                print 'Failed to locate video'
                return None
    print 'URL did not match'


def download(url):
    """Download url and return data
    """
    print USER_AGENT
    headers = {'User-Agent' : USER_AGENT}
    req = urllib2.Request(url, None, headers)
    return urllib2.urlopen(req)


if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog, [-o file.flv -s -h] url')
    parser.add_option('-o', '--output', dest='output', help='Output file to download flash file to. If this is not specified file will not be downloaded.')
    parser.add_option('-s', '--sites', action='store_true', default=False, dest='sites', help='Display sites that pytube supports, then quit.')
    parser.add_option('-a', '--agent', dest='agent', help='Override default user-agent for downloading webpages.') 
    options, args = parser.parse_args()
    if options.sites:
        print '\n'.join(domain for (domain, reg) in VIDEO_DATA)
    else:
        if args:
            if options.agent:
                global USER_AGENT
                USER_AGENT = options.agent
            scrape(args[0], output=options.output)
        else:
            print 'Need to pass the url of the video you want to download'
            parser.print_help()

