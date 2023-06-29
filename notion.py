import os, logging, json
from notion_client import Client, APIErrorCode, APIResponseError
from configparser import ConfigParser
from pprint import pprint

# get config - notion token and database id 
config = ConfigParser()
config.read('config.ini')
token = config.get('notion', 'token')
databaseID = config.get('notion', 'databaseID')

# make a notion
notion = Client(
    auth = token,
    log_level = logging.DEBUG,
)

data = notion.databases.query(
    **{
        'database_id': databaseID,
        'filter': {
            'and': [
                {
                    'property': '状态',
                    'select': {'equals': '在售'}
                },
                {
                    'property': '所在分店',
                    'relation': {'contains': '78ba5732-1ca2-40ed-b3d4-83841d39c0a1'}
                },
            ]
        },
        "sorts": [
            {
                "property": "酒头",
                "direction": "ascending"
            }
        ]
    }
)
pprint(len(data['results']))
















# headers = {
#     "Authorization": "Bearer " + token,
#     "Content-Type": "application/json",
#     "Notion-Version": "2022-06-28"
# }

# data = notion.databases.query(
#     **{
#         "database_id": databaseID,
#         "filter": {
#             "property": "所在分店",
#             "relation": {
#                 "contains": "南翔店",
#             },
#         },
#     }
# )

# pprint(data)

# # read a database
# def readDatabase(databaseID, headers):
#     readUrl = f"https://api.notion.com/v1/databases/{databaseID}/query"
#     res = requests.request("POST", readUrl, headers=headers)
#     data = res.json()
#     print(res.status_code)
    
#     with open('./full-properties.json', 'w', encoding='utf8') as f:
#         json.dump(data, f, ensure_ascii=False)

#     return data

# # response a database
# def responseDatabase(databaseID, headers):
#     readUrl = f"https://api.notion.com/v1/databases/{databaseID}"
#     res = requests.request("GET",readUrl,headers=headers)
#     print(res.status_code)

# def beautiDump(data):
#     print(json.dumps(data, indent=4))

# data = readDatabase(databaseID, headers)

# # beautiDump(data.object)

# # for key, value in data.items():
# #     # beautiDump(json.dumps(value, indent=4))
# #     print(key)

# print(len(data['results']))