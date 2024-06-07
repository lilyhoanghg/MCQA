KB_URI = "https://www.wikidata.org/entity/"

PREFIXES_FULL = f'''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <{KB_URI}>
PREFIX wd: <https://www.wikidata.org/entity/>
'''


PREFIXES = f'''PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
'''

type_to_rdf_class = {
"actor"	    :	"actor",
"director"	:	"director",
"writer"	:	"writer",
"tag"	    :	"tag",
"tags"	    :	"tag",
"year"	    :	"year",
"language"	:	"language",
"genre"	    :	"genre",
"imdb_vote"	:	"IMDb Votes",
"imdbvotes"	:	"IMDb Votes",
"imdb_rating"	:	"IMDb Rating",
"movie"     :   "film",
 "imdbrating": "IMDb Rating"
}

rel_starred_actors = 'starred_actors'
rel_release_year = "release_year"
rel_directed_by = "directed_by"
rel_written_by = "written_by"
rel_has_tags = "has_tags"
rel_in_language = "in_language"
rel_has_imdb_votes = "has_imdb_votes"
rel_has_imdb_rating = "has_imdb_rating"
rel_has_genre = "has_genre"
rel_movie_name = "movie_name"

key_question = "question"
key_q_type = "question_type"
key_answer = "answer"
key_answer_text = key_answer + "_text"
key_answer_id = key_answer + "_id"
key_movie_name = "movie_name"
key_actor = "[actor]"
key_director = "[director]"
key_writer = "[writer]"
key_tag = "[tag]"
key_year = "[year]"
key_language = "[language]"
key_imdb_votes = "[imdb_votes]"
key_imdb_rating = "[imdb_rating]"
key_genre = "[genre]"
key_movie = "movie"
key_topic_entity = "topic_entity"
key_topic_ent_text = key_topic_entity + "_text"
key_topic_ent_id = key_topic_entity + "_id"
key_constraint = "constraint"
key_constraint_txt = key_constraint + "_text"
key_constraint_id = key_constraint + "_id"
key_qa_wo_constraint = "qa without constraint"
key_sparql_gt = "sparql"
key_topic_ent_uri = key_topic_entity + "_uri"
key_constraint_uri = key_constraint + "_uri"
key_answer_uri = key_answer + "_uri"
key_answer_corrected = key_answer + "_corrected"
key_answer_id_corrected = key_answer_id + "_corrected"
key_answer_metaqa1_uncorrected = key_answer + "_metaqa1_uncorrected"

q_type_actor_to_movie_constr_year = "actor_to_movie_constraint_year"

key_templates = "templates"

key_index_to_info = "index_to_info"
key_movie_to_index = "movie_to_index"
key_type_to_rel = "type_to_rel"
key_to_index = "_to_index"
key_rel_to_type = "rel_to_type"

key_intermediate_entity = "intermediate entity"
key_ans_before_constraint = "answer before constraint"

type_actor = "actor"
type_director = "director"
type_writer = "writer"
type_tag = "tag"
type_year = "year"
type_language = "language"
type_imdb_vote = "imdb_vote"
type_imdb_rating = "imdb_rating"
type_genre = "genre"
type_movie = "movie"

key_qid = "qid"
key_q_identifier = "q_identifier"

key_x_to_movie = "x_to_movie"
key_movie_to_y = "movie_to_y"

CONSTRAINTS_ALL = ["movie", "actor", "director", "writer", "tag", "year", "language", "genre", "imdb_vote", "imdb_rating"]

type_answer_movie = "movie"
type_answer_non_movie = "non-movie"
type_answer_any = "any"
type_answer_both = "both"