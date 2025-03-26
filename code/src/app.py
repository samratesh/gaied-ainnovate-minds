import streamlit as st
import os
from main import process_email

st.title("Upload EML Files")

uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        save_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        try:
            result = process_email(save_path)
            result.update({"file_name": uploaded_file.name})
            st.write(result)
        except Exception as e:
            st.json({"message": "An error occurred", "error": str(e)})