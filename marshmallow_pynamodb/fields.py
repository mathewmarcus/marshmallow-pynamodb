from marshmallow import fields


class PynamoDict(fields.Dict):
    def _serialize(self, value, attr, obj):
        return value.attribute_values
