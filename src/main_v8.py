import random
import time
import os

from SPARQLWrapper import SPARQLWrapper, JSON
from src.make_sparql_query_v5 import *
from src.utils import *


NUM_SAMPLES_PER_QTYPE = 2000
def make_database_from_rdf(settings, verbose=False, time_start=None, hop_number=1, qtemplates=None,
                           check_sparql_gt=True, output_full_uri=False):
    if hop_number == 1:
        qa_count = settings[key_qa_count_1_hop]
        created_path = "data/MCQA/4-3-2_mcqa_add_sparql_label/"
        save_path = "data/MCQA/4-3-2_mcqa_add_sparql_label/"
    elif hop_number == 2:
        qa_count = settings[key_qa_count_2_hop]
        created_path = "data/MCQA/4-3-2_mcqa_add_sparql_label/"
        save_path = "data/MCQA/4-3-2_mcqa_add_sparql_label/"

    ANS_LEN_THRESHOLD = settings["ANS_LEN_THRESHOLD"]

    for qtype, max_qa_count in qa_count.items():
        max_qa_count = NUM_SAMPLES_PER_QTYPE
        include_list = settings["include_list"] # include list takes precedence over exclude list.
        exclude_list = settings["exclude_list"]
        if len(include_list) > 0:
            if qtype not in include_list:
                continue
        else:
            if qtype in exclude_list:
                continue

        print("Processing {} ...".format(qtype))

        sparql_query = SPARQLWrapper('http://localhost:7200/repositories/imkg')

        sparql_query.setReturnFormat(JSON)

        qid = 0
        qa_counter = 0
        query_counter = 0
        qa_database = {}
        topic_entity_type = get_topic_ent_type_from_qtype(qtype)
        constraint_ent_type = get_constraint_type(qtype)
        qtype_no_constr = qtype.split("_constraint_")[0]

        # Get created database
        created_pairs = [] # list of [topic_entity, constraint_entity] already created.
        created_file = created_path + "{}.json".format(qtype)
        if os.path.isfile(created_file):
            with open(created_file, encoding="utf-8") as f:
                created_qa = json.load(f)
            for qid, qa in created_qa.items():
                created_pairs.append([qa[key_topic_ent_id], qa[key_constraint_id]])
            qa_database = created_qa
            qa_counter = len(created_qa)
            if qa_counter > 0:
                print("Continue processing from {}: {} / {}.".format(created_file, qa_counter, max_qa_count))
                qid = int(list(qa_database.keys())[-1]) + 1  # get last key of dictionary and plus 1.

        # Get all topic entities
        preprocess_path = "data/preprocess_wikidata/"
        preprocess_file = preprocess_path + "{}.json".format(topic_entity_type)
        with open(preprocess_file, encoding="utf-8") as f:
            all_topic_ent_dict = json.load(f)
        topic_ent_exclude_list = [] # exclude topic entities with no valid constraints.

        loop_counter = 0
        # max_qa_count = 10  # uncomment to test
        MAX_LOOP_COUNT = settings["MAX_LOOP_COUNT_PER_QTYPE"]
        while qa_counter < max_qa_count:
            loop_counter += 1
            if loop_counter == MAX_LOOP_COUNT:
                print("BREAK LOOP: {} iterations reached.".format(MAX_LOOP_COUNT))
                break

            # 1. get random topic entity
            topic_ent_short_id = random.choice(list(all_topic_ent_dict.keys()))
            topic_ent_text = all_topic_ent_dict[topic_ent_short_id]
            if verbose: print("Topic entity: {}, qtype: {}.".format(topic_ent_text, qtype))

            if topic_ent_short_id in topic_ent_exclude_list:
                if verbose: print("Topic entity in exclude list: Skip.")
                continue

            # 2. Find valid constraint entity + get answers (in parallel)
            '''
            This is the single SPARQL used for the current QA. The reason the SPARQL is at this step, instead of
            final QA step, where constraint entity is specified is:
            The results from this SPARQL is superset of SPARQL for final QA, because in this step, all possible
            constraints are included.
            If the SPARQL is given with fixed constraint entity at final step, we don't know the number of
            answer entities before constraint. Whereas, when SPARQL is executed at this step, the number of answers
            before constraint is known. And the answers with constraints can be inferred from this result.

            
            It also does not do to pick randomly both topic entity and constraint entity, because we also need to check
            the number of answer entities before constraint. 
            '''

            # 2a. SPARQL query
            # query_constr = sparql_get_constraint_entities(qtype, topic_ent_short_id)
            query_constr = sparql_get_constraint_entities_by_label(qtype, topic_ent_text)
            # print(query_constr)
            # input()

            try:
                sparql_query.setQuery(query_constr)
                ret = sparql_query.queryAndConvert()
                query_counter += 1
            except Exception as e:
                print(e)
                # print(query)
                break

            constraints_list = ret["results"]["bindings"]

            if len(constraints_list) == 0:
                topic_ent_exclude_list.append(topic_ent_short_id) # exclude topic entity from future search.
                if verbose: print("No valid constraint entity: Skip.")
                continue

            # 2b. Check number of answer entities before constraint.
            # If no of ans = 1, then it's trivial to add constraint. Move on to next topic entity.
            # This is not right, need to factor in answer per constraint entity.
            ans_before_constraint = []
            for result in constraints_list:
                ans_uri = result["answer_entity"]["value"]
                if ans_uri not in ans_before_constraint: ans_before_constraint.append(ans_uri)
            if len(ans_before_constraint) == 1:
                topic_ent_exclude_list.append(topic_ent_short_id)
                continue

            # 2c. This loop is to pick out a valid constraint entity
            # Valid constraint entity needs to be: [1-hop] different from topic entity.
            constr_ent_short_id = ''
            while constr_ent_short_id == '': # keep interating until a valid constraint entity is found
                if len(constraints_list) == 0: # or until no more possible valid constraint entity is left.
                    break
                constraint_entity = random.choice(constraints_list)
                constr_ent_text = constraint_entity['l']['value']
                constraint_entity_uri = constraint_entity['constraint_entity']['value']
                constr_ent_short_id_test = uri_2_short_id(constraint_entity_uri)
                if constr_ent_short_id_test == topic_ent_short_id:
                    constraints_list.remove(constraint_entity)
                    continue
                # # [2-hop] do not allow constraint entity = intermediate entity.
                # # [2022-10-19] UPDATE: ALLOW THIS!
                # if hop_number == 2:
                #     inter_ent_uri = constraint_entity['inter_ent']['value']
                #     inter_ent_id = uri_2_short_id(inter_ent_uri)
                #     if constr_ent_short_id_test == inter_ent_id:
                #         constraints_list.remove(constraint_entity)
                #         continue
                constr_ent_short_id = constr_ent_short_id_test


            if verbose: print("Constraint entity: {}.".format(constr_ent_text))

            current_pair = [topic_ent_short_id, constr_ent_short_id]
            if verbose: print("Current pair: {}".format(current_pair))

            if topic_ent_text == constr_ent_text:
                if verbose: print("Same topic and constraint entity: Skip.")
                continue
            if current_pair in created_pairs: # topic and constraint entities already picked.
                if verbose: print("Pair already created: Skip.")
                continue

            created_pairs.append(current_pair)

            # 3. Make final qa
            # Re-write results into list [{ans_id: , ans_txt: }, {}]
            answer_list_raw = []
            for result in constraints_list:
                tmp_constr_uri = result["constraint_entity"]['value']
                tmp_constr_id = uri_2_short_id(tmp_constr_uri)
                if tmp_constr_id == constr_ent_short_id: # this answer entity should belong in final answer.
                    tmp_ans_uri = result["answer_entity"]['value']
                    tmp_ans_id = uri_2_short_id(tmp_ans_uri)
                    tmp_ans_txt = result["answer_label"]["value"]
                    ans = {"ans_id": tmp_ans_id,
                           "ans_txt": tmp_ans_txt}
                    if ans not in answer_list_raw:
                        answer_list_raw.append(ans)



            answer_list = []
            answer_list_id = []

            if len(answer_list_raw) == 0:
                if verbose: print("No answer: Skip.")
                continue
            elif len(answer_list_raw) > ANS_LEN_THRESHOLD:
                if verbose: print("Answer longer than threshold {}: Skip.".format(ANS_LEN_THRESHOLD))
                continue

            for ans in answer_list_raw:
                ans_id = ans["ans_id"]
                ans_txt = ans["ans_txt"]
                if ans_id == topic_ent_short_id: # This scenario only happens for 2-hop, not 1-hop.
                    if verbose: print("Answer entity same as topic entity: Skip current answer entity.")
                    continue
                answer_list.append(ans_txt)
                answer_list_id.append(ans_id)

            answer_list_uri = []
            for short_id in answer_list_id:
                answer_list_uri.append(short_id_2_uri(short_id))

            if len(answer_list) == 0:
                if verbose: print("No answer: Skip.")
                continue

            # print(answer_list)
            # print("final ans len: {}".format(len(answer_list)))

            # Make question in natural language
            if qtemplates is None:
                qn_text = None
            else:
                qtemplate = random.choice(qtemplates[qtype])
                qn_text = make_question_text(qtype, qtemplate, topic_ent_text, constr_ent_text)

            # Make SPARQL ground-truth + check correctness (optional)
            # sparql_gt = make_sparql_query(qtype, topic_ent_short_id, constr_ent_short_id)
            sparql_gt = make_sparql_query_by_label(qtype, topic_ent_text, constr_ent_text)
            # sparql_gt_4_output = '''{}'''.format(sparql_gt.replace('\n', '\\n'))
            sparql_gt_4_output = '''{}'''.format(sparql_gt)
            sparql_gt_4_output = format_sparql_4_output(sparql_gt)
            # print(sparql_gt)

            if check_sparql_gt is True:
                try:
                    sparql_query.setQuery(sparql_gt)
                    ret2 = sparql_query.queryAndConvert()
                    query_counter += 1
                    if verbose: print("Querying SPARQL ground-truth ...")
                except Exception as e:
                    print(e)
                    # print(query)
                    break

                answer_list_raw_sparql = ret2["results"]["bindings"]
                answer_list_id_sparql = []
                # pp.pprint(answer_list_raw_sparql)
                for ans in answer_list_raw_sparql:
                    ans_id_check = uri_2_short_id(ans["uri"]["value"])
                    if ans_id_check != topic_ent_short_id:
                        answer_list_id_sparql.append(ans_id_check)

                # Check correct SPARQL
                if compare_lists(answer_list_id_sparql, answer_list_id) is False: # incorrect SPARQL, do not add QA.
                    print("Current pair: {}".format(current_pair))
                    print("Constraint query: {}".format(query_constr))
                    pp.pprint("constraint query result: {}".format(constraints_list))
                    print("Incorrect SPARQL ground-truth : {}".format(sparql_gt))
                    print("SPARQL result: {}".format(answer_list_id_sparql))
                    print("GT result: {}".format(answer_list_id))
                    continue
                if verbose: print("SPARQL ground-truth check passed.")

            if output_full_uri is True:
                qa_database[qid] = {
                    key_question: qn_text,
                    key_q_type: qtype,
                    key_topic_entity: topic_ent_text,
                    key_topic_ent_uri: short_id_2_uri(topic_ent_short_id),
                    key_constraint: constr_ent_text,
                    key_constraint_uri: short_id_2_uri(constr_ent_short_id),
                    key_answer: answer_list,
                    key_answer_uri: answer_list_uri,
                    key_sparql_gt: sparql_gt_4_output
                }
            else:
                qa_database[qid] = {
                    key_question: qn_text,
                    key_q_type: qtype,
                    key_topic_entity: topic_ent_text,
                    key_topic_ent_id: topic_ent_short_id,
                    key_constraint: constr_ent_text,
                    key_constraint_id: constr_ent_short_id,
                    key_answer: answer_list,
                    key_answer_id: answer_list_id,
                    key_sparql_gt: sparql_gt_4_output
                }

            if verbose: pp.pprint(qa_database[qid])
            qid += 1
            qa_counter += 1

            if (qa_counter % 500) == 0:
                print("... {}/{}".format(qa_counter, max_qa_count))


        # Save each qtype qa database to file
        print("... {}/{}".format(qa_counter, max_qa_count))
        save_json_to_file(qa_database, "{}{}.json".format(save_path, qtype), ensure_ascii=False)
        if time_start is not None:
            time_now = time.perf_counter()
            time_elapsed = time_now - time_start
            print("Time elapsed: {:0f}".format(time_elapsed))
    return None


if __name__ == '__main__':
    time_start = time.perf_counter()

    # -----------------------------
    # Import settings file
    # -----------------------------
    settings_file_path = 'data/settings_v5.json'
    # settings_file_path = 'src/lilyhg/MetaQA_2/generate_qa_using_rdf_kb/settings_test.json'
    with open(settings_file_path) as f:
        settings = json.load(f)

    qtemplates_file = "data/all_selected_qn_templates.json"
    with open(qtemplates_file, encoding="utf-8") as f:
        qtemplates = json.load(f)


    # -----------------------------
    # Make QA database
    # -----------------------------
    make_database_from_rdf(settings, verbose=False, time_start=time_start, hop_number=2, qtemplates=qtemplates,
                           check_sparql_gt=True)


    # -----------------------------
    # time
    # -----------------------------
    time_stop = time.perf_counter()
    runtime = time_stop - time_start
    print("Runtime: {:0f}".format(runtime))

