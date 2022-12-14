# coding: utf-8

"""
    Actual Generation

    Generation data aggregated by sector and produced per group (in MW) on an intradaily basis for net generation injected into the network. This data is produced by RTE using remote measurement facilities with which production units are equipped, and using an estimate model for the wind-power and photovoltaic sectors. Hydraulic stocks for France are the aggregated weekly fill rates of reservoirs and lake-type hydraulic storage plants; they are expressed in MWh and sent by the generators to RTE.  # noqa: E501

    OpenAPI spec version: 1.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from generation_client.configuration import Configuration


class ActualGenerationsPerUnitObj(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'actual_generations_per_unit': 'list[ActualGenerationsPerUnit]'
    }

    attribute_map = {
        'actual_generations_per_unit': 'actual_generations_per_unit'
    }

    def __init__(self, actual_generations_per_unit=None, _configuration=None):  # noqa: E501
        """ActualGenerationsPerUnitObj - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._actual_generations_per_unit = None
        self.discriminator = None

        if actual_generations_per_unit is not None:
            self.actual_generations_per_unit = actual_generations_per_unit

    @property
    def actual_generations_per_unit(self):
        """Gets the actual_generations_per_unit of this ActualGenerationsPerUnitObj.  # noqa: E501


        :return: The actual_generations_per_unit of this ActualGenerationsPerUnitObj.  # noqa: E501
        :rtype: list[ActualGenerationsPerUnit]
        """
        return self._actual_generations_per_unit

    @actual_generations_per_unit.setter
    def actual_generations_per_unit(self, actual_generations_per_unit):
        """Sets the actual_generations_per_unit of this ActualGenerationsPerUnitObj.


        :param actual_generations_per_unit: The actual_generations_per_unit of this ActualGenerationsPerUnitObj.  # noqa: E501
        :type: list[ActualGenerationsPerUnit]
        """

        self._actual_generations_per_unit = actual_generations_per_unit

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ActualGenerationsPerUnitObj, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ActualGenerationsPerUnitObj):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ActualGenerationsPerUnitObj):
            return True

        return self.to_dict() != other.to_dict()
