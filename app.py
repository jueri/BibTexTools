import gradio as gr
from clean_bibtex.clean_bibtex import get_url, get_dblp_bibtext, parse_bibtext_file_titles

DEFAULT_TEXT = """@inproceedings{DBLP:conf/naacl/DevlinCLT19,
  author    = {Jacob Devlin and
               Ming{-}Wei Chang and
               Kenton Lee and
               Kristina Toutanova},
  editor    = {Jill Burstein and
               Christy Doran and
               Thamar Solorio},
  title     = {{BERT:} Pre-training of Deep Bidirectional Transformers for Language
               Understanding},
  booktitle = {Proceedings of the 2019 Conference of the North American Chapter of
               the Association for Computational Linguistics: Human Language Technologies,
               {NAACL-HLT} 2019, Minneapolis, MN, USA, June 2-7, 2019, Volume 1 (Long
               and Short Papers)},
  pages     = {4171--4186},
  publisher = {Association for Computational Linguistics},
  year      = {2019},
  url       = {https://doi.org/10.18653/v1/n19-1423},
  doi       = {10.18653/v1/n19-1423},
  timestamp = {Fri, 06 Aug 2021 00:41:31 +0200},
  biburl    = {https://dblp.org/rec/conf/naacl/DevlinCLT19.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""


def parse_titles(bibtex):
    titles = []
    lines = bibtex.split(",")
    for line in lines:
        if line.strip().startswith("title"):
            title = "".join(line.split("=")[1:])
            title_clean = title.replace("{", "").replace("}", "").replace(",\n", "").strip()
            titles.append(title_clean)
    return titles


def cleaner(bibtex, file_obj):
    dblp_citations = []
    errors = []

    if file_obj:
        titles = parse_bibtext_file_titles(file_obj.name)

    elif bibtex:
        titles = parse_titles(bibtex)

    # request bibtex
    for publication in titles:
        if site_url := get_url(publication):
            if dblp_citation := get_dblp_bibtext(site_url):
                dblp_citations.append(dblp_citation)
            else:
                errors.append(" - " + publication)
        else:
            errors.append(" - " + publication)

    if dblp_citations:
        filename = "cleaned.bib"
        bibliography = "\n".join(dblp_citations)
        with open(filename, "w") as outFile:
            outFile.write(bibliography)
    else:
        filename = None
        bibliography = None
        errors.append("All")

    if errors:
        errors = "Couldnt parse files: " + "\n".join(errors)
    else:
        errors = "Success!"

    return errors, filename, bibliography


iface = gr.Interface(
    fn=cleaner,
    title="BibTeX cleaner",
    description="Clean a BibTeX file or string by dragging the incomplete or broken BibTeX file into the file box or pasting a BibTeX string into the string field. The titles are extracted, searched at the DBLP, compiled into a clean BibTeX file.",
    article="<p style='text-align: center'><a href='https://github.com/jueri/clean_bibtex'>CLI and repo</a></p>",
    inputs=[
        gr.inputs.Textbox(label="Paste a string here:", lines=1),
        # gr.inputs.Checkbox(label="Keep original keys:"),
        gr.inputs.File(label="Drag a Bibtex file here:", file_count="single", type="file", optional=True),
    ],
    outputs=[
        gr.outputs.Textbox(type="auto", label="Result Message:"),
        gr.outputs.File(label="Cleaned bibtext file:"),
        gr.outputs.Textbox(type="auto", label="Cleaned Bibliography:"),
    ],
)
iface.launch()
