import boto3
from dynamodb_json import json_util as json
from boto3.dynamodb.types import TypeDeserializer
import pandas as pd
from elasticsearch import Elasticsearch, RequestsHttpConnection

import requests
from requests_aws4auth import AWS4Auth
from tabulate import tabulate
client = boto3.client('dynamodb')
deserializer = TypeDeserializer()

def get_table(table_name):
    results = []
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = client.scan(
                TableName=table_name,
                ExclusiveStartKey=last_evaluated_key
            )
        else: 
            response = client.scan(TableName=table_name)
        last_evaluated_key = response.get('LastEvaluatedKey')
        
        results.extend({k: deserializer.deserialize(v) for k,v in results.items()})
        break
        if not last_evaluated_key:
            break
    return results


def dump_table(data):
    # build file
    # The action_and_metadata portion of the bulk file
    bulk_file = ''
    for idx, index in enumerate(data):
        bulk_file += '{ "index" : { "_index" : "yelp-restaurants", "_type" : "_doc", "_id" : "' + str(idx+1) + '" } }\n'
        # The optional_document portion of the bulk file
        bulk_file += json.dumps(index) + '\n'
    print(bulk_file)
    return
    host = 'https://search-coms6998-yelp-restaurants-z7imacvtv7fs5go5sbpgucwdha.us-east-1.es.amazonaws.com' 
    region = 'us-east-1' # e.g. us-west-1

    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service)

    aos = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )

    aos.bulk(bulk_file)

    print(aos.search(q='some test query'))

# Usage
data = get_table('coms6998_hw1_yelp_restaurants')
# do something with data
df = pd.DataFrame(data)
dump_table(df[['business_id', 'categories']].to_dict(orient='records'))