# Goal #
Most video streaming websites try to obfuscate the source URL's of their content to prevent you downloading it. [Pytube](http://code.google.com/p/pytube) aims to combat this obfuscation and provide you with the actual source URL of the video.

# Example #

```
#!python

>>> # list sites that pytube currently works with
>>> python pytube.py -s
youtube.com
metacafe.com

>>> # find source URL of flash video and download it to given file
>>> python pytube.py http://www.youtube.com/watch?v=YZTG2IBMXeU -o video.flv
http://v21.lscache8.c.youtube.com/videoplayback?ip=0.0.0.0&sparams=id%2Cexpire...[truncated]

>>> # find source URL of flash video but don't download it
>>> python pytube.py http://www.metacafe.com/watch/3446250/pimp_my_truck_truck_vs_plane/
http://akvideos.metacafe.com/ItemFiles/%5BFrom%20www.metacafe.com%5D%203446250.11748563.11.flv

```


# TODO #
So far pytube only works with [YouTube](http://www.youtube.com) and [MetaCafe](http://metacafe.com/). 
To add another video site you just need a regular expression to match the flash URL in the HTML of a video webpage. For example metacafe URLs are stored in the mediaURL attribute, so the regular expression is simply *` &mediaURL=(.*?)& `*

Online video sites often update their layout, possibly to mess up programs like pytube, so let me know if a video site no longer works. And definitely send me regular expressions for other video sites you get pytube working with.