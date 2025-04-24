import streamlit as st
import spacy
from collections import Counter
import re

st.set_page_config(page_title="YouTagger", layout="centered")
st.title("🎬 YouTagger – Video Tag Optimizer")
st.write("Generate relevant tags from your YouTube video title and description.")

nlp = spacy.load("en_core_web_sm")

title = st.text_input("Video Title")
description = st.text_area("Video Description")

if st.button("Generate Tags"):
    text = f"{title} {description}"
    doc = nlp(text.lower())

    tags = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop]
    tags = [re.sub(r"[^\w\s-]", "", tag).strip() for tag in tags if len(tag) > 2]

    most_common = [tag for tag, count in Counter(tags).most_common(10)]

    if most_common:
        st.subheader("Suggested Tags:")
        st.write(", ".join(most_common))
    else:
        st.warning("No tags found. Try a longer description.")