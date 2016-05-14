import shutil
import PILL as pl
import urllib
import os
from bs4 import BeautifulSoup
import sys, traceback
import nltk
from nltk.corpus import stopwords

def getRelevantImages(results, query):

    index = 0
    for res in results:
        title = res[0]
        url = res[1]
        summary = res[2]
        try:
          soup = BeautifulSoup(urllib.urlopen(url))
          imageTag = soup.find("meta", {"property":"og:image"})
          if imageTag is None:
              imageUrl = soup.find("meta", {"property":"og:image"})['content']
              print imageUrl
              fn = saveImage(imageUrl, index)
              res = (title, url, summary, fn)
              results[index] = res
          else:
              allImages = soup.find_all("img")
              for img in allImages:
                  imgText = img.find_next_sibling()
                  if imgText is not None:
                    imgText = imgText.findAll(text=True)
                    print imgText
                    if imgText:
                        print 's is', imgText
                        flag = checkImgRelevancy(query, imgText[0])
                        if (flag):
                            siu = saveImage(img["src"], index)
                            res = (title, url, summary, siu)
                            results[index] = res
                            print "Image saved from Sibling Logic"
                            
          index = index+1
        except:
           print "error while feeding url to beautiful soup", sys.exc_info()[0]
           traceback.print_exc(file=sys.stdout)
           continue

def saveImage(imageUrl, index):
    filename = os.getcwd() + '/searchengine/static/searchengine/img/' + str(index) + '.jpg'
    f = open(filename,'wb')
    f.write(urllib.urlopen(imageUrl).read())
    f.close()
    return 'searchengine/img/'+ str(index) + '.jpg'

def removeStopWordsFromQuery(query):
    queryWords = nltk.word_tokenize(query)
    print queryWords
    filteredWordList = queryWords[:]
    for word in queryWords: 
        if word in stopwords.words('english'):
            filteredWordList.remove(word)
    print filteredWordList
    return filteredWordList

def checkImgRelevancy(query, text):
    queryWrdsList = removeStopWordsFromQuery(query)
    text = text.lower()
    for word in queryWrdsList:
        if word.lower() in text:
            return True
    return False
        

t = [('London', 'http://www.dawn.com/news/1058258/iran-nuclear-deal-reached', 'London is the capital city')]
getRelevantImages(t, "nawaz sharif in isb meeting")       

            



            
