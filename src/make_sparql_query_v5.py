'''
Simplify SPARQL queries.
'''

from src.lilyhg.MCQA.utils import *
# from src.lilyhg.MetaQA_2.constants import *
from src.lilyhg.MCQA.generate_qa_using_rdf_kb_wikidata.constants import *

def make_sparql_query(qtype, topic_entity_id, constraint_entity_id):
    no_of_hop = get_no_of_hop(qtype)
    answer_type = get_answer_type(qtype)
    topic_ent_type = get_topic_ent_type_from_qtype(qtype)
    topic_ent_type_rdf = type_to_rdf_class[topic_ent_type]
    answer_type_rdf = type_to_rdf_class[answer_type]
    constraint_type = get_constraint_type(qtype)
    constraint_type_rdf = type_to_rdf_class[constraint_type]
    pred_constr = get_pred_constr(ent_type=answer_type, constr_type=constraint_type)
    if no_of_hop == 1:
        pred1 = get_pred_type_between_two_entities(ent1_type=topic_ent_type, ent2_type=answer_type)
        if topic_ent_type != type_movie:
            sparql_query = sparql_ent_to_movie_constraint_x(topic_entity_id, answer_type_rdf,
                                                            constraint_entity_id, pred1, pred_constr)
        else: # topic_ent_type == type_movie
            sparql_query = sparql_movie_to_ent_constraint_movie(topic_entity_id, answer_type_rdf,
                                                            constraint_entity_id, pred1, pred_constr)
    elif no_of_hop == 2:
        ent_type_hop2 = get_ent_type_by_hop_no(qtype, hop_number=2)
        ent_type_hop2_rdf = type_to_rdf_class[ent_type_hop2]
        pred1 = get_pred_type_between_two_entities(ent1_type=topic_ent_type, ent2_type=ent_type_hop2)
        pred2 = get_pred_type_between_two_entities(ent1_type=ent_type_hop2, ent2_type=answer_type)
        if topic_ent_type != type_movie:
            sparql_query = sparql_ent1_to_movie_to_ent2_constraint_movie(topic_entity_id, ent_type_hop2_rdf,
                                                                         answer_type_rdf,
                                                                         constraint_entity_id,
                                                                         pred1, pred2, pred_constr)
        else: # topic_ent_type == type_movie
            sparql_query = sparql_movie_to_ent_to_movie_constraint_x(topic_entity_id, ent_type_hop2_rdf,
                                                                     answer_type_rdf,
                                                                         constraint_entity_id,
                                                                         pred1, pred2, pred_constr)

    return sparql_query

def make_sparql_query_by_label(qtype, topic_entity_txt, constraint_entity_txt):
    no_of_hop = get_no_of_hop(qtype)
    answer_type = get_answer_type(qtype)
    topic_ent_type = get_topic_ent_type_from_qtype(qtype)
    topic_ent_type_rdf = type_to_rdf_class[topic_ent_type]
    answer_type_rdf = type_to_rdf_class[answer_type]
    constraint_type = get_constraint_type(qtype)
    constraint_type_rdf = type_to_rdf_class[constraint_type]
    pred_constr = get_pred_constr(ent_type=answer_type, constr_type=constraint_type)
    if no_of_hop == 1:
        pred1 = get_pred_type_between_two_entities(ent1_type=topic_ent_type, ent2_type=answer_type)
        if topic_ent_type != type_movie:
            sparql_query = sparql_ent_to_movie_constraint_x(topic_entity_txt, answer_type_rdf,
                                                            constraint_entity_txt, pred1, pred_constr)
        else: # topic_ent_type == type_movie
            sparql_query = sparql_movie_to_ent_constraint_movie(topic_entity_txt, answer_type_rdf,
                                                            constraint_entity_txt, pred1, pred_constr)
    elif no_of_hop == 2:
        ent_type_hop2 = get_ent_type_by_hop_no(qtype, hop_number=2)
        ent_type_hop2_rdf = type_to_rdf_class[ent_type_hop2]
        pred1 = get_pred_type_between_two_entities(ent1_type=topic_ent_type, ent2_type=ent_type_hop2)
        pred2 = get_pred_type_between_two_entities(ent1_type=ent_type_hop2, ent2_type=answer_type)
        if topic_ent_type != type_movie:
            sparql_query = sparql_ent1_to_movie_to_ent2_constraint_movie(topic_entity_txt, ent_type_hop2_rdf,
                                                                         answer_type_rdf,
                                                                         constraint_entity_txt,
                                                                         pred1, pred2, pred_constr)
        else: # topic_ent_type == type_movie
            sparql_query = sparql_movie_to_ent_to_movie_constraint_x(topic_entity_txt, ent_type_hop2_rdf,
                                                                     answer_type_rdf,
                                                                         constraint_entity_txt,
                                                                         pred1, pred2, pred_constr)

    return sparql_query


