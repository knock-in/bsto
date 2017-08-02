from bshttpwork import httpWorker

def load(url, path):
    return bsto(url, path).load()
    
class bsto:
    def __init__(self, url, path):
        self.url = url;
        self.worker = httpWorker(url);
        self.indexHtml = self.worker.getSoup(path)
        self.series = []
    
    def load(self):
        for tag in self.indexHtml.find_all('div', class_='genre'):
            genre = tag.find('span').find('strong').text
            for seriesHtml in tag.find_all('li'):
                name = seriesHtml.find('a').text
                link = seriesHtml.find('a').get('href')
                self.series.append(Series(genre, link, name))
        return self
    
    def loadSeries(self, seriesNum, streamLinks = False):
        retSeries = self.getSeries(seriesNum)
        
        if retSeries.loadedData != True:
            return retSeries.loadData(self.worker, streamLinks)
        else:
            return retSeries
    
    def getSeries(self, seriesNum):
        if seriesNum < self.getSeriesCount():
            return self.series[seriesNum]
    
    def getSeriesCount(self):
        return len(self.series)
        
    def isLoadedData(self, seriesNum):
        return self.getSeries(seriesNum).loadedData
    
    def isLoadedStreams(self, seriesNum):
        return self.getSeries(seriesNum).loadedStreams
    
    def isLoadedAll(self, seriesNum):
        return self.isLoadedData(seriesNum) and self.isLoadedStreams(seriesNum)
        


class Series:
    def __init__(self, genre, link, name, load = False):
        self.genre = genre;
        self.link = link;
        self.name = name;
        self.cover = ''
        self.description = ''
        self.infos = {}
        
        self.seasons = [];
        self.loadedData = False;
        self.loadedStreams = False;
        
        # Non standard variables
        self.seasonCount = 0;
        if load == True:
            self.loadData();
        
    def unload(self):
        self.seasons = []
        loadedData = False
        loadedStreams = False
        
    def getSeason(self, seasonNum):
        if seasonNum < self.getSeasonCount():
            return self.seasons[seasonNum]
        
    def getSeasonCount(self):
        return len(self.seasons)
    
    def loadData(self, httpWorker, streamLoad = False):
        soup = httpWorker.getSoup(self.link)
        
        self.description = soup.find(class_='justify').getText()
        self.cover = soup.find(alt='Cover').get('src')
        
        for div in soup.find(class_='infos').find_all('div'):
            key = div.span.getText()
            value = div.p.get_text()
            self.infos[key] = value
        
        seasonCount = 0
        for tagHtml in soup.find_all('ul', class_='clearfix'):
            for seasonHtml in tagHtml.find_all('li'):
                seasonCount += 1
        
        self.seasonCount = seasonCount
        
        # Now do the same to the other seasons
        for x in range(0, self.seasonCount):
            self.seasons.append(Season(x, '', self.link + '/' + str(x)));
            
            if x == 0:
                seasonSoup = soup # First season is already loaded so use it
            else:
                seasonSoup = httpWorker.getSoup(self.getSeason(x).seasonLink)
                
                
            first = True
            for table in seasonSoup.find_all('table', class_='episodes'):
                if first == True: # Only first table has relevant informations
                    episodeNum = 0;
                    for tr in table.find_all('tr'):
                        episodeLink = '';
                        episodeName = '';
                        episodeStreams = []
                        count = 0
                        td = tr.find('td')
                        episodeNum += 1
                        for streamHtml in td.find_all('a'):
                            episodeName = streamHtml.get('title')
                            episodeLink = streamHtml.get('href')
                            if streamLoad == True:
                                episodeSoup = httpWorker.getSoup(episodeLink)
                                hostsLinks = episodeSoup.find('ul',class_='hoster-tabs').find_all('li')
                                hosts = []
                                for li in hostsLinks:
                                    hosts.append(li.find('a').get('href'))
                                for host in hosts:
                                    streamSoup = httpWorker.getSoup(host)
                                    streamLink = streamSoup.find(id="root").section.find(target="_blank").get('href')
                                    streamName = streamSoup.find('ul',class_='hoster-tabs').find(class_='active').find('a').getText().strip()
                                    tmpStream = Stream(streamName, host)
                                    tmpStream.streamVideoLink = streamLink
                                    episodeStreams.append(tmpStream)
                        if streamLoad == True:
                            self.loadedStreams = True
                        self.getSeason(x).addEpisode(Episode(episodeNum, episodeLink, episodeName, episodeStreams));
                    first = False # Afterwards turn it off
            
        # All episodes now saved with each streams
        self.loadedData = True
        return self

class Season:
    def __init__(self, seasonNum, seasonName, seasonLink):
        self.seasonNum = seasonNum
        self.seasonName = seasonName
        self.seasonLink = seasonLink
        self.episodes = [];
    
    def addEpisode(self, episode):
        self.episodes.append(episode);
    
    def getEpisode(self, episodeNum):
        if episodeNum < self.getEpisodeCount():
            return self.episodes[episodeNum];
    
    def getEpisodeCount(self):
        return len(self.episodes)
        
class Episode:
    def __init__(self, index, episodeLink, episodeName, episodeStreams):
        self.index = int(index);
        self.link = episodeLink;
        self.name = episodeName;
        self.streams = episodeStreams;
    
    def getStream(self, streamNum):
        if streamNum < getStreamCount():
            return self.streams[streamNum]
    
    def addStream(self, stream):
        self.streams.append(stream)
    
    def getStreamCount(self):
        return len(self.streams)
        
class Stream:
    def __init__(self, streamName, streamLink):
        self.name = streamName
        self.link = streamLink
        self.videoLink = ''