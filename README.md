# Clean BibTeX references
**Clean BibTeX** is a handy tool to resolve incomplete or misleading BibTeX references in computer science.
The CLI tool parses publication titles from a BibTeX and retrieves high-quality references from [dblp](https://dblp.uni-trier.de/).

<br>

## Installation:
**Clean BibTeX** can be installed using pip and this repository:
```
pip install git+https://github.com/jueri/clean_bibtex.git
```

Alternatively, you can clone this repository and install it from source.
1. Clone the repository:
` git clone https://github.com/jueri/clean_bibtex.git`

2. Change working directory:
`cd clean_bibtex`

3. install with:
`pip install -e .`

<br>

## Usage:
To resolve a `.bib` file, simply call `clean_bibtex` and specify an input and output file:
```
clean_bibtex [input file] [output file]
```
<br>

## Example:
Imagine you found an interesting paper online and saved it to your collection. Unluckily, in addition to the paper itself, you only got incomplete metadata like this:
```BibTeX
@article{devlin2018bert,
  title={Bert: Pre-training of deep bidirectional transformers for language understanding},
  author={Devlin, and Chang, Ming-Wei and Lee, Kenton and Toutanova, Kristina},
  year={2018}
}
```

**Clean BibTeX** will extract the name of the paper and retrieve complete BibTeX metadata from dblp, resolving the reference into:

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
