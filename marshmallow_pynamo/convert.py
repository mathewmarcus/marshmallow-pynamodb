from marshmallow.schema import BaseSchema
from marshmallow import fields

from pynamodb import attributes
from pynamodb.constants import ATTR_TYPE_MAP


class ModelConverter(object):

    PYNAMODB_TYPE_MAPPING = {
        attributes.MapAttribute: fields.Dict(),
        attributes.JSONAttribute: fields.Raw(),
        attributes.UnicodeAttribute: fields.String(),
        attributes.BooleanAttribute: fields.Boolean(),
        attributes.UTCDateTimeAttribute: fields.DateTime(),
        attributes.ListAttribute: fields.Raw()
    }

    @property
    def type_mapping(self):
        return self.PYNAMODB_TYPE_MAPPING
        # return BaseSchema.TYPE_MAPPING

    def attribute2field(self, attribute):
        return self.type_mapping[type(attribute)]
        # return BaseSchema.TYPE_MAPPING[ATTR_TYPE_MAP[attribute.attr_type]]


converter = ModelConverter()