def sparql_movie_to_ent_to_movie_constraint_x(topic_ent_id, ent_type_hop2_rdf, answer_type, constraint_ent_id,
                                                  pred1, pred2, pred_constr):
    query = PREFIXES + '''SELECT DISTINCT ?uri ?label
	WHERE {{ 
    ?e1 ?rel1 ?intermediate_ent_1.
    
    ?uri ?rel2 ?intermediate_ent_1;
    ?rel3 ?e2;
    rdfs:label ?label.
    
    ?e1 rdfs:label "{0}".
    ?rel1 rdfs:label "{4}".
    ?rel2 rdfs:label "{5}".
    ?rel3 rdfs:label "{6}".
    ?e2 rdfs:label "{3}".
    
}}'''
    return query.format(topic_ent_id, ent_type_hop2_rdf, answer_type, constraint_ent_id,
                        pred1, pred2, pred_constr)

def sparql_ent1_to_movie_to_ent2_constraint_movie(topic_ent_id, ent_type_hop2_rdf, answer_type, constraint_ent_id,
                                     pred1, pred2, pred_constr):
    query = PREFIXES + '''SELECT DISTINCT ?uri ?label
	WHERE {{
    ?intermediate_ent_1 ?rel1 ?e1;
    ?rel2 ?uri.
    ?e2 ?rel3 ?uri.
    ?uri rdfs:label ?label.
    ?rel1 rdfs:label "{4}".
    ?e1 rdfs:label "{0}".
    ?rel2 rdfs:label "{5}".
    ?e2 rdfs:label "{3}".
    ?rel2 rdfs:label "{6}".
    
}}'''
    return query.format(topic_ent_id, ent_type_hop2_rdf, answer_type, constraint_ent_id,
                                     pred1, pred2, pred_constr)


def sparql_ent_to_movie_constraint_x(topic_ent_id, answer_type, constraint_ent_id,
                                     pred1, pred_constr):
    query = PREFIXES + '''SELECT DISTINCT ?uri ?l
	WHERE {{
    ?uri ?rel1 ?e1;
    ?rel2 ?e2;
    rdfs:label ?l.
    ?rel1 rdfs:label "{3}".
    ?e1 rdfs:label "{0}".
    ?rel2 rdfs:label "{4}".
    ?e2 rdfs:label "{2}".
}}'''
    return query.format(topic_ent_id, answer_type, constraint_ent_id,
                                     pred1, pred_constr)


def sparql_movie_to_ent_constraint_movie(topic_ent_id, answer_type, constraint_ent_id,
                                     pred1, pred_constr):
    query = PREFIXES + '''SELECT DISTINCT ?uri ?l
	WHERE {{
    ?e1 ?rel1 ?uri.
    ?e2 ?rel2 ?uri.
    ?uri rdfs:label ?l.
    ?e1 rdfs:label "{0}".
    ?rel1 rdfs:label "{3}".
    ?e2 rdfs:label "{2}".
    ?rel2 rdfs:label "{4}".
}}'''
    return query.format(topic_ent_id, answer_type, constraint_ent_id,
                        pred1, pred_constr)


def sparql_get_random_entity(entity_type, limit=None):
    entity_type_rdf = type_to_rdf_class[entity_type]
    query = PREFIXES + '''
SELECT DISTINCT ?topic_entity ?topic_ent_label
	WHERE {{ 

    ?topic_entity rdf:type ?topic_entity_type;
                  rdfs:label ?topic_ent_label.

    ?topic_entity_type rdf:type owl:Class;
                       rdfs:label "{0}"^^xsd:string.
}}
    '''
    if isinstance(limit, int):
        query += '''
        LIMIT {}
        '''.format(limit)
    return query.format(entity_type_rdf)


