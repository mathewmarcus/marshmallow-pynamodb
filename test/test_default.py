from marshmallow_pynamodb import ModelSchema

from unittest import TestCase

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

from marshmallow import fields


class User(Model):

    class Meta:
        table_name = "UserModel"
    email = UnicodeAttribute(default='foo@bar.com')
    first_name = UnicodeAttribute(range_key=True)
    last_name = UnicodeAttribute(hash_key=True)


class TestDefault(TestCase):
    def test_corresponding_field_has_default(self):
        class UserSchema(ModelSchema):
            class Meta:
                model = User

        self.assertEqual(getattr(UserSchema, '_declared_fields')['email'].default, 'foo@bar.com')
