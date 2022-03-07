📚 BibTexTools
<center><img alt="GitHub Pipenv locked Python version" src="https://img.shields.io/github/pipenv/locked/python-version/jueri/BibTexTools"></center>

**BibTexTools** is a handy tool to parse and manipulate BibTex bibliographies and references. **BibTexTools** can abbreviate author names and resolve incomplete references based on the reference title and the computer science bibliography [dblp](https://dblp.uni-trier.de/).

If you encounter any error or parsing mistake, feel free to open a new [issue](https://github.com/jueri/BibTexTools/issues/new).
<br>

## ⚙️ Installation:
**BibTexTools** can be installed using pip and this repository:
```
pip install git+https://github.com/jueri/BibTexTools.git
```

Alternatively, you can clone this repository and install it from the source.
1. Clone the repository:
` git clone https://github.com/jueri/BibTexTools.git`

2. Change working directory:
`cd BibTexTools`

3. install with:
`pip install .`

<br>

## 📖 Usage:
**BibTexTools** provides the following commands:
```
Usage: BibTexTools [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  abbreviate-authors  Abbreviate the author names of a BibTex bibliography
  clean               Clean a BibTex bibliography
```

A bibliography file as input and an output destination need to be specified for all operations.

### Abbreviate-authors:
The `abbreviate-authors` command will abbreviate all author names from a bibliography. The middle names are also included if the `-m` flag is set.
```
Usage: BibTexTools abbreviate-authors [OPTIONS] INPUT OUTPUT

  Abbreviate the author names of a BibTex bibliography

Options:
  -m, --middle_names  Include the middle names
  --help              Show this message and exit.
```

### Clean:
The `clean` command may help resolve incomplete references by retrieving high-quality references from [dblp](https://dblp.uni-trier.de/).
```
Usage: BibTexTools clean [OPTIONS] INPUT OUTPUT

  Clean a BibTex bibliography

Options:
  -k, --keep_keys     Keep original keys
  -u, --keep_unknown  Keep entries that can not be cleaned
  --help              Show this message and exit.
```
<br>

## ✨ Example:
Imagine you found an interesting paper online and saved it to your collection. Unluckily, in addition to the paper itself, you only got incomplete metadata like this:
```BibTeX
@article{devlin2018bert,
  title={Bert: Pre-training of deep bidirectional transformers for language understanding},
  author={Devlin, and Chang, Ming-Wei and Lee, Kenton and Toutanova, Kristina},
  year={2018}
}
```

**BibTexTools** will extract the title of the paper and retrieve complete BibTeX metadata from dblp, resolving the reference into:

```BibTeX
@inproceedings{DBLP:conf/naacl/DevlinCLT19,
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
```
