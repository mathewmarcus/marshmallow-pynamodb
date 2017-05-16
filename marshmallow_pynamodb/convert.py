from marshmallow import fields

from pynamodb import attributes

PYNAMODB_TYPE_MAPPING = {
    attributes.NumberAttribute: fields.Number,
    attributes.JSONAttribute: fields.Raw,
    attributes.UnicodeAttribute: fields.String,
    attributes.BooleanAttribute: fields.Boolean,
    attributes.UTCDateTimeAttribute: fields.DateTime,
    attributes.MapAttributeMeta: {True: fields.Nested,
                                  False: fields.Dict},
    attributes.ListAttribute: {True: fields.List,
                               False: fields.Raw}
}


def attribute2field(attribute, validate_collections):
    try:
        pynamodb_type = type(attribute)
        field = PYNAMODB_TYPE_MAPPING[pynamodb_type]
    except KeyError:
        pynamodb_type = type(pynamodb_type)
        field = PYNAMODB_TYPE_MAPPING[pynamodb_type]

    if isinstance(attribute, attributes.ListAttribute) or isinstance(attribute, attributes.MapAttribute):
        return field[validate_collections]
    else:
        return field
