#
# Description: pytube is a Python script to download flash video from various video websites
# Author: Richard Penman (see http://code.google.com/p/pytube/)
#


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
# default user agent to use when downloading
USER_AGENT = 'pytube'



def scrape(url, html=None, user_agent=None, output=None):
    """Scrape video location from given url. 

    Use html instead of downloading if passed.
    Download file to output if passed.
    Return url of video if found, else None
    """
    netloc = urlparse.urlsplit(url).netloc
    for domain, video_re in VIDEO_DATA:
        if domain in netloc:
            html = html if html else download(url, user_agent).read()
            search = re.search(video_re, html)
            if search:
                flash_url = urllib2.unquote(search.group(1))
                if output:
                    print "Downloading flash to `%s' ..." % output
                    open(output, 'wb').write(download(flash_url, user_agent).read())
                return flash_url
            else:
                raise PyTubeException('Failed to locate video regular expression in downloaded HTML')
    raise PyTubeException('URL did not match available domains')


def download(url, user_agent=None):
    """Download url and return data
    """
    headers = {'User-Agent' : user_agent}
    req = urllib2.Request(url, None, headers)
    return urllib2.urlopen(req)


class PyTubeException(Exception):
    pass



if __name__ == '__main__':
    # parse command line options
    parser = OptionParser(usage='usage: %prog, [-o <file.flv> -a <user_agent> -s -h] url')
    parser.add_option('-o', '--output', dest='output', help='Output file to download flash file to. If this is not specified file will not be downloaded.')
    parser.add_option('-s', '--sites', action='store_true', default=False, dest='sites', help='Display sites that pytube supports, then quit.')
    parser.add_option('-a', '--agent', dest='user_agent', default=USER_AGENT, help='Set user-agent for downloads.') 
    options, args = parser.parse_args()
    if options.sites:
        print '\n'.join(domain for (domain, reg) in VIDEO_DATA)
    else:
        if args:
            flash_url = scrape(args[0], user_agent=options.user_agent, output=options.output)
            if flash_url:
                print flash_url
        else:
            print 'Need to pass the url of the video you want to download'
            parser.print_help()
