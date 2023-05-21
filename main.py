
import music2ps


mp = music2ps.music()
mp.set_path(NEUTRINO='NEUTRINO', music='さくら.musicxml', lyrics='さくら.txt')
model = mp.load_model('wiki_model_sg_20.model', max_word=200, similar_percent=0.6)
texts = mp.load_lyrics_file()
converted_text = mp.convert(model=model, texts=texts)
mp.run(converted_text)
mp.play(converted_text)