def get_constraints_4_movie_to_ent_constraint_movie(topic_ent, topic_ent_type, answer_type, constraint_type,
                                         pred1, pred_constr):
    query = PREFIXES + '''
SELECT DISTINCT ?constraint_entity ?l
	WHERE {{ 
    ?topic_entity ?p1 ?answer_entity.
    ?constraint_entity ?p2 ?answer_entity.

    ?topic_entity rdf:type ?topic_entity_type;
                  rdfs:label "{0}"^^xsd:string.

    ?topic_entity_type rdf:type owl:Class;
                       rdfs:label "{1}"^^xsd:string.

    ?answer_entity rdf:type ?answer_type.

    ?answer_type rdf:type owl:Class;
                 rdfs:label "{2}"^^xsd:string.

    ?constraint_entity rdf:type ?constraint_entity_type;
                  	   rdfs:label ?l.

    ?constraint_entity_type rdf:type owl:Class;
                 			rdfs:label "{3}"^^xsd:string.

    ?p1 rdfs:subPropertyOf :{4}.

    ?p2 rdfs:subPropertyOf :{5}.

}}
    '''
    return query.format(topic_ent, topic_ent_type, answer_type, constraint_type,
                        pred1, pred_constr)

def get_constraints_4_movie_to_ent_constraint_movie_by_id(topic_ent_txt, answer_type, constraint_type,
                                         pred1, pred_constr):
    query = PREFIXES + '''
SELECT DISTINCT ?constraint_entity ?l ?answer_entity ?answer_label
	WHERE {{ 
    ?e1 ?rel1 ?answer_entity.
    ?constraint_entity ?rel2 ?answer_entity.

    ?answer_entity rdfs:label ?answer_label.

    ?constraint_entity rdfs:label ?l.
    
    ?e1 rdfs:label "{0}".
    ?rel1 rdfs:label "{3}".
    ?rel2 rdfs:label "{4}".

}}
    '''
    return query.format(topic_ent_txt, answer_type, constraint_type,
                        pred1, pred_constr)

def get_constraints_4_ent_to_movie_constraint_ent(topic_ent, topic_ent_type, answer_type, constraint_type,
                                         pred1, pred_constr):
    query = PREFIXES + '''
SELECT DISTINCT ?constraint_entity ?l
	WHERE {{ 
    ?answer_entity ?p1 ?topic_entity.
    ?answer_entity ?p2 ?constraint_entity.

    ?topic_entity rdf:type ?topic_entity_type;
                  rdfs:label "{0}"^^xsd:string.

    ?topic_entity_type rdf:type owl:Class;
                       rdfs:label "{1}"^^xsd:string.

    ?answer_entity rdf:type ?answer_type.

    ?answer_type rdf:type owl:Class;
                 rdfs:label "{2}"^^xsd:string.

    ?constraint_entity rdf:type ?constraint_entity_type;
                  	   rdfs:label ?l.

    ?constraint_entity_type rdf:type owl:Class;
                 			rdfs:label "{3}"^^xsd:string.

    ?p1 rdfs:subPropertyOf :{4}.

    ?p2 rdfs:subPropertyOf :{5}.

}}
    '''
    return query.format(topic_ent, topic_ent_type, answer_type, constraint_type,
                        pred1, pred_constr)

def get_constraints_4_ent_to_movie_constraint_ent_by_id(topic_ent_txt, answer_type, constraint_type,
                                         pred1, pred_constr):
    query = PREFIXES + '''
SELECT DISTINCT ?constraint_entity ?l ?answer_entity ?answer_label
	WHERE {{ 
    ?answer_entity ?rel1 ?e1.
    ?answer_entity ?rel2 ?constraint_entity.

    ?answer_entity rdfs:label ?answer_label.

    ?constraint_entity rdfs:label ?l.
    
    ?rel1 rdfs:label "{3}".
    ?e1 rdfs:label "{0}".
    ?rel2 rdfs:label "{4}".

}}
    '''
    return query.format(topic_ent_txt, answer_type, constraint_type,
                        pred1, pred_constr)

