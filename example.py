import bsto

# create a bsto instance
burningSeries = bsto.load('http://bs.to/', 'andere-serien');

# load series data at index == 312
mySeries = burningSeries.loadSeries(312) 

# load series data at index == 312 and loads stream links but takes long for series with alot episodes
#mySeries = burningSeries.loadSeries(312, True)

# print episode name of first episode of first season
print mySeries.getSeason(0).getEpisode(0).name 
### Flower Tales

# unload season/episode/stream data
mySeries.unload() 

# prints True, because all season/episode/stream information is deleted
print mySeries.getSeason(0) is None 
### True

# only name, gerne and link remains
print '%s : %s : %s' % (mySeries.name, mySeries.genre, mySeries.link)
