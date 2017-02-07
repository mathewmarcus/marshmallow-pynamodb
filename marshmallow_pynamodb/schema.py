from marshmallow import Schema, SchemaOpts, post_load
from marshmallow.schema import SchemaMeta
from pynamodb.attributes import Attribute
from marshmallow_pynamodb.convert import converter

from six import with_metaclass


class ModelOpts(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        self.model = getattr(meta, 'model', None)


class ModelMeta(SchemaMeta):
    @classmethod
    def get_declared_fields(mcs, klass, cls_fields, inherited_fields, dict_cls):
        declared_fields = super(ModelMeta, mcs).get_declared_fields(klass, cls_fields, inherited_fields, dict_cls)
        if klass.opts.model:
            attributes = {name: attr for name, attr in vars(klass.opts.model).iteritems() if
                          isinstance(attr, Attribute)}
            for attr_name, attribute in attributes.iteritems():
                field = converter.attribute2field(attribute)()
                if attribute.is_hash_key or attribute.is_range_key or not attribute.null:
                    field.required = True

                declared_fields[attr_name] = field
        return declared_fields


class ModelSchema(with_metaclass(ModelMeta, Schema)):
    OPTIONS_CLASS = ModelOpts

    @post_load
    def hydrate_pynamo_model(self, data, sync=False):
        return self.opts.model(**data)
