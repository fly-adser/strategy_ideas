from mix_ranker.src.model.modelForScoreV1 import Mix_RankerV1
from mix_ranker.src.mix_common.Estimate import Estimate
from mix_ranker.src.mix_common.ClassInfo import *
import pandas as pd
import numpy as np
import os

file_path = "../data/"
def load_data(file_name):
    file_stats = os.stat(file_path + file_name)
    print(f'File Size in MegaBytes is {file_stats.st_size / (1024 * 1024)} MB')
    if (file_stats.st_size / (1024 * 1024)) >= 600:
        reader = pd.read_csv(file_path + file_name, iterator=True)
        chunkSize = 250000
        loop = True
        chunks = []
        k = 0
        while loop:
            try:
                chunk = reader.get_chunk(chunkSize)
                chunks.append(chunk)
                k += 1
                print(k, end=',')
            except StopIteration:
                loop = False
                print("Iteration is stopped.")
        data = pd.concat(chunks, ignore_index=True)
    else:
        data = pd.read_csv(file_path + file_name)
    return data



def createAds(rows):
    adinfoReq = AdinfoReq()
    adinfoReq.adId = rows['adId']
    adinfoReq.ecpm = rows['ecpm']
    adinfoReq.fixedPos = rows['posFlag']

    return adinfoReq

def createNews(rows):
    contentInfoReq = ContentInfoReq()
    contentInfoReq.contentId = rows['docId']
    contentInfoReq.score     = rows['score']

    return contentInfoReq

def createRequest(frame):
    mixRankerRequest            = MixRankerRequest()
    adInfoReqs, contentInfoReqs = [], []
    for index, rows in frame.iterrows():
        pages = rows['pages']
        if rows['isAd']==1:
            adInfoReq = createAds(rows)
            adInfoReqs.append(adInfoReq)
        else:
            contentInfoReq = createNews(rows)
            contentInfoReqs.append(contentInfoReq)

    mixRankerRequest.pages           = pages
    mixRankerRequest.adInfoReqs      = adInfoReqs
    mixRankerRequest.contentInfoReqs = contentInfoReqs

    return mixRankerRequest

def sendRequest(data, alpha):
    mixRanker = Mix_RankerV1(2, 3, alpha)
    estimate  = Estimate()
    groups = data.groupby(['requestId'])

    for each in groups:
        mixRankerRequest  = createRequest(each[1])
        mixRankerResponse = mixRanker.mixRank(mixRankerRequest)
        estimate.computeDCGForAds(mixRankerResponse.adInfoRes)
        estimate.computeDCGForNews(mixRankerResponse.contentInfoRes)

    print("alpha:", alpha, "DCGforAd:", estimate.cumulateAds, "DCGForNews:", estimate.cumulateNews,
          "adNum:", len(estimate.adPos), "avgPos:", np.mean(estimate.adPos), 'newNum:', len(estimate.newPos), 'avgNewPos:', np.mean(estimate.newPos))

def createAdRes(rows):
    adinfoRes = AdinfoRes()
    adinfoRes.ecpm = rows['ecpm']
    adinfoRes.pos  = rows['pos']

    return adinfoRes

def createContentRes(rows):
    contentInfoRes = ContentInfoRes()
    contentInfoRes.score = rows['score']
    contentInfoRes.pos   = rows['pos']

    return contentInfoRes

def createResponse(frame):
    listAds, listNews = [], []
    for index, rows in frame.iterrows():
        if rows['isAd']==1:
            adInfoRes = createAdRes(rows)
            listAds.append(adInfoRes)
        else:
            contentInfoRes = createContentRes(rows)
            listNews.append(contentInfoRes)

    return listAds, listNews

def estimateOrigin(data):
    estimate = Estimate()
    groups = data.groupby(['requestId'])

    for each in groups:
        listAds, listNews = createResponse(each[1])

        estimate.computeDCGForAds(listAds)
        estimate.computeDCGForNews(listNews)

    print("alpha:", -1, "DCGforAd:", estimate.cumulateAds, "DCGForNews:", estimate.cumulateNews,
          "adNum:", len(estimate.adPos), "avgPos:", np.mean(estimate.adPos), 'newNum:', len(estimate.newPos), 'avgNewPos:', np.mean(estimate.newPos))

def dataType(data):
    data['ecpm'].astype('int64')
    data['posFlag'].astype('int32')
    data['score'].astype('float64')
    data['isAd'].astype('int32')
    data['pos'].astype('int32')
    data['pages'].astype('int32')

def main():
    file_name = "test.csv"
    data = load_data(file_name)
    dataType(data)
    estimateOrigin(data)
    alphas = [0.01, 0.1, 1, 10, 100]
    for alpha in alphas:
        sendRequest(data, alpha)

if __name__ == "__main__":
    main()