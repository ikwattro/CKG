import os
import sys
import ckg_utils
from graphdb_connector import connector

def read_knowledge_queries(dataset_type='proteomics'):
    queries_dir = os.path.abspath(os.path.dirname(__file__))
    query_file = dataset_type+"_knowledge_cypher.yml"
    queries_file_path = os.path.join(queries_dir, "../report_manager/queries/"+query_file)
    queries = read_queries(queries_file_path)
    
    return queries

def read_queries(queries_file):
    queries = ckg_utils.get_queries(queries_file)

    return queries

def list_queries(queries):
    for q in queries:
        print("Name: {}\nDescription: {}\nInvolves nodes: {}\nInvolves relationships: {}\n Query: {}".format(
            queries[q]['name'], queries[q]['description'], ",".join(queries[q]['involved_nodes']), ",".join(queries[q]['involved_rels']), queries[q]['query']))


def find_queries_involving_nodes(queries, nodes, print_pretty=False):
    valid_queries = {}
    for q in queries:
        if len(set(queries[q]['involved_nodes']).intersection(nodes)) == len(nodes):
            valid_queries[q] = queries[q]
    if print_pretty:
        for q in valid_queries:
            query = valid_queries[q]
            print("Query id:", q)
            print("Query Name: ", query["name"])
            print("Description: ", query["description"])
            print("Involves nodes:", ",".join(query['involved_nodes']))
            print("Involves relationships:", ",".join(query['involved_rels']))
            print("Query:\n", query["query"])
            if "example" in query:
                print("How to use it:\n", "\n".join(query["example"]), "\n")
            
    return valid_queries


def find_queries_involving_relationships(queries, rels):
    valid_queries = []
    for q in queries:
        if len(set(queries[q]['involved_rels']).intersection(rels)) > 0:
            valid_queries.append(queries[q])

    return valid_queries


def get_query(queries, query_id):
    query = None
    if query_id in queries:
        if "query" in queries[query_id]:
            query = queries[query_id]["query"]
    return query


def get_description(query):
    return query['description']


def get_nodes(query):
    return query['involved_nodes']


def get_relationships(query):
    return query['involved_rels']


def map_node_name_to_id(driver, node, value):
    query_name = 'map_node_name'
    cwd = os.path.abspath(os.path.dirname(__file__))
    queries_path = "project_cypher.yml"
    cypher = read_queries(os.path.join(cwd, queries_path))
    query = cypher[query_name]['query'].replace('NODE', node)
    identifier = connector.getCursorData(driver, query, parameters={
                                         'name': str(value)}).values[0][0]
    return identifier