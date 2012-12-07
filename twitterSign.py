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
                resultsDict=searchTweets("#Phx2600LedSign")
                #for result in resultsDict: 
                #        print "Found:",result["text"],"\n"
                
                signText=resultsDict[0]["text"]

                signText=signText.split("#")[0]
                signText=signText.replace("&lt;", "<")
                signText=signText.replace("&gt;", ">")

                print "Most Recent:",signText,"\n"
                
                s.sendTextPriority(AlphaSign.encodeText('<slow><r>'+signText),'a')
                time.sleep(30)
        return 0

if __name__ == '__main__': main()
