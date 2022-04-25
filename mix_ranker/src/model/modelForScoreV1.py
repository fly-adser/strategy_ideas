from mix_ranker.src.mix_common.ClassInfo import *

"""
广告混排服务模拟，说明文档参考：
"""
class Mix_RankerV1(object):

    def __init__(self, maxInterval=0, maxAdsNum=3, alpha=1.0):
        self.maxInterval = maxInterval
        self.maxAdsNum   = maxAdsNum
        self.alpha       = alpha

    """
    支持广告保位诉求(如品牌广告置顶)
    """
    def insertAds(self, pos, listAds, fixedPosAd):
        if pos not in fixedPosAd: return False

        if listAds and pos-listAds[-1].pos<=self.maxInterval:
            AdPosMap = {}
            for key, value in fixedPosAd.items():
                if key>=pos:
                    AdPosMap[key+1] = value
                    continue
                AdPosMap[key] = value

            fixedPosAd.clear()
            fixedPosAd = AdPosMap.copy()
            return False

        adInfoReq = fixedPosAd[pos]
        adInfoRes = AdinfoRes()
        adInfoRes.adId = adInfoReq.adId
        adInfoRes.ecpm = adInfoReq.ecpm
        adInfoRes.pos  = pos
        listAds.append(adInfoRes)

        return True

    """
    获取保位广告
    """
    def getFixedPos(self, adInfoReqs):
        fixedPosAd, index = {}, 0
        while index<len(adInfoReqs):
            adInfoReq = adInfoReqs[index]
            if adInfoReq.fixedPos and adInfoReq.fixedPos > 0:
                fixedPosAd[adInfoReq.fixedPos] = adInfoReq
                del adInfoReqs[index]
                index -= 1
            index += 1

        return fixedPosAd

    """
    重新赋予人工干预广告的ecpm（双指针法）
    """
    def adjustEcpm(self, adInfoReqs):
        left, right = 0, len(adInfoReqs)-1

        while right>=0:
            rightEcpm = adInfoReqs[right].ecpm
            left      = right - 1
            while left>=0 and adInfoReqs[left].ecpm<=rightEcpm: left-=1

            if left==right-1:
                right = left
            else:
                if left>=0:
                    gap = (adInfoReqs[left].ecpm-rightEcpm) // (right - left)
                else:
                    if right==len(adInfoReqs)-1:
                        gap = rightEcpm
                    else:
                        gap = rightEcpm - adInfoReqs[right+1].ecpm

                index = right - 1
                while index>left:
                    rightEcpm += gap
                    adInfoReqs[index].ecpm = rightEcpm
                    index -= 1

                right = left

    """
    根据广告请求信息构造广告返回信息
    """
    def createAds(self, adInfoReq, pos):
        adInfoRes = AdinfoRes()

        adInfoRes.adId = adInfoReq.adId
        adInfoRes.ecpm = adInfoReq.ecpm
        adInfoRes.pos  = pos

        return adInfoRes

    """
    根据资讯请求信息构造资讯返回信息
    """
    def createContent(self, contentInfoReq, pos):
        contentInfoRes = ContentInfoRes()

        contentInfoRes.contendId = contentInfoReq.contentId
        contentInfoRes.score     = contentInfoReq.score
        contentInfoRes.pos       = pos

        return contentInfoRes

    """
    广告和资讯混排过程（归并排序）
    """
    def mixProcess(self, mixRankerRequest, listAds, listNews):
        pos, indexAd, indexNews, pages = 1, 0, 0, mixRankerRequest.pages
        adInfoReqs, contentInfoReqs = mixRankerRequest.adInfoReqs, mixRankerRequest.contentInfoReqs

        adInfoReqs.sort(key=lambda x: x.ecpm, reverse=True)
        contentInfoReqs.sort(key=lambda x: x.score, reverse=True)

        fixedPosAd = self.getFixedPos(adInfoReqs)
        self.adjustEcpm(adInfoReqs)

        while indexAd<len(adInfoReqs) and indexNews<len(contentInfoReqs):
            if self.insertAds(pos, listAds, fixedPosAd):
                pos += 1
                continue

            if pages==1 and pos==1:
                contentInfoRes = self.createContent(contentInfoReqs[indexNews], pos)
                listNews.append(contentInfoRes)

                indexNews += 1
                pos += 1
                continue

            if len(listAds)>=self.maxAdsNum or (len(listAds)>0 and pos-listAds[-1].pos<=self.maxInterval):
                contentInfoRes = self.createContent(contentInfoReqs[indexNews], pos)
                listNews.append(contentInfoRes)

                indexNews    += 1
                pos          += 1
                continue

            if adInfoReqs[indexAd].ecpm >= contentInfoReqs[indexNews].score*self.alpha:
                adInfoRes = self.createAds(adInfoReqs[indexAd], pos)
                listAds.append(adInfoRes)

                indexAd     += 1
                pos         += 1
            else:
                contentInfoRes = self.createContent(contentInfoReqs[indexNews], pos)
                listNews.append(contentInfoRes)

                indexNews += 1
                pos += 1

        if self.insertAds(pos, listAds, fixedPosAd):
            pos += 1

        while indexNews<len(contentInfoReqs):
            if self.insertAds(pos, listAds, fixedPosAd):
                pos += 1
                continue

            contentInfoRes = self.createContent(contentInfoReqs[indexNews], pos)
            listNews.append(contentInfoRes)

            indexNews += 1
            pos += 1

        if len(listAds)<self.maxAdsNum and indexAd<len(adInfoReqs) and (len(listAds)<=0 or (len(listAds)>0 and pos-listAds[-1].pos>self.maxInterval)):
            adInfoRes = self.createAds(adInfoReqs[indexAd], pos)
            listAds.append(adInfoRes)

        listAds.sort(key=lambda x:x.pos)
        listNews.sort(key=lambda x:x.pos)

    """
    广告和资讯混合排序入口
    """
    def mixRank(self, mixRankerRequest):
        listAds, listNews = [], []
        self.mixProcess(mixRankerRequest, listAds, listNews)

        mixRankerResponse = MixRankerResponse()
        mixRankerResponse.adInfoRes      = listAds
        mixRankerResponse.contentInfoRes = listNews

        return mixRankerResponse