#-*- encoding: utf-8 -*-
#! /usr/bin/env python



from gensim.models import word2vec
import logging
import argparse


parser = argparse.ArgumentParser(
    description='word2vec')
parser.add_argument('filepath',type = str, help='分かち書き済みテキストファイルのパス')
parser.add_argument('-size', type=int, default=2, help='word2vecで作成する特徴ベクトルの次元数')
parser.add_argument('-outpath',type=str, default="out", help='モデルの出力先パス')
parser.add_argument('--min', '-m',type=int, default=5,
                    help='単語の最小出現数。これ以下の単語は無視する。')
parser.add_argument('--window', '-w', type=int, default=1,
                    help='sentence中における、現在の単語と予測した単語との最大距離')
parser.add_argument('--workers', '-wk', type=int, default=4,
                    help='cpuのコア数')

args = parser.parse_args()


# 進捗表示用
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Word2Vecの学習に使用する分かち書き済みのテキストファイルの準備
sentences = word2vec.Text8Corpus(args.filepath)

# Word2Vecのインスタンス作成
# sentences : 対象となる分かち書きされているテキスト
# size      : 出力するベクトルの次元数
# min_count : この数値よりも登場回数が少ない単語は無視する
# window    : 一つの単語に対してこの数値分だけ前後をチェックする
model = word2vec.Word2Vec(sentences, size=args.size, min_count=args.min, window=args.window,workers=args.workers)

# 学習結果を出力する
model.save(args.outpath +".model")

if __name__ == '__main__':
    print "Finish!!!"
