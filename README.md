# music2ps
## 使い方
### 1. NEUTRINOをダウンロードする
[NEUTRINOのダウンロードページ](https://studio-neutrino.com/)  
ダウンロードしたNEUTRINOはmain.pyと同一ディレクトリにコピーしてください  
（**NEUTRINO/NEUTRINOにならないようにしてください**）
### 2. NEUTRINO/score/musicxmlに替え歌を作成したい（.musicxml）を入れる
sample1.musicxmlの中身は（さくら）
### 3. NEUTRINO/score/lyricsを作成し、歌詞を書いた（.txt）を入れる
歌詞はネットで調べてコピペ
### 4. main.pyを編集する
```
mp.set_path(NEUTRINO='NEUTRINO', music='さくら.musicxml', lyrics='さくら.txt')
```
引数musicに2.のファイル名（.musicxml）、引数lyricsに3.のファイル名（.txt）を入れる（相対パスではない、ただのファイル名）
### 5. main.pyを実行する
替え歌が再生される
### 6. NEUTRINO/output/曲名.wavを再生
替え歌が再生される
