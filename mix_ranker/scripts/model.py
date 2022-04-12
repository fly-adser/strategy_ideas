
from envs.ClassInfo import *

"""
广告混排服务模拟，说明文档参考：
"""
class Mix_RankerV1(object):

    def __init__(self, topPos=1, maxInterval=0):
        self.topPos      = topPos
        self.maxInterval = maxInterval

    """
    支持广告保位诉求(如品牌广告)
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
        fixedPosAd = {}
        for i in range(len(adInfoReqs)):
            adInfoReq = adInfoReqs.get(i)
            if adInfoReq.fixedPos and adInfoReq.fixedPos>0:
                fixedPosAd[adInfoReq.fixedPos] = adInfoReq
                del adInfoReqs[i]
                i -= 1

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
