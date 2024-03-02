# pubmed

Code to scrape biomedical paper abstracts added to the [PubMed search engine](https://pubmed.ncbi.nlm.nih.gov/) in the last month.


## Requirements

- python >= 3.9


## Usage

To scrape the data and unzip the downloaded files, run the following:

    python download.py
    python unpack.py

This will populate the `data` directory with xml files. 
To parse the abstracts from the data, run the following:

    python parse.py

This will populate directories of the form `processed/abstracts{year}' containing abstracts published in year {year}.
