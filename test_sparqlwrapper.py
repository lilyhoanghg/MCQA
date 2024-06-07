from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:7200/repositories/imkg")
sparql.setReturnFormat(JSON)

print("sparql: {}".format(sparql))

print("============= SPARQL QUERY BY LABEL =============")
# Query by label "Top Gun"
sparql_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?r ?uri ?label WHERE {FILTER (?uri!=?topic)
FILTER (!isLiteral(?uri))
?topic rdfs:label "Top Gun";
?r ?uri.
?uri rdfs:label ?label.
}
"""
print(sparql_query)

sparql.setQuery(sparql_query)

try:
    ret = sparql.queryAndConvert()

    for r in ret["results"]["bindings"]:
        print(r)
except Exception as e:
    print(e)