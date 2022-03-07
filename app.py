import streamlit as st
from BibTexTools.parser import Parser
from BibTexTools.cleaner import Cleaner
from io import StringIO

st.set_page_config(layout="wide")

st.title("📚 BibTexTools")

EXAMPLE = """@article{devlin2018bert,
  title={Bert: Pre-training of deep bidirectional transformers for language understanding},
  author={Devlin, and Chang, Ming-Wei and Lee, Kenton and Toutanova, Kristina},
  year={2018}
}"""


@st.cache
def clean(input, keep_keys, keep_unknown):
    """Clean a BibTex bibliography"""
    # parse
    parser_obj = Parser()
    bib = parser_obj.parse(input)

    # process
    cleaner_obj = Cleaner(keep_keys=keep_keys, keep_unknown=keep_unknown)
    processed_bib = cleaner_obj.clean(bib)

    return processed_bib.to_bibtex()
    # # write
    # bibtex_str = processed_bib.to_bibtex()
    # output.write(bibtex_str)


col1, col2 = st.columns(2)
with col1:
    st.markdown("### Input:")

    option = st.selectbox("Input Options:", ("File", "Text"))
    user_input = ""
    if option == "Text":
        user_input = st.text_area("Paste Data", EXAMPLE)
    elif option == "File":
        uploaded_file = st.file_uploader("Choose bib file", accept_multiple_files=False)
        if uploaded_file is not None:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            user_input = stringio.read()
    with st.form("my_form"):

        keep_keys = st.checkbox("Keep original keys")
        keep_unknown = st.checkbox("Keep enties that can not be cleaned")

        submitted = st.form_submit_button("Clean")

with col2:
    st.markdown("### Output:")
    output_option = st.selectbox("Output Options:", ("File", "Text"))
    if submitted:
        if user_input == "":
            st.error("Pleas choose a file or past bibtex information first.")
        else:
            with st.spinner("Cleaning publications. This may take a while..."):
                processed_bib = clean(user_input, keep_keys, keep_unknown)

            if output_option == "Text":
                st.code(processed_bib, language="latex")
            elif output_option == "File":
                st.download_button(
                    label="Download data as CSV",
                    data=processed_bib,
                    file_name="cleaned_bib.bib",
                )
