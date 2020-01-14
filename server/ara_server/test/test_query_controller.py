# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from ara_server.models.message import Message  # noqa: E501
from ara_server.test import BaseTestCase

test_query = \
{
  "message": {
    "knowledge_graph": {
      "edges": [
        {
          "id": "553903",
          "source_id": "https://omim.org/entry/603903",
          "target_id": "https://www.uniprot.org/uniprot/P00738",
          "type": "affects"
        },
        {
          "id": "553903",
          "source_id": "https://omim.org/entry/603903",
          "target_id": "https://www.uniprot.org/uniprot/P00738",
          "type": "affects"
        }
      ],
      "nodes": [
        {
          "id": "OMIM:603903",
          "name": "Haptoglobin",
          "type": [
            "disease",
            "disease"
          ]
        },
        {
          "id": "OMIM:603903",
          "name": "Haptoglobin",
          "type": [
            "disease",
            "disease"
          ]
        }
      ]
    },
    "query_graph": {
      "edges": [
        {
          "id": "e00",
          "source_id": "https://omim.org/entry/603903",
          "target_id": "https://www.uniprot.org/uniprot/P00738",
          "type": [
            "affects",
            "affects"
          ]
        },
        {
          "id": "e00",
          "source_id": "https://omim.org/entry/603903",
          "target_id": "https://www.uniprot.org/uniprot/P00738",
          "type": [
            "affects",
            "affects"
          ]
        }
      ],
      "nodes": [
        {
          "curie": [
            "OMIM:603903"
          ],
          "id": "n00",
          "type": [
            "disease",
            "disease"
          ]
        },
        {
          "curie": [
            "OMIM:603903"
          ],
          "id": "n00",
          "type": [
            "disease",
            "disease"
          ]
        }
      ]
    },
    "results": [
      {
        "edge_bindings": [
          {
            "kg_id": [
              "kg_id",
              "kg_id"
            ],
            "qg_id": "qg_id"
          },
          {
            "kg_id": [
              "kg_id",
              "kg_id"
            ],
            "qg_id": "qg_id"
          }
        ],
        "node_bindings": [
          {
            "kg_id": [
              "kg_id",
              "kg_id"
            ],
            "qg_id": "qg_id"
          },
          {
            "kg_id": [
              "kg_id",
              "kg_id"
            ],
            "qg_id": "qg_id"
          }
        ]
      },
      {
        "edge_bindings": [
          {
            "kg_id": [
              "kg_id",
              "kg_id"
            ],
            "qg_id": "qg_id"
          },
          {
            "kg_id": [
              "kg_id",
              "kg_id"
            ],
            "qg_id": "qg_id"
          }
        ],
        "node_bindings": [
          {
            "kg_id": [
              "kg_id",
              "kg_id"
            ],
            "qg_id": "qg_id"
          },
          {
            "kg_id": [
              "kg_id",
              "kg_id"
            ],
            "qg_id": "qg_id"
          }
        ]
      }
    ]
  },
  "additionalProp1": {}
}


class TestQueryController(BaseTestCase):
    """QueryController integration test stubs"""

    def test_query(self):
        """Test case for query

        Query reasoner via one of several inputs
        """
        request_body = test_query
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/query',
            method='POST',
            headers=headers,
            data=json.dumps(request_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
