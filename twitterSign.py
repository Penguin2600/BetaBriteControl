#!/usr/bin/env python

import AlphaSign
import urllib
import simplejson
import time

def searchTweets(query):
        search = urllib.urlopen("http://search.twitter.com/search.json?q="+query)
        dict = simplejson.loads(search.read())
        return dict["results"]

def main ():
        
        s = AlphaSign.Sign( 'com3' )
        
        while 1:
                resultsDict=searchTweets("#BockLedSign")
                for result in resultsDict: 
                        print "Found:",result["text"],"\n"

                signText="<nohold><slow><g><block><dr> "
                for i in range(0,2):
                        tempText=resultsDict[i]["text"]

                        tempText=tempText.split("#")[0].strip()
                        tempText=tempText.replace("&lt;", "<")
                        tempText=tempText.replace("&gt;", ">")
                        signText+=tempText + " <g><block><dr> "

                print "Most Recent:",signText,"\n"
                
                s.sendTextPriority(AlphaSign.encodeText(signText),'a')
                time.sleep(30)
        return 0

if __name__ == '__main__': main()
