import os
from contextlib import closing
from pathlib import Path

import boto3
import deepl
import jaconv
import streamlit as st
from sudachipy import Dictionary

PART_OF_SPEECH = {
    "名詞": "noun",
    "形容詞": "adjective",
    "動詞": "verb",
    "助詞": "particle",
    "形容動詞": "adjective verb",
    "副詞": "adverb",
    "助動詞": "auxiliary",
    "連体詞": "prenominal adjective",
    "代名詞": "pronoun",
    "補助記号": "symbol",
    "接頭辞": "prefix",
    "感動詞": "interjection",
}

polly = boto3.client('polly')

tokenizer = Dictionary().create()

translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))


def do_polly(text: str) -> None:
    ssml_text = f'<speak><prosody rate="slow">{text}</prosody></speak>'
    result = polly.synthesize_speech(
        Text=ssml_text, OutputFormat="mp3", TextType="ssml", VoiceId="Mizuki")

    with closing(result["AudioStream"]) as stream:
        Path("japanese.mp3").write_bytes(stream.read())

    return


def translate(text: str) -> str:
    result = translator.translate_text(text, target_lang="EN-US")
    return f"{result.text}"

st.title('Learn Japanese🇯🇵 with Python🐍')

st.write("""## Sample japanese text

* すもももももももものうち
* 一月一日は元日、昨日は大晦日
""")

# Input text
text = st.text_input("**Japanese:**")

if text:
    en_text = translate(text)
    st.write(f"**English text**: {en_text}")

    words = {}
    for i, token in enumerate(tokenizer.tokenize(text)):
        word = token.surface()
        part_of_speech = PART_OF_SPEECH.get(token.part_of_speech()[0], token.part_of_speech()[0])

        if part_of_speech not in ("symbol", "particle"):
            word_en = translate(word)
        else:
            word_en = ""

        reading = token.reading_form()
        reading_hiragana = jaconv.kata2hira(reading)
        reading_roman = jaconv.kata2alphabet(reading)

        words[i] = {
            "word": word,
            "reading(Katakana)": reading,
            "reading(Hiragana)": reading_hiragana,
            "reading(Roman)": reading_roman,
            "english word": word_en,
            "part of speech": part_of_speech
        }

    st.table(words)

    do_polly(text)
    st.audio("japanese.mp3")

