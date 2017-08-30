from marshmallow import Schema, SchemaOpts, post_load, fields
from marshmallow.schema import SchemaMeta
from marshmallow_pynamodb.convert import attribute2field
from marshmallow_pynamodb.fields import PynamoNested
from pynamodb.attributes import Attribute
from six import with_metaclass, iteritems


class ModelOpts(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        self.model = getattr(meta, 'model', None)


class ModelMeta(SchemaMeta):
    @classmethod
    def get_declared_fields(mcs, klass, cls_fields, inherited_fields, dict_cls):
        declared_fields = super(ModelMeta, mcs).get_declared_fields(klass, cls_fields, inherited_fields, dict_cls)
        if klass.opts.model:
            attributes = {name: attr for name, attr in iteritems(vars(klass.opts.model)) if
                          isinstance(attr, Attribute)}
            klass.opts.model.attributes = dict()
            for attr_name, attribute in iteritems(attributes):
                if declared_fields.get(attr_name):
                    continue

                field = attribute2field(attribute)

                if field == PynamoNested:
                    instance_of = type(attribute)

                    class Meta:
                        model = instance_of
                    sub_model = type(instance_of.__name__, (ModelSchema, ), {'Meta': Meta})
                    field = field(sub_model)
                elif field == fields.List:
                    class Meta:
                        model = attribute.element_type
                    element_type = type(attribute.element_type.__name__, (ModelSchema, ), {'Meta': Meta})
                    field = field(PynamoNested(element_type))
                else:
                    field = field()

                field_name = attribute.attr_name if attribute.attr_name else attr_name
                if attribute.is_hash_key or attribute.is_range_key or not attribute.null:
                    field.required = True
                    if attribute.is_hash_key:
                        klass.opts.hash_key = field_name
                    elif attribute.is_range_key:
                        klass.opts.range_key = field_name

                field.default = attribute.default
                declared_fields[field_name] = field
        return declared_fields


class ModelSchema(with_metaclass(ModelMeta, Schema)):
    OPTIONS_CLASS = ModelOpts

    @post_load
    def hydrate_pynamo_model(self, data):
        hash_key = data.pop(getattr(self.opts, 'hash_key', None), None)
        range_key = data.pop(getattr(self.opts, 'range_key', None), None)
        return self.opts.model(hash_key=hash_key, range_key=range_key, **data)
