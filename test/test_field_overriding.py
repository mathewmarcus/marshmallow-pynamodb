from marshmallow_pynamodb import ModelSchema

from unittest import TestCase

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

from marshmallow import fields


class User(Model):

    class Meta:
        table_name = "UserModel"
    email = UnicodeAttribute(null=True)
    first_name = UnicodeAttribute(range_key=True)
    last_name = UnicodeAttribute(hash_key=True)


class TestFieldOverriding(TestCase):
    def test_no_override(self):
        class UserSchema(ModelSchema):
            class Meta:
                model = User

        self.assertFalse(getattr(UserSchema, '_declared_fields')['email'].required)
        self.assertFalse(getattr(UserSchema, '_declared_fields')['email'].allow_none)

    def test_override(self):
        class UserSchema(ModelSchema):
            email = fields.String(required=True, allow_none=True)

            class Meta:
                model = User

        self.assertTrue(getattr(UserSchema, '_declared_fields')['email'].required)
        self.assertTrue(getattr(UserSchema, '_declared_fields')['email'].allow_none)
