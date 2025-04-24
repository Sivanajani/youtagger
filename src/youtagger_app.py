import streamlit as st
import spacy
from collections import Counter
import re
from langdetect import detect, LangDetectException

st.set_page_config(page_title="YouTagger", layout="centered")
st.title("YouTagger – Video Tag Optimizer")
st.write("Generate relevant tags from your YouTube video title and description.")

title = st.text_input("Video Title / Videotitel")
description = st.text_area("Video Description / Videobeschreibung")

if st.button("Generate Tags / Tags generieren"):
    text = f"{title} {description}"
    try:
        lang = detect(text)
        st.info(f"Detected language: {lang}")
    except LangDetectException:
        st.warning("Could not detect language. Please enter more text.")
        lang = None

    if lang == "de":
        nlp = spacy.load("de_core_news_sm")
    else:
        nlp = spacy.load("en_core_web_sm")

    doc = nlp(text.lower())

    tags = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop]
    tags = [re.sub(r"[^\w\s-]", "", tag).strip() for tag in tags if len(tag) > 2]
    most_common = [tag for tag, count in Counter(tags).most_common(10)]

    if most_common:
        st.subheader("Suggested Tags / Vorgeschlagene Tags:")
        st.write(", ".join(most_common))
    else:
        st.warning("No tags found. Try a longer description. / Keine Tags gefunden. Versuche eine längere Beschreibung.")
