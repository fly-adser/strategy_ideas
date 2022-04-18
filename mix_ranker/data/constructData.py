import pandas as pd

file_path = "../data/"
def constructData(file_name):
    requestId = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                 '2', '2', '2', '2', '2', '2','2', '2', '2', '2', '2']
    isAd      = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    ecpm      = [4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                 5, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0]
    posFlag   = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    adId      = [str(i) for i in range(1, 23)]
    docId     = [str(i) for i in range(1, 23)]
    score     = [0, 0, 0, 8, 7, 6, 5, 4, 3, 2, 1,
                 0, 0, 0, 8, 7, 6, 5, 4, 3, 2, 1]
    pos       = [1, 4, 7, 2, 3, 5, 6, 8, 9, 10, 11,
                 2, 5, 8, 1, 3, 4, 6, 7, 9, 10, 11]
    pages     = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    dic = {'requestId': requestId, 'adId': adId, 'ecpm': ecpm, 'posFlag': posFlag,
           'docId': docId, 'score': score, 'isAd': isAd, 'pos':pos, 'pages': pages}

    df = pd.DataFrame(dic)
    df.to_csv(file_name, index=False)

def main():
    constructData("test.csv")

if __name__ == '__main__':
    main()