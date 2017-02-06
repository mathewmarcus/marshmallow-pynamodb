from marshmallow import Schema, SchemaOpts, post_load
from marshmallow.schema import SchemaMeta
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, Attribute
from marshmallow_pynamo.convert import converter

from six import with_metaclass


class ModelOpts(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        self.model = getattr(meta, 'model', None)


class ModelMeta(SchemaMeta):
    # __metaclass__ = SchemaMeta

    # def __new__(mcs, name, bases, attrs):
    #     model = getattr(attrs.get('Meta', object), 'model', None)
    #     if model:
    #         attributes = {name: attr for name, attr in vars(model).iteritems() if isinstance(attr, Attribute)}
    #         fields = dict()
    #         for attr_name, attribute in attributes.iteritems():
    #             field = converter.attribute2field(attribute)
    #             if attribute.is_hash_key or attribute.is_range_key or not attribute.null:
    #                 field.required = True
    #
    #             fields[attr_name] = field
    #
    #         attrs['boo'] = 1
    #         attrs.update(fields)
    #     return SchemaMeta.__new__(mcs, name, bases, attrs)

    @classmethod
    def get_declared_fields(mcs, klass, cls_fields, inherited_fields, dict_cls):
        declared_fields = super(ModelMeta, mcs).get_declared_fields(klass, cls_fields, inherited_fields, dict_cls)
        if klass.opts.model:
            attributes = {name: attr for name, attr in vars(klass.opts.model).iteritems() if
                          isinstance(attr, Attribute)}
            fields = dict()
            for attr_name, attribute in attributes.iteritems():
                field = converter.attribute2field(attribute)
                if attribute.is_hash_key or attribute.is_range_key or not attribute.null:
                    field.required = True

                fields[attr_name] = field

            declared_fields.update(fields)
        return declared_fields


class ModelSchema(with_metaclass(SchemaMeta, Schema)):
    OPTIONS_CLASS = ModelOpts

    @post_load
    def hydrate_pynamo_model(self, data, sync=False):
        x = self.opts.model
        y = x("Marcus")
        return self.opts.model("Marcus")
