import jaconv
import streamlit as st
from sudachipy import Dictionary

from kanji_reading_with_level import add_reading as add_reading_with_level

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

    パイコン あめりか
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
    st.write("""## Kanji Reading

    一人の日本人の大人が一人前のラーメンを食べる
    """)
    text = st.text_input("Text with Kanji:")
    if text:
        hiragana, romaji = add_reading(text)
        st.write(f"#### {hiragana}", unsafe_allow_html=True)
        st.write(f"#### {romaji}", unsafe_allow_html=True)


def kanji_reading_with_level():
    st.write("""## Kanji Reading with Kanji level

    日本語を勉強する
    """)

    st.markdown("[The Python Tutorial](https://docs.python.org/3.13/tutorial/index.html)")

    levels = {"N1": "1", "N2": "2", "N3": "3", "N4": "4", "N5": "5"}
    text = st.text_input("Text:")
    alphabet = st.toggle("Alphabet(romaji) annotation(default: Hiragana)")
    level = st.pills("Kanji level", levels, selection_mode="single")
    if text:
        text = text.replace(" ", "")
        level_value = levels.get(level)
        result = add_reading_with_level(text, level_value, alphabet)
        result = result.replace("\n", " ")
        st.write(f"#### {result}", unsafe_allow_html=True)


def main():
    st.title("Learn Japanese🇯🇵 with Python🐍")
    st.write("PyCon US 2025 ver.")

    kana_to_romaji()
    st.write("------")

    word_segmentation()
    st.write("------")

    kanji_reading()
    st.write("------")

    kanji_reading_with_level()


if __name__ == "__main__":
    main()
