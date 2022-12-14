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


class ValueActualGenerationsPerUnit(object):
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
        'updated_date': 'datetime',
        'production_type': 'str',
        'value': 'int'
    }

    attribute_map = {
        'start_date': 'start_date',
        'end_date': 'end_date',
        'updated_date': 'updated_date',
        'production_type': 'production_type',
        'value': 'value'
    }

    def __init__(self, start_date=None, end_date=None, updated_date=None, production_type=None, value=None, _configuration=None):  # noqa: E501
        """ValueActualGenerationsPerUnit - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._start_date = None
        self._end_date = None
        self._updated_date = None
        self._production_type = None
        self._value = None
        self.discriminator = None

        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        if updated_date is not None:
            self.updated_date = updated_date
        if production_type is not None:
            self.production_type = production_type
        if value is not None:
            self.value = value

    @property
    def start_date(self):
        """Gets the start_date of this ValueActualGenerationsPerUnit.  # noqa: E501

        Start time interval (YYYY-MM-DDThh:mm:sszzzzzz)  # noqa: E501

        :return: The start_date of this ValueActualGenerationsPerUnit.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this ValueActualGenerationsPerUnit.

        Start time interval (YYYY-MM-DDThh:mm:sszzzzzz)  # noqa: E501

        :param start_date: The start_date of this ValueActualGenerationsPerUnit.  # noqa: E501
        :type: datetime
        """

        self._start_date = start_date

    @property
    def end_date(self):
        """Gets the end_date of this ValueActualGenerationsPerUnit.  # noqa: E501

        End time interval (YYYY-MM-DDThh:mm:sszzzzzz)  # noqa: E501

        :return: The end_date of this ValueActualGenerationsPerUnit.  # noqa: E501
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this ValueActualGenerationsPerUnit.

        End time interval (YYYY-MM-DDThh:mm:sszzzzzz)  # noqa: E501

        :param end_date: The end_date of this ValueActualGenerationsPerUnit.  # noqa: E501
        :type: datetime
        """

        self._end_date = end_date

    @property
    def updated_date(self):
        """Gets the updated_date of this ValueActualGenerationsPerUnit.  # noqa: E501

        Data update date (YYYY-MM-DDThh:mm:sszzzzzz)  # noqa: E501

        :return: The updated_date of this ValueActualGenerationsPerUnit.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_date

    @updated_date.setter
    def updated_date(self, updated_date):
        """Sets the updated_date of this ValueActualGenerationsPerUnit.

        Data update date (YYYY-MM-DDThh:mm:sszzzzzz)  # noqa: E501

        :param updated_date: The updated_date of this ValueActualGenerationsPerUnit.  # noqa: E501
        :type: datetime
        """

        self._updated_date = updated_date

    @property
    def production_type(self):
        """Gets the production_type of this ValueActualGenerationsPerUnit.  # noqa: E501

        Generating sector  # noqa: E501

        :return: The production_type of this ValueActualGenerationsPerUnit.  # noqa: E501
        :rtype: str
        """
        return self._production_type

    @production_type.setter
    def production_type(self, production_type):
        """Sets the production_type of this ValueActualGenerationsPerUnit.

        Generating sector  # noqa: E501

        :param production_type: The production_type of this ValueActualGenerationsPerUnit.  # noqa: E501
        :type: str
        """
        allowed_values = ["BIOMASS", "FOSSIL_BROWN_COAL_LIGNITE", "FOSSIL_COAL_DERIVED_GAS", "FOSSIL_GAS", "FOSSIL_HARD_COAL", "FOSSIL_OIL", "FOSSIL_OIL_SHALE", "FOSSIL_PEAT", "GEOTHERMAL", "HYDRO_PUMPED_STORAGE", "HYDRO_RUN_OF_RIVER_AND_POUNDAGE", "HYDRO_WATER_RESERVOIR", "MARINE", "NUCLEAR", "OTHER_RENEWABLE", "SOLAR", "WASTE", "WIND_OFFSHORE", "WIND_ONSHORE", "OTHER"]  # noqa: E501
        if (self._configuration.client_side_validation and
                production_type not in allowed_values):
            raise ValueError(
                "Invalid value for `production_type` ({0}), must be one of {1}"  # noqa: E501
                .format(production_type, allowed_values)
            )

        self._production_type = production_type

    @property
    def value(self):
        """Gets the value of this ValueActualGenerationsPerUnit.  # noqa: E501

        Data value  # noqa: E501

        :return: The value of this ValueActualGenerationsPerUnit.  # noqa: E501
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this ValueActualGenerationsPerUnit.

        Data value  # noqa: E501

        :param value: The value of this ValueActualGenerationsPerUnit.  # noqa: E501
        :type: int
        """

        self._value = value

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
        if issubclass(ValueActualGenerationsPerUnit, dict):
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
        if not isinstance(other, ValueActualGenerationsPerUnit):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ValueActualGenerationsPerUnit):
            return True

        return self.to_dict() != other.to_dict()
