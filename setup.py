from setuptools import setup, find_packages  # type: ignore

setup(
    name="BibTexTools",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    # install_requires=["Click", "requests"],
    # entry_points={
    #     "console_scripts": [
    #         "BibTexTools = BibTexTools.clean_bibtex:clean_bibtex",
    #     ],
    # },
)
