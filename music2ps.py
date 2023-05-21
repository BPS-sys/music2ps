
import gensim
import MeCab
import pykakasi
import subprocess
import os
import shutil
import xml.etree.ElementTree as ET
import string
import winsound


class music():
    filename = None
    lyrics_filename = None
    similar_percent = None
    max_word = None
    NEUTRINO_path = None
    score_path = None
    lyrics_path = None
    musicxml_path = None
    lyrics_filename = None
    abs_filename = None
    abs_xmlfilename = None
    batfile = None
    name = None
    extension = None
    def __init__(self):
        self.tagger = MeCab.Tagger("-Ochasen")
        self.wakati_tagger = MeCab.Tagger("-Owakati")
        self.kks = pykakasi.kakasi()
        self.available_extension = ['musicxml', 'xml']
        # skip文字
        self.xmoji_list = [i for i in string.printable] \
                    + ['「', '」', '〔', '〕', '”', '〈', '〉', '『', '』', '【', '】', '＆', '＊', '・', '（', '）', '＄', 
                       '＃', '＠', '。', '、', '？', '！', '｀', '＋', '￥', '％', '’', '≠', '\u3000', '→', '←', 'Λ']
        # 日本語（小文字）
        self.small_word = ['ゃ', 'ゅ', 'ょ', 'ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ', 'っ',
                           'ャ', 'ュ', 'ョ', 'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ッ']

    def set_path(self, NEUTRINO=None, music=None, lyrics=None):
        self.NEUTRINO_path = NEUTRINO
        self.filename = music
        self.lyrics_filename = lyrics
        self.score_path = os.path.join(self.NEUTRINO_path, 'score')
        self.lyrics_path = os.path.join(self.score_path, 'lyrics')
        self.musicxml_path = os.path.join(self.score_path, 'musicxml')
        self.lyrics_filename = os.path.join(self.lyrics_path, self.lyrics_filename)
        self.abs_filename = os.path.join(self.musicxml_path, self.filename)
        self.abs_xmlfilename = self.abs_filename.split('.')[0]+'_copy.xml'
        self.batfile = os.path.join(self.NEUTRINO_path, 'Run.bat')
        # 読み込んだファイルの拡張子より手前のファイル名
        self.name = self.filename.split('.')[0]
        # 読み込んだファイルの拡張子
        self.extension = self.filename.split('.')[-1]

    def load_lyrics_file(self):
        # 歌詞ファイル読み込み
        with open(self.lyrics_filename, encoding='utf-8') as lyf:
            texts = lyf.read().splitlines()
        # 前処理（空白等削除）
        for i, sentence in enumerate(texts):
            for xmoji in self.xmoji_list:
                sentence = sentence.replace(xmoji, '')
            texts[i] = sentence
        return [i for i in texts if i]

    def load_model(self, filename, max_word=100, similar_percent=0.7):
        self.similar_percent = similar_percent
        self.max_word = max_word
        return gensim.models.Word2Vec.load(filename)

    def convert(self, model=None, texts=None):
        # .xml, .musicxmlコピー
        shutil.copyfile(self.abs_filename, self.abs_xmlfilename)
        # 歌詞改変
        kana = []
        for text in texts:
            node = self.tagger.parseToNode(text)
            wakati = self.wakati_tagger.parse(text).split(' ')[:-1]
            wakati.insert(0, '*')
            wakati.append('*')
            index = 0
            while node:
                conv_hira = ''
                wakati_hira = ''
                before = []
                after = []
                if node.feature.split(',')[-2] == '*':
                    if wakati[index] != '*':
                        # 漢字ー＞ひら
                        for i in self.kks.convert(wakati[index]):
                            wakati_hira += i['hira']
                        # リスト化
                        wakati_hira = [i for i in wakati_hira]
                        # 小文字の合成
                        kana = self._bond(wakati_hira, kana)
                else:
                    if node.feature.split(',')[0] == '名詞':
                        try:
                            similar_word = model.wv.most_similar(wakati[index], topn=self.max_word)
                        except KeyError:
                            # 漢字ー＞ひらがな
                            conv_hira = node.feature.split(',')[-2]
                            # リスト化
                            conv_hira = [i for i in conv_hira]
                            # 小文字の合成
                            kana = self._bond(conv_hira, kana)
                        else:
                            # 類似語抽出
                            for word in similar_word:
                                wakati_hira = ''
                                conv_hira = ''
                                before = []
                                after = []
                                if word[1] < self.similar_percent:
                                    # 漢字ー＞ひら
                                    wakati_hira = node.feature.split(',')[-2]
                                    # リスト化
                                    wakati_hira = [i for i in wakati_hira]
                                    # 小文字の合成
                                    kana = self._bond(wakati_hira, kana)
                                    break
                                else:
                                    # 漢字ー＞ひら
                                    wakati_hira = node.feature.split(',')[-2]
                                    # リスト化
                                    wakati_hira = [i for i in wakati_hira]
                                    # 小文字の合成
                                    before = self._bond(wakati_hira, before)
                                    # 漢字ー＞ひら
                                    for i in self.kks.convert(word[0]):
                                        conv_hira += i['hira']
                                    judge = False
                                    for i in conv_hira:
                                        if i in self.xmoji_list:
                                            judge = True
                                    if judge:
                                        continue
                                    # リスト化
                                    conv_hira = [i for i in conv_hira]
                                    for i, k in enumerate(wakati_hira):
                                        wakati_hira[i] = self.kks.convert(k)[0]['hira']
                                    # カタカナー＞ひらがな等は弾く
                                    if wakati_hira == conv_hira:
                                        continue
                                    # 小文字の合成
                                    after = self._bond(conv_hira, after)
                                    # 前と後の文字数を比較
                                    if len(before) == len(after):
                                        kana += after
                                        break
                            else:
                                # 漢字ー＞ひら
                                wakati_hira = node.feature.split(',')[-2]
                                # リスト化
                                wakati_hira = [i for i in wakati_hira]
                                # 小文字の合成
                                kana = self._bond(wakati_hira, kana)
                    else:
                        # 漢字ー＞ひら
                        wakati_hira = node.feature.split(',')[-2]
                        # リスト化
                        wakati_hira = [i for i in wakati_hira]
                        # 小文字の合成
                        kana = self._bond(wakati_hira, kana)
                index += 1
                node = node.next
        
        for i, word in enumerate(kana):
            temp = ''
            for j in self.kks.convert(word):
                temp += j['hira']
            kana[i] = temp

        for i, word in enumerate(kana):
            if word[-1] in self.small_word and i != len(kana)-1:
                if kana[i+1] == 'う' or kana[i+1] == 'ウ':
                    kana[i+1] = ' '
            if word == 'ゔぁ':
                kana[i] = 'ば'
            elif word == 'ゔぃ':
                kana[i] = 'び'
            elif word == 'ゔぅ':
                kana[i] = 'ぶ'
            elif word == 'ゔぇ':
                kana[i] = 'べ'
            elif word == 'ゔぉ':
                kana[i] = 'ぼ'
        kana = [i for i in kana if i != ' ']
        
        return kana
    
    def _bond(self, hira, l=[]):
        # 小文字の合成
        for i in hira:
            if i in self.small_word and l:
                l[-1] += i
            else:
                l.append(i)
        return l
    
    def run(self,kana):
        # XMLを解析
        tree = ET.parse(self.abs_xmlfilename)
        # 歌詞書き込み
        no_write_count = 0
        root = tree.getroot()
        for i, text in enumerate(root.iter('text')):
            if not text.text == 'ー':
                text.text =  kana[i-no_write_count]
            else:
                no_write_count += 1
        # 保存
        tree.write(os.path.join(self.musicxml_path, 'conv_'+self.name+'.musicxml'), encoding='shift-jis')
        # .bat書き換え
        with open(self.batfile) as rf:
            rf = rf.read().splitlines()
        rf[10] = f'set SUFFIX={self.extension}'
        rf[5] = f'set BASENAME=conv_{self.name}'
        with open(self.batfile, 'w') as wf:
            wf.write('\n'.join(rf))
        # .bat実行
        a = subprocess.Popen(self.batfile)
        a.wait()

    def play(self, text=None):
        if text:
            print(''.join(text))
        winsound.PlaySound(os.path.join(self.NEUTRINO_path, r'output\conv_{}.wav'.format(self.name)), winsound.SND_FILENAME)
