import boto3
import jaconv
import streamlit as st
from sudachipy import Dictionary

polly = boto3.client("polly")
tokenizer = Dictionary().create()


def make_ruby(text: str, rt: str) -> str:
    """Generater Ruby tagged text"""
    return f"<ruby>{text}<rt>{rt}</rt></ruby>"


def kana_with_romaji_ruby(text: str) -> str:
    hiragana = jaconv.kata2hira(text)
    romaji = jaconv.kana2alphabet(hiragana)
    return make_ruby(text, romaji)


def kana_to_romaji():
    st.write("""## Hiragana and Katakana to Romaji

    パイコンえいぱっく
    """)

    text = st.text_input("Hiragana and Katakana texts:")
    if text:
        result = kana_with_romaji_ruby(text)
        st.write(f"#### {result}", unsafe_allow_html=True)


def word_segmentation():
    st.write("""## Word segmentation

    すもももももももものうち
    """)

    text = st.text_input("Text for Word segmentation:")
    if text:
        words = []
        for token in tokenizer.tokenize(text):
            words.append(kana_with_romaji_ruby(str(token)))
        result = " / ".join(words)
        st.write(f"#### {result}", unsafe_allow_html=True)


def add_reading(text: str) -> tuple[str, str]:
    """Add Hiranaga ruby to text"""
    hiragana = ""
    romaji = ""
    for token in tokenizer.tokenize(text):
        ruby_kana = jaconv.kata2hira(token.reading_form())
        hiragana += make_ruby(token, ruby_kana) + " "
        ruby_romaji = jaconv.kata2alphabet(token.reading_form())
        romaji += make_ruby(token, ruby_romaji) + " "
    return hiragana, romaji


def kanji_reading():
    st.write("""## Kanji Readings

    今日は一月一日で日曜日
    """)
    text = st.text_input("Text with Kanji:")
    if text:
        hiragana, romaji = add_reading(text)
        st.write(f"#### {hiragana}", unsafe_allow_html=True)
        st.write(f"#### {romaji}", unsafe_allow_html=True)


def text_to_speech():
    st.write("""## Text to Speach

    東京、英語
    """)
    text = st.text_input("Text for speech:")
    if text:
        hiragana, romaji = add_reading(text)
        st.write(f"#### {hiragana}", unsafe_allow_html=True)
        st.write(f"#### {romaji}", unsafe_allow_html=True)

        ssml_text = f'<speak><prosody rate="slow">{text}</prosody></speak>'
        result = polly.synthesize_speech(
            Text=ssml_text, OutputFormat="mp3", TextType="ssml", VoiceId="Mizuki")
        with open("japanese.mp3", "wb") as f:
            f.write(result["AudioStream"].read())
        st.audio("japanese.mp3")


def main():
    st.title("Learn Japanese🇯🇵 with Python🐍")
    st.write("PyCon APAC ver.")

    kana_to_romaji()
    st.write("------")

    word_segmentation()
    st.write("------")

    kanji_reading()
    st.write("------")

    text_to_speech()


if __name__ == "__main__":
    main()
