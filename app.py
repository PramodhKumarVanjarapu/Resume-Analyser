import streamlit as st
import pandas as pd
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed

from services.parser_service import process_resume

st.title("DSA Resume Extractor")

input_text = st.text_area("Paste UID and Resume Links (tab separated)")

if st.button("Process"):
    if not input_text.strip():
        st.warning("Please provide input")
        st.stop()

    df = pd.read_csv(
        BytesIO(input_text.encode()),
        sep="\t",
        names=["UID", "resume_link"]
    )

    total = len(df)
    results = []

    progress_bar = st.progress(0)
    status_text = st.empty()
    output_placeholder = st.empty()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []

        for _, row in df.iterrows():
            futures.append(
                executor.submit(process_resume, row["UID"], row["resume_link"])
            )

        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            results.append(result)


            progress = (i + 1) / total
            progress_bar.progress(progress)
            status_text.text(f"Processed {i+1} / {total}")

            
            df_output = pd.DataFrame(results)
            output_placeholder.dataframe(df_output)


    df_output = pd.DataFrame(results)

    csv = df_output.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "output.csv",
        "text/csv"
    )