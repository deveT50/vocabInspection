#!/usr/bin/env python
# -*- coding: utf-8 -*-
#http://tokibito.hatenablog.com/entry/20111204/1322989305
#http://qiita.com/Nawada/items/cf6e4ee46b244fba13c6


#for flask
import os
from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from flask import send_from_directory
import json

from gensim.models import word2vec
from word2vec_map import vec2word
import astar
import sys
import numpy as np


reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

#モデルロード
model = word2vec.Word2Vec.load("out.model")

#tupleをlistに直す
def tuple2list(_tuple):

    l=[]
    for i in _tuple:
        if isinstance(i,tuple):
            l.append(tuple2list(i))
        else:
            l.append(i)
    return l



#root
@app.route('/')
def main():
    
    return render_template("index.html")


#pos2word
@app.route('/pos2word', methods=['POST'])
def pos2word():

    get_json =request.json
    trg=json.loads(get_json)
    px=float(trg['x'])
    py=float(trg['y'])
    mapw=400
    maph=400

    #正規化する

    px=float(px)-mapw/2.0
    py=float(py)-maph/2.0
    px=float(px)/mapw
    py=float(py)/maph
    
    vec=[px,py]
    print "vec",vec
    #変換する
    resword=vec2word(model,vec)
    
    #print result[0]

    result={'word':resword[0], 'vector':vec}
    return jsonify(result)



#aster
@app.route('/aster', methods=['POST'])
def req_aster():

    get_json =request.json
    trg=json.loads(get_json)

    mapw=400
    maph=400
    #start単語
    startW=trg['sw']
    #goal単語
    goalW=trg['gw'] #unicode(trg['gw'],'utf-8')
    #座標クリックで送信されたかどうか
    isButton=trg['isButton']
    #pathWの数
    wordNum=int(trg['reqLen'])

    #startWがモデルに含まれない場合
    if startW not in model.vocab:
        #modelに含まれる単語に置き換える！
        startW="スマートフォン"
    #start語のベクトル表現を返す
    start=model[startW.decode('utf-8')]


    #座標クリックの場合
    if isButton==0:

        #clientマウス座標
        px=float(trg['x'])
        py=float(trg['y'])

        #座標クリックで送信された場合
        #マウス座標を正規化する
        vx=px-mapw/2.0
        vy=py-maph/2.0
        vx=vx/mapw
        vy=vy/maph
        #マウス座標ベクトル
        start=[vx,vy]

        #マウス座標を単語に変換する
        startW=vec2word(model,start)[0]


    #goalWがモデルに含まれない場合
    if goalW not in model.vocab:
        #modelに含まれる単語に置き換える！
        goalW="スマートフォン"
    #start語とgoal語が同じ場合（asterの計算結果がlen()=0になるので）
    #goal語を近似する
    if startW==goalW:
        goalW=model.most_similar(positive=[goalW.decode('utf-8')], topn=1)[0][0]

    #goal語のベクトル表現を返す
    goal=model[goalW.decode('utf-8')]

    #スタートとゴールのベクトルを１０００倍する(astarを小数点に対応させてない)
    #小数第３位までは保持する(w2vのモデルが３位まで対応している)
    #s=(round(vec[0],3)*1000, round(vec[1],3)*1000)
    s=(round(start[0],3)*1000, round(start[1],3)*1000)
    g=(round(goal[0],3)*1000, round(goal[1],3)*1000)

    #スタートからゴールへの経路を求める
    res=tuple2list(astar.astar(s,g))
    #arrayにする(numpyでブロードキャスト計算したいため)
    res=np.array(res,np.int)


    #astarで得られた経路のうち、単語に変換するもの（経路が長過ぎるので間引く）
    wordList=[]
    stride=len(res)/wordNum
    #正規化する
    regres=(res-mapw/2.0)/mapw
    #欲しい個数だけpathの単語を得る    
    wordList=[vec2word(model,x)[0] for x in regres[::stride]]
    #startとgoalを連結
    wordList.insert(0,startW)
    wordList.append(goalW)


    #日本語にする
    pathWList=[]
    for w in wordList:
        #print w.decode('utf-8').encode('utf-8')
        pathWList.append(w.decode('utf-8').encode('utf-8'))


    #クライアント座標に直す
    clcoo=res/1000.0
    #print clcoo
    for i in range(len(clcoo)):
        clcoo[i][0]=(clcoo[i][0]*mapw)+(mapw/2.0)
        clcoo[i][1]=(clcoo[i][1]*maph)+(maph/2.0)
    

    #start,goalをクライアント座標に
    startPos=[s[0]/1000*mapw+mapw/2.0, s[1]/1000*maph+maph/2.0]
    goalPos=[g[0]/1000*mapw+mapw/2.0, g[1]/1000*maph+maph/2.0]


    #クライアントに返す
    result={'pathW':pathWList,
     'coordinate':clcoo.tolist(),
     'length':len(clcoo),
    }
    return jsonify(result)


if __name__ == "__main__":
    app.debug = False
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    

