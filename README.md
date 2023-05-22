# music2ps
## 使い方
### 1. NEUTRINOをダウンロードする
[NEUTRINOのダウンロードページ](https://studio-neutrino.com/)  
ダウンロードしたNEUTRINOはmain.pyと同一ディレクトリにコピーしてください  
（**NEUTRINO/NEUTRINOにならないようにしてください**）
### 2. ライブラリのインストール
[MeCabのダウンロードページ](https://www.mlab.im.dendai.ac.jp/~yamada/ir/MorphologicalAnalyzer/MeCab.html)
よりMeCabをダウンロードする（pip install mecab-python3だけではダメ）  
以下のコマンドをコマンドプロンプトで実行
```
pip install mecab-python3
pip install pykakasi
pip install gensim
```
### 3. NEUTRINO/score/musicxmlに替え歌を作成したい（.musicxml）を入れる
初期から入っている  
sample1.musicxmlは（春が来た）  
sample2.musicxmlは（茶摘み）  
sample3.musicxmlは（さくら）
### 4. NEUTRINO/score/lyricsを作成し、歌詞を書いた（.txt）を入れる
歌詞はネットで調べてコピペ  
特殊な読みをする場合は置き換える必要がある  
例)景色（いろ）→いろ
### 5. main.pyを編集する
```
mp.set_path(NEUTRINO='NEUTRINO', music='さくら.musicxml', lyrics='さくら.txt')
```
引数musicに3.のファイル名（.musicxml）、引数lyricsに4.のファイル名（.txt）を入れる（相対パスではない、ただのファイル名）
```
model = mp.load_model('wiki_model_sg_20.model', max_word=200, similar_percent=0.6)
```
第1引数に自作のgensimのword2vecモデルのパスを入れると自作モデルを使った替え歌をつくれる  
（絶対パスか相対パス）
### 6. main.pyを実行する（もしくはmain.ipynb）
替え歌が再生される
### 7. NEUTRINO/output/（.musicxmlのファイル名）.wavを再生
替え歌が再生される
