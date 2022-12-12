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


class WaterReserves(object):
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
        'start_date': 'datetime',
        'end_date': 'datetime',
        'values': 'list[ValueWaterReserves]'
    }

    attribute_map = {
        'start_date': 'start_date',
        'end_date': 'end_date',
        'values': 'values'
    }

    def __init__(self, start_date=None, end_date=None, values=None, _configuration=None):  # noqa: E501
        """WaterReserves - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._start_date = None
        self._end_date = None
        self._values = None
        self.discriminator = None

        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        if values is not None:
            self.values = values

    @property
    def start_date(self):
        """Gets the start_date of this WaterReserves.  # noqa: E501

        Search start date (YYYY-MM-DDThh:mm:sszzzzzz)  # noqa: E501

        :return: The start_date of this WaterReserves.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this WaterReserves.

        Search start date (YYYY-MM-DDThh:mm:sszzzzzz)  # noqa: E501

        :param start_date: The start_date of this WaterReserves.  # noqa: E501
        :type: datetime
        """

        self._start_date = start_date

    @property
    def end_date(self):
        """Gets the end_date of this WaterReserves.  # noqa: E501

        Search end date (YYYY-MM-DDThh:mm:sszzzzzz)  # noqa: E501

        :return: The end_date of this WaterReserves.  # noqa: E501
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this WaterReserves.

        Search end date (YYYY-MM-DDThh:mm:sszzzzzz)  # noqa: E501

        :param end_date: The end_date of this WaterReserves.  # noqa: E501
        :type: datetime
        """

        self._end_date = end_date

    @property
    def values(self):
        """Gets the values of this WaterReserves.  # noqa: E501


        :return: The values of this WaterReserves.  # noqa: E501
        :rtype: list[ValueWaterReserves]
        """
        return self._values

    @values.setter
    def values(self, values):
        """Sets the values of this WaterReserves.


        :param values: The values of this WaterReserves.  # noqa: E501
        :type: list[ValueWaterReserves]
        """

        self._values = values

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
        if issubclass(WaterReserves, dict):
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
        if not isinstance(other, WaterReserves):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WaterReserves):
            return True

        return self.to_dict() != other.to_dict()
