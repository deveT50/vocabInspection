# vocabInspection
CBOW言語モデル（２次元）の空間上の広がりを探索する  
gensim/python  

gensim.models.word2vecのCBOWで作成した言語モデル（２次元）内の語彙の関係を探索するデモ。  
ブラウザ上に描かれた２次元矩形をクリックすると、その位置からゴール単語への最短パスをA-Starアルゴリズムで計算し、指定数の単語リストとして出力する。  
これにより、モデル空間内における任意の単語間の位置関係を提示すると共に、現実的な会話においてはある単語（＝トピック）から別の単語（＝トピック）へと違和感なく話題を変遷させるための指標を得ることが可能となる。  

概要：「もうこの話題飽きたんだけど、どう変えていいかわからない」時に使う。  
デモ： <https://vocab-inspection.herokuapp.com/>  

スクリーンショット  
![デモ](https://github.com/deveT50/images/blob/master/vocabInspection/screen_1.png "デモ")　　

###サーバ配置ファイル  
####設定ファイル等
* static ・・・・・・・・・・・・・・・ flaskが指定するjs,css,イメージファイル等を配置するディレクトリ  
* client.js ・・・・・・・・・・・・ クライアントで実行する２次元空間の描画、サーバとのajax通信処理  
* style.css ・・・・・・・・・・・・ クライアント側スタイルシート  
* templates ・・・・・・・・・・・・ flaskが指定するhtmlファイルを配置するディレクトリ  
* Procfile ・・・・・・・・・・・・・ Herokuに対してアプリケーションの種別を指定するファイル  
* requirements.txt ・・・・・ Herokuに対してアプリケーションが使用するモジュールを指定するファイル  
* runtime.txt ・・・・・・・・・・ Herokuに対してアプリケーションが使用する言語を指定するファイル  
####アルゴリズム等
* astar.py ・・・・・・・・・・・・・ A-Starアルゴリズムのモジュール。 <http://qiita.com/masashi127/items/0c794e28f4b295ad82c6> を一部改変して使用した。  
* out.model ・・・・・・・・・・・・ gensim.models.word2vecで作成した言語モデル。データはlivedoor ニュースコーパス <http://www.rondhuit.com/download.html#ldcc> の一部を使用した。  
* vocab_map_2d.py ・・・・・・ サーバ側実行ファイル本体。クライアントからPOSTされた座標をmodel内で対応する単語に変換して返す。  
* word2vec_map.py ・・・・・・ サーバ側実行モジュール。ベクトルからmodel内で対応する単語を取り出す。  

###model作成用ファイル  
* testtext ・・・・・・・・・・・・・ 学習に使用するテキストデータを格納する  
* test1~test5.txt ・・・・・・ 学習に使用するテキストデータ  
* 01_mecab_devider.py ・・ テキストデータを分かち書きし、名詞のみ抽出したtxtファイルを作成する。実行後、wakati_text.txtが作成される。  
* 02_word2vec_train.py ・ gensim.models.word2vecでmodelを作成する。01_mecab_devider.pyで出力されたtxtファイルを引数に指定する。  

* * *

###注意事項
####学習時
* データに含まれる単語数があまりにも少ない場合、word2vecでmodel作成に失敗する。
* 02_word2vec_train.pyが出力するmodelは"out.model"となっているため、同梱しているmodelはそのまま実行すると上書きされる。01_mecab_devider.pyの出力ファイルについても同様。

####実行時
* 「パスの単語数」で指定する単語数は（現在は）正確な値にならない。今後対応する。
* 2Dマップをクリックして実行した場合と、「スタート単語」「ゴール単語」を指定して[送信]ボタンにより実行した場合とでは、同じ単語であってもパスの位置がずれる。これはクリック座標を単語に変換する際に近似値を使用することが主な理由であると考える。また、そもそもmodel空間に存在する単語には重複があり、（現在は）１単語が与えられてもその位置は一意に定まらない。  





