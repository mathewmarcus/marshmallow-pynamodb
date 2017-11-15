from marshmallow import fields
from marshmallow.exceptions import ValidationError


class PynamoNested(fields.Nested):
    def _serialize(self, nested_obj, attr, obj):
        if not isinstance(nested_obj, dict):
            nested_obj = nested_obj.attribute_values
        return super(PynamoNested, self)._serialize(nested_obj, attr, obj)


class PynamoSet(fields.List):
    def __init__(self, cls_or_instance, **kwargs):
        self.strict_unique = kwargs.pop('strict_unique', True)
        super(PynamoSet, self).__init__(cls_or_instance, **kwargs)

    def _deserialize(self, value, attr, data):
        if self.strict_unique:
            unfiltered_value = super(PynamoSet, self)._deserialize(value, attr, data)
            duplicates = dict()
            unique_list = set()

            for element in unfiltered_value:
                if element in unique_list:
                    duplicates[element] = ['Duplicate element'] 
                else:
                    unique_list.add(element)

            if duplicates:
                raise ValidationError(duplicates)
        else:
            unique_list = set(super(PynamoSet, self)._deserialize(value, attr, data))
        
        return unique_list

    def _serialize(self, value, attr, obj):
        return super(PynamoSet, self)._serialize(value, attr, obj)


class NumberSet(PynamoSet):
    def __init__(self, **kwargs):
        super(NumberSet, self).__init__(fields.Number, **kwargs)


class UnicodeSet(PynamoSet):
    def __init__(self, **kwargs):
        super(UnicodeSet, self).__init__(fields.String, **kwargs)
