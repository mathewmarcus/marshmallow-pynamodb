from marshmallow import fields

from pynamodb import attributes

from marshmallow_pynamodb.fields import PynamoNested

PYNAMODB_TYPE_MAPPING = {
    attributes.NumberAttribute: fields.Number,
    attributes.JSONAttribute: fields.Raw,
    attributes.UnicodeAttribute: fields.String,
    attributes.BooleanAttribute: fields.Boolean,
    attributes.UTCDateTimeAttribute: fields.DateTime,
    attributes.MapAttributeMeta: PynamoNested,
    attributes.ListAttribute: fields.List,
    attributes.NullAttribute: fields.Raw
}


def attribute2field(attribute):
    try:
        pynamodb_type = type(attribute)
        field = PYNAMODB_TYPE_MAPPING[pynamodb_type]
    except KeyError:
        pynamodb_type = type(pynamodb_type)
        field = PYNAMODB_TYPE_MAPPING[pynamodb_type]

    return field
