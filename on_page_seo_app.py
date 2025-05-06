import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("SEO On-Page Audit Tool")

url = st.text_input("Enter website URL (with https://):")

if st.button("Run Audit") and url:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        st.subheader("Title")
        st.write(soup.title.string.strip() if soup.title else "No title tag found.")

        st.subheader("Meta Description")
        meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        st.write(meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else "Meta description not found.")

        h1_tags = soup.find_all("h1")
        st.subheader("H1 Tags")
        if h1_tags:
            for i, h1 in enumerate(h1_tags, 1):
                st.write(f"H1-{i}: {h1.get_text(strip=True)}")
        else:
            st.write("No H1 tags found.")

        text = soup.get_text(separator=' ')
        words = text.split()
        st.subheader("Word Count")
        st.write(f"{len(words)} words")

        images = soup.find_all("img")
        missing_alt = [img for img in images if not img.get("alt")]
        st.subheader("Images Missing ALT Text")
        st.write(f"{len(missing_alt)} out of {len(images)} images missing ALT tags.")

    except Exception as e:
        st.error(f"Error: {str(e)}")
