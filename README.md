# Download
The entire question answering dataset and knowledge graph can be downloaded [here](https://drive.google.com/drive/folders/1q9ww9iSM52V5kGaFXw3q8-6cjCDP7YMq?usp=sharing).

# Introduction
MCQA is a Movie Complex Question Answering benchmark dataset created with diverse question types, natural language questions, and SPARQL query for knowledge base question answering. The knowledge graph used is iMKG which is constructed from Wikimovies and Wikidata movie entities, following standard RDF format.

This repository is a guide to using the dataset, as instroduced in our paper: cite.

# 1. Set up iMKG movie knowledge graph
Download the knowledge graph data file iMKG.ttl included in the [download link above](https://drive.google.com/drive/folders/1q9ww9iSM52V5kGaFXw3q8-6cjCDP7YMq?usp=sharing).

Steps to set up MovieKG:
1. Download and install GraphDB

Download GraphDB from this link: https://www.ontotext.com/products/graphdb/download/

Install GraphDB on your machine.

2. Import iMKG data into GraphDB

Ensure GraphDB is stopped.

Use the following command to import data into GraphDB from command line, changing the paths in <brackets> to your local paths:

```
<graphdb-dist>/bin/importrdf load -c <path to file>/repo-config.ttl -m parallel <path to file>/iMKG.ttl
```

There are other ways to import data into GraphDB. Refer to documentation here: https://graphdb.ontotext.com/documentation/10.0/loading-data-using-importrdf.html

3. Access iMKG using SPARQLWrapper in Python

First, start GraphDB.

Install package SPARQLWrapper.

```
pip install SPARQLWrapper
```


When GraphDB is running, the iMKG data can be accessed using SPARQLWrapper in Python. 

Run test_sparqlwrapper.py to verify that everything is running smoothly.

4. [Optional] View knowledge graph visualisation on GraphDB Workbench

Once imported into GraphDB, MovieKG can be viewed as a visual graph on GraphDB Workbench mode. While GraphDB is running, enter Workbench by opening <http://localhost:7200/> on your web browser.

![Screenshot 2024-05-21 171900](https://github.com/lilyhoanghg/MCQA/assets/30521679/8e869a8a-5686-4c54-a4f4-d864432d86ce)
