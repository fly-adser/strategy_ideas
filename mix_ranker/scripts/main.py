from envs.ClassInfo import *
from scripts.model import Mix_RankerV1
import time

def createAds(adId, ecpm, posFlag):
    adInfoReq = AdinfoReq()
    adInfoReq.adId = adId
    adInfoReq.ecpm = ecpm
    adInfoReq.fixedPos = posFlag

    return adInfoReq

def createContentReq(contentId, score):
    contentInfoReq = ContentInfoReq()
    contentInfoReq.contentId = contentId
    contentInfoReq.score     = score

    return contentInfoReq

def createRequest():
    adInfoReqs, contentInfoReqs = [], []

    adIds, ecpms, fixedPos = [1, 2, 3, 4], [180, 200, 160, 140], [0, 0, 1, 0]
    contentIds, scores     = [1, 2, 3, 4, 5, 6, 7, 8, 9], [250, 230, 210, 190, 170, 150, 130, 110, 90]

    for i in range(len(adIds)):
        adInfoReq = createAds(adIds[i], ecpms[i], fixedPos[i])
        adInfoReqs.append(adInfoReq)

    for i in range(len(contentIds)):
        contentInfoReq = createContentReq(contentIds[i], scores[i])
        contentInfoReqs.append(contentInfoReq)

    mixRankerRequest            = MixRankerRequest()
    mixRankerRequest.requestId  = time.time()
    mixRankerRequest.adInfoReqs = adInfoReqs
    mixRankerRequest.contentInfoReqs = contentInfoReqs

    return mixRankerRequest


def main():
    mixRanker         = Mix_RankerV1(1, 2, 3, 1.2)
    mixRankerRequest  = createRequest()
    mixRankerResponse = mixRanker.mixRank(mixRankerRequest)

    adInfoRes, contentInfoRes = mixRankerResponse.adInfoRes, mixRankerResponse.contentInfoRes
    for i in range(len(adInfoRes)):
        print("ad:", adInfoRes[i].adId, "ecom: ", adInfoRes[i].ecpm,  "pos: ", adInfoRes[i].pos)

    for i in range(len(contentInfoRes)):
        print("content: ", contentInfoRes[i].contendId, "score: ", contentInfoRes[i].score,  "pos: ", contentInfoRes[i].pos)

    print("success!")

if __name__ == "__main__":
    main()