from BeautifulSoup import bs4
import urllib2

class httpWorker:
    def __init__(self, site):
        self.site = site
    
    def getHtml(self, path):
        return urllib2.urlopen(self.site + path)
        
    def getSoup(self, path):
        return BeautifulSoup(self.getHtml(path))