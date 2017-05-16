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
            klass.opts.model.attributes = dict()
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

                field_name = attribute.attr_name if attribute.attr_name else attr_name
                if attribute.is_hash_key or attribute.is_range_key or not attribute.null:
                    field.required = True
                    if attribute.is_hash_key:
                        klass.opts.hash_key = field_name
                    elif attribute.is_range_key:
                        klass.opts.range_key = field_name

                declared_fields[field_name] = field
        return declared_fields


class ModelSchema(with_metaclass(ModelMeta, Schema)):
    OPTIONS_CLASS = ModelOpts

    @post_load(pass_original=True)
    def hydrate_pynamo_model(self, data, orig_data):
        hash_key = orig_data.pop(getattr(self.opts, 'hash_key', None), None)
        range_key = orig_data.pop(getattr(self.opts, 'range_key', None), None)
        return self.opts.model(hash_key=hash_key, range_key=range_key, **orig_data)
