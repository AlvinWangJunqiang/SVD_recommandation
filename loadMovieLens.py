
import sys
import os


def loadMovieLensTrain(fileName='u1.base'):
    str1 = './movielens/'                         
    
    prefer = {}
    for line in open(str1+fileName,'r'):     
        (userid, movieid, rating,ts) = line.split('\t')    
        prefer.setdefault(userid, {})     
        prefer[userid][movieid] = float(rating)    

    return prefer      



def loadMovieLensTest(fileName='u1.test'):
    str1 = './movielens/'    
    prefer = {}
    for line in open(str1+fileName,'r'):    
        (userid, movieid, rating,ts) = line.split('\t')  
        prefer.setdefault(userid, {})    
        prefer[userid][movieid] = float(rating)   
    return prefer                   


if __name__ == "__main__":
    
    trainDict = loadMovieLensTrain()
    testDict = loadMovieLensTest()

    print (len(trainDict))
    print (len(testDict))

                        

















