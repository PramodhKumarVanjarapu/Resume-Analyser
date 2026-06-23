import streamlit as st
import pandas as pd
from io import BytesIO
from services.parser_service import process_resume

st.set_page_config(page_title="DSA Profile Extractor")

st.title("Resume DSA Profile Extractor")

st.write("Paste CSV with UID and resume_link")

input_text = st.text_area(
    "Input CSV",
    placeholder="UID,resume_link\n1,https://example.com/resume.pdf"
)

if st.button("Process"):
    if not input_text.strip():
        st.error("Please provide input")
        st.stop()

    try:
        df = pd.read_csv(BytesIO(input_text.encode()),sep="\t",names=["UID", "resume_link"] )
    except Exception:
        st.error("Invalid CSV format")
        st.stop()

    results = []

    progress = st.progress(0)

    for i, row in df.iterrows():
        result = process_resume(row["UID"], row["resume_link"])
        results.append(result)

        progress.progress((i + 1) / len(df))

    output_df = pd.DataFrame(results)

    st.success("Done")
    st.dataframe(output_df)

    csv = output_df.to_csv(index=False).encode()
    st.download_button(
        "Download CSV",
        csv,
        "dsa_profiles.csv",
        "text/csv"
    )