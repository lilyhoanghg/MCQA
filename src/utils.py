from src.constants import *

def uri_2_short_id(uri):
    return uri.split(KB_URI)[-1]

def short_id_2_uri(short_id):
    return KB_URI + short_id

def compare_lists(list1, list2):
    # return True if list1 == list2, return False if not.
    list1.sort()
    list2.sort()

    if list1 == list2:
        return True
    else:
        return False

def format_sparql_4_output(sparql_gt):
    sparql_output = sparql_gt.replace('\n',' ').replace('\t',' ')
    return sparql_output