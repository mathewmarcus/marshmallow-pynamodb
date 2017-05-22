from marshmallow import fields


class PynamoDict(fields.Dict):
    def _serialize(self, value, attr, obj):
        if not isinstance(value, dict):
            return value.attribute_values
        else:
            return value


class PynamoNested(fields.Nested):
    def _serialize(self, nested_obj, attr, obj):
        if not isinstance(nested_obj, dict):
            nested_obj = nested_obj.attribute_values
        return super(PynamoNested, self)._serialize(nested_obj, attr, obj)

