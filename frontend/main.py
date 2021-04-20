import requests
import streamlit as st
from PIL import Image

STYLES = {
    "candy": "candy",
    "composition 6": "composition_vii",
    "feathers": "feathers",
    "la_muse": "la_muse",
    "mosaic": "mosaic",
    "starry night": "starry_night",
    "the scream": "the_scream",
    "the wave": "the_wave",
    "udnie": "udnie",
}

# https://discuss.streamlit.io/t/version-0-64-0-deprecation-warning-for-st-file-uploader-decoding/4465
st.set_option("deprecation.showfileUploaderEncoding", False)

# defines an h1 header
st.title("Style transfer web app")

# displays a file uploader widget
image = st.file_uploader("Choose an image")

# displays the select widget for the styles
style = st.selectbox("Choose the style", [i for i in STYLES.keys()])

# displays a button
if st.button("Style Transfer"):
    if image is not None and style is not None:
        files = {"file": image.getvalue()}
        res = requests.post(f"http://model:8080/{style}", files=files)  # バックエンドのコンテナの名前
        img_path = res.json()  # jsonでapiの返り値を取る

        col1, col2 = st.beta_columns(2)

        with col1:
            st.subheader('Original')
            image = Image.open(img_path.get("original"))  # nameにはimage_pathが格納されている fastapiのget_imageの返り値
            st.image(image, use_column_width=True)

        with col2:
            st.subheader('Transferred')
            image = Image.open(img_path.get("name"))  # nameにはimage_pathが格納されている fastapiのget_imageの返り値
            st.image(image, use_column_width=True)

        displayed_styles = [style]
        displayed = 1
        total = len(STYLES)
