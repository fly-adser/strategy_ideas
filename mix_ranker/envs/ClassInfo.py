
class AdinfoReq(object):

    def __init__(self, adId=None, ecpm=None, fixedPos=None):
        self.adId     = adId
        self.ecpm     = ecpm
        self.fixedPos = fixedPos

class ContentInfoReq(object):

    def __init__(self, contentId=None, score=None, fixedPos=None):
        self.contentId = contentId
        self.score     = score
        self.fixedPod  = fixedPos

class AdinfoRes(object):

    def __init__(self, adId=None, ecpm=None, pos=None):
        self.adId = adId
        self.ecpm = ecpm
        self.pos  = pos

class ContentInfoRes(object):

    def __init__(self, contendId=None, score=None, pos=None):
        self.contendId = contendId
        self.score     = score
        self.pos       = pos

class MixRankerRequest(object):

    def __init__(self, requestId=None, pages=None, adInfoReqs=[], contentInfoReqs=[]):
        self.requestId       = requestId
        self.pages           = pages
        self.adInfoReqs      = adInfoReqs
        self.contentInfoReqs = contentInfoReqs

class MixRankerResponse(object):

    def __init__(self, adInfoRes=[], contentInfoRes=[]):
        self.adInfoRes = adInfoRes
        self.contentInfoRes = contentInfoRes