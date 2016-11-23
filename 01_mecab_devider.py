#-*- encoding: utf-8 -*-
#! /usr/bin/env python

#http://qiita.com/yasunori/items/31a23eb259482e4824e2


import os
import sys
import MeCab

reload(sys)
sys.setdefaultencoding("utf-8")


mecab = MeCab.Tagger(' -d /usr/lib/mecab/dic/mecab-ipadic-neologd')

STOP_WORD = "1 2 3 4 5 6 7 8 9 0 １ ２ ３ ４ ５ ６ ７ ８ ９ ０ の ○ ● ◎ □ ■ ^ - 。 、 「 」 （ ） ? ？ ： ， , ． ! ！ # $ % & ' ( ) = ~ | ` { } * + ? _ > [ ] @ : ; / . ¥ ^ 【 】 ￥ ＿ ／ 『 』 ＞ ？ ＿ ＊ ＋ ｀ ｜ 〜 ＊ ＋ ＞ ？ ＃ ” ＃ ＄ ％ ＆ ’ \" ・".split()


def tokenize(text):
    '''
    とりあえず形態素解析して名詞だけ取り出す感じにしてる
    '''
    node = mecab.parseToNode(text)
    while node:
        if node.feature.split(',')[0] == '名詞':
            yield node.surface.lower()
        node = node.next


def get_words(contents):
    '''
    記事群のdictについて、形態素解析してリストにして返す
    '''
    ret = []
    for k, content in contents.items():
        ret.append(get_words_main(content))
    return ret


def get_words_main(content):
    '''
    一つの記事を形態素解析して返す
    '''
    return [token for token in tokenize(content)]




def preprocess_japanese_doc(argtxt):
    wakati_formalize = []
    wakati_text=""
    #wakati_array=[]

    text=unicode(argtxt,'utf-8')
    #encodeしたテキストは変数に入れておく（寿命対策）
    encoded_text=text.encode('utf-8')
    #分かち書き
    wakati_raw = get_words_main(encoded_text)

    for row in wakati_raw:
        #空白消去と小文字化
        row = row.rstrip().lower()
        #STOPWORDを除去
        for sw in STOP_WORD:
            row = row.replace(sw,'')
        
        #wakati_formalize.append(unicode(row,'utf-8'))
        wakati_formalize.append(row.encode('utf-8'))

    #textに追加
    wakati_text = ' '+ wakati_text + (' '.join(wakati_formalize))
    #wakati_array=wakati_formalize
    return wakati_text
    #return wakati_array



if __name__ == "__main__":


    # コーパスのロード-----------------
    docs = {}
    #読み込むファイルのあるディレクトリ
    corpus_dir = 'testtext'
    for filename in os.listdir(corpus_dir):
        path = os.path.join(corpus_dir, filename)
        doc = open(path).read().strip().lower()
        docs[filename] = doc
    #多分key=filename
    names = docs.keys()

    # main ---------------------------
    f = open("wakati_text.txt", 'w')
    strtxt=""
    for name in names:
        #preprocessする
        txt=preprocess_japanese_doc(docs[name])
        #textに書き出す
        f.write((txt))

    f.close()

