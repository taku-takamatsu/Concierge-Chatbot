import YelpApi
import os
from dotenv import load_dotenv
import pandas
import boto3
from time import time
from decimal import Decimal
import json
load_dotenv()

def insert_to_db(data):
    dynamodb = boto3.resource('dynamodb')
    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    # on the table resource are accessed or its load() method is called.
    table = dynamodb.Table('coms4111_hw1_yelp_restaurants')

    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.
    print(table.creation_date_time)
    #batch insert 
    with table.batch_writer(overwrite_by_pkeys=['business_id', 'created_at']) as batch:
        # Float types must be converted to decimal
        for row in json.loads(json.dumps(data['businesses']), parse_float=Decimal):
            row['business_id'] = row['id']
            row['created_at'] = Decimal(time())
            batch.put_item(
                Item=row
            )

def get_data(category):
    client_id = os.environ['YELP_API_CLIENT_ID']
    api_key = os.environ['YELP_API_KEY']
    api = YelpApi.YelpApi(client_id, api_key)
    return api.get_business_search({
            "term": "restaurants",
            "location": "New York City",
            "limit": 10,
            "offset": 0,
            "category": category
        }, count=10)

if __name__ == '__main__':
    categories = [
        'afghani',
        'african',
        'newamerican',
        'tradamerican',
        'arabian',
        'asianfusion',
        'australian',
        'baguettes',
        'bangladeshi',
        'bbq',
        'beerhall',
        'belgian',
        'bistros',
        'brazilian',
        'british',
        'breakfast_brunch',
        'cajun',
        'cambodian',
        'newcanadian',
        'caribbean',
        'chilean',
        'chinese',
        'comfortfood',
        'cuban',
        'diners',
        'filipino',
        'fishnchips',
        'food_court',
        'foodstands',
        'french',
        'german',
        'greek',
        'halal',
        'hawaiian',
        'himalayan',
        'hkcafe',
        'hotdog',
        'indonesian',
        'irish',
        'italian',
        'japanese',
        'jewish',
        'kebab',
        'korean',
        'kosher',
        'malaysian',
        'mediterranean',
        'mexican',
        'mideastern',
        'moroccan',
        'pakistani',
        'peruvian',
        'persian',
        'pizza',
        'portugese',
        'russian',
        'seafood',
        'singaporean',
        'spanish',
        'taiwanese',
        'thai',
        'tapas',
        'turkish',
        'ukrainian',
        'vegan',
        'vegetarian',
        'vietnamese',
        'ukrainian'
    ]

    result = get_data(",".join(categories[:5]))
    insert_to_db(result)