def get_constraints_4_ent_to_movie_to_ent2_constraint_movie_by_id(topic_ent_txt, answer_type, constraint_type,
                                         pred1, pred2, pred_constr): # 2-hop
    query = PREFIXES + '''
SELECT DISTINCT ?constraint_entity ?l ?inter_ent ?answer_entity ?answer_label
	WHERE {{ 
    ?inter_ent ?p1 ?e1.
    ?inter_ent ?p2 ?answer_entity.
    ?constraint_entity ?p3 ?answer_entity.

    ?answer_entity rdfs:label ?answer_label.

    ?constraint_entity rdfs:label ?l.


    ?e1 rdfs:label "{0}".
    ?p1 rdfs:label "{3}".

    ?p2 rdfs:label "{4}".
    
    ?p3 rdfs:label "{5}".

}}
    '''
    return query.format(topic_ent_txt, answer_type, constraint_type,
                        pred1, pred2, pred_constr)

def get_constraints_4_movie_to_ent_to_movie_constraint_x_by_id(topic_ent_txt, answer_type, constraint_type,
                                         pred1, pred2, pred_constr): # 2-hop
    query = PREFIXES + '''
SELECT DISTINCT ?constraint_entity ?l ?inter_ent ?answer_entity ?answer_label
	WHERE {{ 
    ?e1 ?p1 ?inter_ent.
    ?answer_entity ?p2 ?inter_ent.
    ?answer_entity ?p3 ?constraint_entity.

    ?answer_entity rdfs:label ?answer_label.

    ?constraint_entity rdfs:label ?l.

    ?e1 rdfs:label "{0}".
    ?p1 rdfs:label "{3}".
    ?p2 rdfs:label "{4}".
    ?p3 rdfs:label "{5}".

}}
    '''
    return query.format(topic_ent_txt, answer_type, constraint_type,
                        pred1, pred2, pred_constr)

def sparql_make_query_no_constr(qtype_no_constr, topic_ent):
    no_of_hop = get_no_of_hop(qtype_no_constr)
    topic_ent_type = get_topic_ent_type_from_qtype(qtype_no_constr)
    answer_type = get_answer_type(qtype_no_constr)
    if no_of_hop == 1:
        pred1 = get_pred_type_between_two_entities(topic_ent_type, answer_type)
        if topic_ent_type == type_movie:
            query = sparql_movie_to_ent(topic_ent, pred1)
        else: # topic_ent_type != type_movie
            query = sparql_ent_to_movie(topic_ent, pred1)
    elif no_of_hop == 2:
        intermediate_ent_type = get_ent_type_by_hop_no(qtype_no_constr, hop_number=2)
        pred1 = get_pred_type_between_two_entities(topic_ent_type, intermediate_ent_type)
        pred2 = get_pred_type_between_two_entities(intermediate_ent_type, answer_type)
        if topic_ent_type == type_movie:
            query = sparql_movie_to_ent_to_movie(topic_ent, pred1, pred2)
        else:  # topic_ent_type != type_movie
            query = sparql_ent_to_movie_to_ent2(topic_ent, pred1, pred2)
    return query

def sparql_movie_to_ent_to_movie(topic_entity, pred1, pred2): # 2-hop
    query = PREFIXES + '''

    SELECT ?answer_ent
    	WHERE {{ ?movie rdfs:label "{0}"^^xsd:string;
    	                :{1} ?entity.
    	                
    	        ?answer_ent :{2} ?entity.
    }}
        '''
    return query.format(topic_entity, pred1, pred2)

def sparql_ent_to_movie_to_ent2(topic_entity, pred1, pred2): # 2-hop
    query = PREFIXES + '''
    SELECT ?answer_ent
    	WHERE {{ ?entity rdfs:label "{0}"^^xsd:string.
    	            ?movie :{1} ?entity.
    	            ?movie :{2} ?answer_ent.
    	            
    	}}
        '''
    return query.format(topic_entity, pred1, pred2)


def sparql_movie_to_ent(topic_entity, pred1):
    query = PREFIXES + '''

    SELECT ?entity
    	WHERE {{ ?movie rdfs:label "{0}"^^xsd:string;
    	                :{1} ?entity.}}
        '''
    return query.format(topic_entity, pred1)

