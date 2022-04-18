import math

class Estimate(object):

    def __init__(self, c=1.0, cumulateAds=0, cumulateNews=0):
        self.c = c
        self.cumulateAds  = cumulateAds
        self.cumulateNews = cumulateNews
        self.adPos        = []
        self.newPos       = []

    def computeDCGForAds(self, listAds):

        if not listAds or len(listAds)<=0: return

        for adinfoRes in listAds:
            self.cumulateAds += adinfoRes.ecpm / (self.c * math.log2(adinfoRes.pos+1))
            self.adPos.append(adinfoRes.pos)

    def computeDCGForNews(self, listNews):

        if not listNews or len(listNews)<=0: return

        for contentInfoRes in listNews:
            self.cumulateNews += contentInfoRes.score / (self.c * math.log2(contentInfoRes.pos+1))
            self.newPos.append(contentInfoRes.pos)