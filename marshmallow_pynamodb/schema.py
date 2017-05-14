from marshmallow import Schema, SchemaOpts, post_load, fields
from marshmallow.schema import SchemaMeta
from marshmallow_pynamodb.convert import attribute2field
from pynamodb.attributes import Attribute
from six import with_metaclass


class ModelOpts(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        self.model = getattr(meta, 'model', None)
        self.validate = getattr(meta, 'validate', False)


class ModelMeta(SchemaMeta):
    @classmethod
    def get_declared_fields(mcs, klass, cls_fields, inherited_fields, dict_cls):
        declared_fields = super(ModelMeta, mcs).get_declared_fields(klass, cls_fields, inherited_fields, dict_cls)
        if klass.opts.model:
            attributes = {name: attr for name, attr in vars(klass.opts.model).iteritems() if
                          isinstance(attr, Attribute)}
            for attr_name, attribute in attributes.iteritems():
                field = attribute2field(attribute, klass.opts.validate)

                if field == fields.Nested:
                    instance_of = type(attribute)

                    class Meta:
                        model = instance_of
                        validate = True
                    sub_model = type(instance_of.__name__, (klass, ), {'Meta': Meta})
                    field = field(sub_model)
                elif field == fields.List:
                    class Meta:
                        model = attribute.element_type
                        validate = True
                    element_type = type(attribute.element_type.__name__, (klass, ), {'Meta': Meta})
                    field = field(fields.Nested(element_type))
                else:
                    field = field()

                if attribute.is_hash_key or attribute.is_range_key or not attribute.null:
                    field.required = True
                    if attribute.is_hash_key:
                        field.description = 'hash key'
                    elif attribute.is_range_key:
                        field.description = 'range key'

                field_name = attribute.attr_name if attribute.attr_name else attr_name
                declared_fields[field_name] = field
        return declared_fields


class ModelSchema(with_metaclass(ModelMeta, Schema)):
    OPTIONS_CLASS = ModelOpts

    @post_load(pass_original=True)
    def hydrate_pynamo_model(self, data, orig_data):
        hash_key, range_key = self._get_hash_and_range_key(orig_data)
        return self.opts.model(hash_key=hash_key, range_key=range_key, **orig_data)

    def _get_hash_and_range_key(self, data):
        hash_key = None
        range_key = None

        for field_name, field_value in self.declared_fields.iteritems():
            if hash_key and range_key:
                break
            elif getattr(field_value, 'description', None) == 'hash key':
                hash_key = data.get(field_name)
                del data[field_name]
            elif getattr(field_value, 'description', None) == 'range key':
                range_key = data.get(field_name)
                del data[field_name]

        return hash_key, range_key