def sparql_ent_to_movie(topic_entity, pred1):
    query = PREFIXES + '''
    SELECT ?movie
    	WHERE {{ ?entity rdfs:label "{0}"^^xsd:string.
    	            ?movie :{1} ?entity.}}
        '''
    return query.format(topic_entity, pred1)

def sparql_get_constraint_entities(qtype, topic_ent_id):
    topic_ent_type = get_topic_ent_type_from_qtype(qtype)
    topic_ent_type_rdf = type_to_rdf_class[topic_ent_type]
    answer_type = get_answer_type(qtype)
    answer_type_rdf = type_to_rdf_class[answer_type]
    constraint_type = get_constraint_type(qtype)
    constraint_type_rdf = type_to_rdf_class[constraint_type]
    no_of_hop = get_no_of_hop(qtype)
    pred_constr = get_pred_constr(answer_type, constraint_type)
    if no_of_hop == 1:
        pred1 = get_pred_type_between_two_entities(topic_ent_type, answer_type)
        if topic_ent_type == type_movie:
            query = get_constraints_4_movie_to_ent_constraint_movie_by_id(topic_ent_id, answer_type_rdf, constraint_type_rdf,
                                                    pred1, pred_constr)
        else: # topic_ent_type != type_movie
            query = get_constraints_4_ent_to_movie_constraint_ent_by_id(topic_ent_id, answer_type_rdf, constraint_type_rdf,
                                         pred1, pred_constr)
    elif no_of_hop == 2:
        intermediate_ent_type = get_ent_type_by_hop_no(qtype, hop_number=2)
        pred1 = get_pred_type_between_two_entities(topic_ent_type, intermediate_ent_type)
        pred2 = get_pred_type_between_two_entities(intermediate_ent_type, answer_type)
        if topic_ent_type == type_movie:
            query = get_constraints_4_movie_to_ent_to_movie_constraint_x_by_id(topic_ent_id,
                                                                         answer_type_rdf, constraint_type_rdf,
                                                                        pred1, pred2, pred_constr)
        else:  # topic_ent_type != type_movie
            query = get_constraints_4_ent_to_movie_to_ent2_constraint_movie_by_id(topic_ent_id,
                                                                             answer_type_rdf, constraint_type_rdf,
                                                                             pred1, pred2, pred_constr)
    return query

def sparql_get_constraint_entities_by_label(qtype, topic_ent_txt):
    topic_ent_type = get_topic_ent_type_from_qtype(qtype)
    topic_ent_type_rdf = type_to_rdf_class[topic_ent_type]
    answer_type = get_answer_type(qtype)
    answer_type_rdf = type_to_rdf_class[answer_type]
    constraint_type = get_constraint_type(qtype)
    constraint_type_rdf = type_to_rdf_class[constraint_type]
    no_of_hop = get_no_of_hop(qtype)
    pred_constr = get_pred_constr(answer_type, constraint_type)
    if no_of_hop == 1:
        pred1 = get_pred_type_between_two_entities(topic_ent_type, answer_type)
        if topic_ent_type == type_movie:
            query = get_constraints_4_movie_to_ent_constraint_movie_by_id(topic_ent_txt, answer_type_rdf, constraint_type_rdf,
                                                    pred1, pred_constr)
        else: # topic_ent_type != type_movie
            query = get_constraints_4_ent_to_movie_constraint_ent_by_id(topic_ent_txt, answer_type_rdf, constraint_type_rdf,
                                         pred1, pred_constr)
    elif no_of_hop == 2:
        intermediate_ent_type = get_ent_type_by_hop_no(qtype, hop_number=2)
        pred1 = get_pred_type_between_two_entities(topic_ent_type, intermediate_ent_type)
        pred2 = get_pred_type_between_two_entities(intermediate_ent_type, answer_type)
        if topic_ent_type == type_movie:
            query = get_constraints_4_movie_to_ent_to_movie_constraint_x_by_id(topic_ent_txt,
                                                                         answer_type_rdf, constraint_type_rdf,
                                                                        pred1, pred2, pred_constr)
        else:  # topic_ent_type != type_movie
            query = get_constraints_4_ent_to_movie_to_ent2_constraint_movie_by_id(topic_ent_txt,
                                                                             answer_type_rdf, constraint_type_rdf,
                                                                             pred1, pred2, pred_constr)
    return query