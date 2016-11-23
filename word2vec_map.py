#-*- encoding: utf-8 -*-
#! /usr/bin/env python



from gensim.models import word2vec
import argparse
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding("utf-8")



#モデルロード
model = word2vec.Word2Vec.load("out.model")


def vec2word(model,vec):
    words=[]
    npvec=np.asarray(vec,dtype=np.float64)
    for i in range(3):
        #words[i]=model.similar_by_vector(vec)[i][0]
        p=model.similar_by_vector(npvec)
        words.append(p[i][0].encode("utf-8").decode('utf-8'))
    return words

if __name__ == '__main__':
    #npvec=np.asarray(args.vector,dtype=np.float64)
    result=vec2word(model,(0,0))
    
    for i in range (3):
        print result[i]


