# coding: utf-8

"""
    Actual Generation

    Generation data aggregated by sector and produced per group (in MW) on an intradaily basis for net generation injected into the network. This data is produced by RTE using remote measurement facilities with which production units are equipped, and using an estimate model for the wind-power and photovoltaic sectors. Hydraulic stocks for France are the aggregated weekly fill rates of reservoirs and lake-type hydraulic storage plants; they are expressed in MWh and sent by the generators to RTE.  # noqa: E501

    OpenAPI spec version: 1.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import generation_client
from generation_client.models.actual_generations_per_production_type import ActualGenerationsPerProductionType  # noqa: E501
from generation_client.rest import ApiException


class TestActualGenerationsPerProductionType(unittest.TestCase):
    """ActualGenerationsPerProductionType unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testActualGenerationsPerProductionType(self):
        """Test ActualGenerationsPerProductionType"""
        # FIXME: construct object with mandatory attributes with example values
        # model = generation_client.models.actual_generations_per_production_type.ActualGenerationsPerProductionType()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()