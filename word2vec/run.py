from dataGetter import getNews, getPriceByDate
from datetime import date
import sys
import re

glove = {}
_output_dir = "output/"

def vecAdd(a,b):
    return [a[i]+b[i] for i in range(len(a))]

def findVec(word):
    if word in glove:
        return glove[word]
    else:
        return None

if __name__ == '__main__':
    tickers = sys.argv
    tickers.pop(0)
    offset = tickers.pop(0)

    #f = open(file='glove.6B.100d.txt',encoding = 'utf-8')
    #print("pumping vectors...")
    #for l in f:
    #    vec = l.replace("\n", "").split(" ")
    #    ind = vec.pop(0)
    #    glove[ind] = [float(vec[i]) for i in range(100)]
    #print("pumping done!")
    #f.close()

    fw = open( file = _output_dir + "COMBINED_" + offset + '_output.txt', mode = 'w+', encoding = "utf-8" )
    for ticker in tickers:
        print("fetching news of " + ticker + "...")
        newsList = getNews(ticker)
        print("news loaded!")

        print("matching word vector...")
        vecList = {}
        for news in newsList:
            wordl = re.split( '\s|\'|,', news['title'] )
            vec = [ 0 for i in range(100) ]

            c = 0
            for w in wordl:
                v = findVec(w.lower())
                if v != None:
                    c = c+1
                    vec = vecAdd(vec, v)
            if c > 0:
                for i in range(len(vec)):
                    vec[i] = vec[i] / c
                vecList[ news['date'] ] = vec
        print("matched all words!")

        print("preparing output...")
        out = []
        for k in vecList:
            p = getPriceByDate(ticker, k, int(offset) )
            pp = getPriceByDate(ticker, k, int(offset) - 1 )
            if p != None and p["close"] != None and pp != None and pp["close"] != None:
                #print((p["close"] - pp["close"]) / pp["close"] * 100)
                out.append({
                    "price": (p["close"] - pp["close"]) / pp["close"] * 100,
                    "vec": vecList[k]
                })

        print("start writing output file for " + ticker + "...")

        try:
            for i in out:
                fw.write( str(i["price"]) + "," + ",".join( str(x) for x in i["vec"]  ) + "\n" )
        finally:
            print( "finish output file for " + ticker )
    fw.close()
    print("[finished]")