#!/usr/bin/env python3

import os
import json
import singer
import requests
import requests_cache

username = os.environ["TRELLO_USERNAME"]
auth = {
    "key": os.environ["TRELLO_API_KEY"],
    "token": os.environ["TRELLO_API_TOKEN"]
}

# We've tried to follow the convention of the "official" trello tap by StitchData which uses camel case names and id format
trello_organizations_schema = {
    'properties': {
        'id': {
            'type': 'string'
        },
        'name': {
            'type': 'string'
        },
        'displayName': {
            'type': ['null', 'string']
        },
        'url': {
            'type': 'string'
        },
        'logoUrl': {
            'type': ['null', 'string']
        },
    },
}
singer.write_schema('trello_organizations', trello_organizations_schema, 'id')

# We've tried to follow the convention of the "official" trello tap by StitchData which uses camel case names and id format
trello_card_custom_fields_schema = {
    'properties': {
        'id': {
            'type': 'string'
        },
        'idCard': {
            'type': 'string'
        },
        'idBoard': {
            'type': 'string'
        },
        'idOrganization': {
            'type': 'string'
        },
        'name': {
            'type': 'string'
        },
        'value': {
            'type': ['null', 'string']
        },
    },
}
singer.write_schema('trello_card_custom_fields',
                    trello_card_custom_fields_schema, 'id')

# We've tried to follow the convention of the "official" trello tap by StitchData which uses camel case names and id format
trello_card_attachments_schema = {
    'properties': {
        'id': {
            'type': 'string'
        },
        'idCard': {
            'type': 'string'
        },
        'idBoard': {
            'type': 'string'
        },
        'idOrganization': {
            'type': 'string'
        },
        'idMember': {
            'type': ['null', 'string']
        },
        'name': {
            'type': 'string'
        },
        'bytes': {
            'type': ['null', 'integer']
        },
        'url': {
            'type': ['null', 'string']
        },
        'pos': {
            'type': 'integer'
        },
        'mimeType': {
            'type': ['null', 'string']
        },
        'isUpload': {
            'type': ['null', 'boolean']
        },
        'date': {
            "type": ["null", "string"],
            "format": "date-time"
        },
    },
}
singer.write_schema('trello_card_attachments', trello_card_attachments_schema,
                    'id')

requests_cache.install_cache(expire_after=3600)

try:
    orgs = requests.request("GET",
                            "https://api.trello.com/1/members/" + username +
                            "/organizations",
                            params=auth)
    for org in json.loads(orgs.text):
        singer.write_records('trello_organizations',
                             [{
                                 'id': org["id"],
                                 'name': org["name"],
                                 'displayName': org["displayName"],
                                 'url': org["url"],
                                 'logoUrl': org["logoUrl"]
                             }])
        boards = requests.request("GET",
                                  "https://api.trello.com/1/organizations/" +
                                  org["id"] + "/boards",
                                  params=auth)
        for board in json.loads(boards.text):
            cards = requests.request("GET",
                                     "https://api.trello.com/1/boards/" +
                                     board["id"] + "/cards",
                                     params=auth)
            for card in json.loads(cards.text):
                # Fetch attachments
                attachments = requests.request(
                    "GET",
                    "https://api.trello.com/1/cards/" + card["id"] +
                    "/attachments",
                    params=auth)
                for attachment in json.loads(attachments.text):
                    singer.write_records(
                        'trello_card_attachments',
                        [{
                            'id': attachment["id"],
                            'idCard': card["id"],
                            'idBoard': board["id"],
                            'idOrganization': org["id"],
                            'idMember': attachment["idMember"],
                            'name': attachment["name"],
                            'url': attachment["url"],
                            'mimeType': attachment["mimeType"],
                            'isUpload': attachment["isUpload"],
                            'date': attachment["date"],
                            'pos': attachment["pos"],
                            'bytes': attachment["bytes"],
                        }])

                # Fetch Custom Fields
                custom_field_items = requests.request(
                    "GET",
                    "https://api.trello.com/1/cards/" + card["id"] +
                    "/customFieldItems",
                    params=auth)
                for custom_field_item in json.loads(custom_field_items.text):
                    custom_field = requests.request(
                        "GET",
                        "https://api.trello.com/1/customField/" +
                        custom_field_item["idCustomField"],
                        params=auth)
                    field = json.loads(custom_field.text)
                    if custom_field_item.get("value") != None:
                        if custom_field_item["value"].get("text") != None:
                            singer.write_records(
                                'trello_card_custom_fields',
                                [{
                                    'id': custom_field_item["id"],
                                    'idCard': card["id"],
                                    'idBoard': board["id"],
                                    'idOrganization': org["id"],
                                    'name': field["name"],
                                    'value': custom_field_item["value"]["text"]
                                }])
                        else:
                            singer.write_records(
                                'trello_card_custom_fields',
                                [{
                                    'id': custom_field_item["idCustomField"],
                                    'idCard': card["id"],
                                    'idBoard': board["id"],
                                    'idOrganization': org["id"],
                                    'name': field["name"],
                                    'value':
                                    custom_field_item["value"]["number"]
                                }])
                    else:
                        for option in field.get("options", []):
                            if option["id"] == custom_field_item["idValue"]:
                                singer.write_records(
                                    'trello_card_custom_fields',
                                    [{
                                        'id':
                                        custom_field_item["idCustomField"],
                                        'idCard': card["id"],
                                        'idBoard': board["id"],
                                        'idOrganization': org["id"],
                                        'name': field["name"],
                                        'value': option["value"]["text"]
                                    }])
except KeyboardInterrupt:
    print("DEBUG received exit, exiting")
