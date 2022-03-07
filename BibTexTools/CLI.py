import click
from BibTexTools.parser import Parser
from BibTexTools.cleaner import Cleaner


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--keep_keys", "-k", is_flag=True, help="Keep original keys")
@click.option(
    "--keep_unknown", "-u", is_flag=True, help="Keep enties that can not be cleaned"
)
@click.argument("output", type=click.File("w"))
def clean(input, keep_keys, keep_unknown, output):
    """Clean a BibTex bibliography"""
    # parse
    parser_obj = Parser()
    bib = parser_obj.from_file(input)

    # process
    click.echo(
        "Requesting citation metadata for {num_publications} publications, this may take a while..."
    )
    cleaner_obj = Cleaner(keep_keys=keep_keys, keep_unknown=keep_unknown)
    processed_bib = cleaner_obj.clean(bib)

    # write
    bibtex_str = processed_bib.to_bibtex()
    output.write(bibtex_str)


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--middle_names", "-m", is_flag=True, help="Include the middle names")
@click.argument("output", type=click.File("w"))
def abbreviate_authors(input, middle_names, output):
    """Abbreviate the author names of a BibTex bibliography"""
    # parse
    parser_obj = Parser()
    bib = parser_obj.from_file(input)

    # process
    processed_bib = bib.abbreviate_names(middle_names)

    # write
    bibtex_str = processed_bib.to_bibtex()
    output.write(bibtex_str)


cli.add_command(clean)
cli.add_command(abbreviate_authors)
