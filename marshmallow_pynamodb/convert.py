from marshmallow import fields

from pynamodb import attributes

PYNAMODB_TYPE_MAPPING = {
    attributes.NumberAttribute: fields.Decimal,
    attributes.JSONAttribute: fields.Raw,
    attributes.UnicodeAttribute: fields.String,
    attributes.BooleanAttribute: fields.Boolean,
    attributes.UTCDateTimeAttribute: fields.DateTime,
    attributes.MapAttributeMeta: {True: fields.Nested,
                              False: fields.Dict},
    attributes.ListAttribute: {True: fields.List,
                               False: fields.Raw}
}

#
# def model2declared_fields(model, validate_collections=False):
#     declared_fields = dict()
#     attrs = {name: attr for name, attr in vars(model).iteritems() if
#                   isinstance(attr, attributes.Attribute)}
#     for attr_name, attribute in attrs.iteritems():
#         field = attribute2field(attribute, validate_collections)()
#
#         if isinstance(fields.Nested, field):
#             mcs.get_declared_fields(attribute, )
#
#         if attribute.is_hash_key or attribute.is_range_key or not attribute.null:
#             field.required = True
#
#         declared_fields[attr_name] = field
#

def attribute2field(attribute, validate_collections):
    try:
        pynamodb_type = type(attribute)
        field = PYNAMODB_TYPE_MAPPING[pynamodb_type]
    except KeyError as e:
        pynamodb_type = type(pynamodb_type)
        field = PYNAMODB_TYPE_MAPPING[pynamodb_type]
        x = 1

    if isinstance(attribute, attributes.ListAttribute) or isinstance(attribute, attributes.MapAttribute):
        return field[validate_collections]
    else:
        return field
