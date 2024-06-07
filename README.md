# Download
The entire question answering dataset and knowledge graph can be downloaded [here](https://drive.google.com/drive/folders/1q9ww9iSM52V5kGaFXw3q8-6cjCDP7YMq?usp=sharing).

# Introduction
MCQA is a Movie Complex Question Answering benchmark dataset created with diverse question types, natural language questions, and SPARQL query for knowledge base question answering. The knowledge graph used is iMKG which is constructed from Wikimovies and Wikidata movie entities, following standard RDF format.

This repository is a guide to using the dataset, as instroduced in our paper: Lily Hoang, Fiona Liausvia, Liu Yan, and Thanh-Son Nguyen, *Semi-Automated Construction of Complex Knowledge Base Question Answering Dataset using Large Language Model*, ECML PKDD 2024.

Source code for MCQA dataset construction using an automated KG sampling approach is also shared in this repository.

# Set up iMKG movie knowledge graph
Download the knowledge graph data file iMKG.ttl included in the [download link above](https://drive.google.com/drive/folders/1q9ww9iSM52V5kGaFXw3q8-6cjCDP7YMq?usp=sharing).

Steps to set up MovieKG:
1. Download and install GraphDB

Download GraphDB from this link: https://www.ontotext.com/products/graphdb/download/

Install GraphDB on your machine.

2. Import iMKG data into GraphDB

Ensure GraphDB is stopped.

Download the provided repo-config.ttl to your machine.

Use the following command to import data into GraphDB from command line, changing the paths in \<brackets\> to your local paths:

```
<graphdb-dist>/bin/importrdf load -c <path to file>/repo-config.ttl -m parallel <path to file>/iMKG.ttl
```

Refer to documentation [here](https://graphdb.ontotext.com/documentation/10.0/loading-data-using-importrdf.html).

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

# MCQA benchmark dataset
MCQA contains a total of 157,764 question-asnwer pairs, including 4,135 different question templates, and 83 question types. A sample from the MCQA validation set is presented here.
```
"qid": "mcqa-91c22325-e67e-11ee-adc7-58961d663d9c",
"question": "Can you help me remember who starred in both [Edge of Tomorrow] and [Rain Man]?",
"question_type": "movie_to_actor_constraint_movie",
"topic_entity": ["Edge of Tomorrow", "Rain Man"],
"topic_entity_id": [
      "https://www.wikidata.org/entity/Q1187607",
"answer": ["Tom Cruise"],
"answer_id": ["https://www.wikidata.org/entity/Q37079"],
"sparql": "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT DISTINCT ?label ?uri
      WHERE { ?e1 ?rel ?uri; rdfs:label \"Edge of Tomorrow\" .
      ?e3 ?rel ?uri; rdfs:label \"Rain Man\" .
      ?rel rdfs:label \"starred_actors\" .
      ?uri rdfs:label ?label . }"
```
The wikidata entity ids are functional URLs that lead to the webpage containing information about the entity. Note that backslashes in the SPARQL have to be removed before querying on the knowledge graph. That is ```\"Edge of Tomorrow\"``` should become ```"Edge of Tomorrow"```.

Selected examples of question types found in the dataset are as follows. Refer to the paper for a full list of 83 question types.
|     Question     Category           |     Question Type                       |     Example                                                                                      |
|-------------------------------------|-----------------------------------------|--------------------------------------------------------------------------------------------------|
|     comparative                     |     compare_directors_num_movies        |     Which director has helmed a greater number of films,   [director] or [director]?             |
|     count                           |     actor_year_num_movies               |     Find out the total number of movies featuring [actor] in   [year].                           |
|     count                           |     movie_num_actors                    |     What's the total actor count for the film [movie]?                                           |
|     difference                      |     director_movie_not_actor            |     Tell me which movies were directed by [director] without   [actor] in the cast.              |
|     intersection    |     director_year_movie                 |     Could you inform me about the actors in films directed by   [Director] during [Year]?        |
|     intersection    |     writer_director_movie               |     I'm interested in finding out the films written by [Writer]   and directed by [Director].    |
|     multi-hop, constraint                       |     movie_to_actor_constraint_movie     |     Can you help me remember who starred in both [movie] and [movie]?                            |
|     superlative                     |     movie_release_first                 |     I'm curious, did [movie] debut before [movie]?                                               |
|     yes/no                          |     yesno_actor_genre                   |     Has [actor] appeared in any movies of the [genre] genre?                                     |
|     yes/no                          |     yesno_movie_same_director_writer    |     Was [Movie] penned and helmed by the same creative mind?                                     |
