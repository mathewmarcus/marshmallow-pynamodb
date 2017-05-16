from marshmallow_pynamodb.schema import ModelSchema

from pynamodb.attributes import ListAttribute, MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.models import Model

from unittest import TestCase


class Location(MapAttribute):
    lat = NumberAttribute(attr_name='latitude')
    lng = NumberAttribute(attr_name='longitude')
    name = UnicodeAttribute()


class Person(MapAttribute):
    fname = UnicodeAttribute(attr_name='firstName')
    lname = UnicodeAttribute(attr_name='lastName')
    age = NumberAttribute()


class OfficeEmployeeMap(MapAttribute):
    office_employee_id = NumberAttribute()
    person = Person()
    office_location = Location()


class Office(Model):
    class Meta:
        table_name = 'OfficeModel'
        host = "http://localhost:8000"

    office_id = NumberAttribute(hash_key=True)
    address = Location()
    employees = ListAttribute(of=OfficeEmployeeMap)


class OfficeSchema(ModelSchema):
    class Meta:
        model = Office
        validate = True


hash_key = 789
attrs = {'address': {'latitude': 6.98454,
                     'longitude': 172.38832,
                     'name': 'some_location'},
         'employees': [{'office_employee_id': 123,
                        'person': {'firstName': 'John',
                                   'lastName': 'Smith',
                                   'age': 45},
                        'office_location': {'latitude': -24.0853,
                                            'longitude': 144.87660,
                                            'name': 'other_location'}},
                       {'office_employee_id': 456,
                        'person': {'firstName': 'Jane',
                                   'lastName': 'Doe',
                                   'age': 33},
                        'office_location': {'latitude': -20.57989,
                                            'longitude': 92.30463,
                                            'name': 'yal'}}]}


class TestValidatedModelSchema(TestCase):
    def setUp(self):
        if not Office.exists():
            Office.create_table(read_capacity_units=1, write_capacity_units=1)

    def test_load(self):
        expected_model = Office(hash_key=hash_key, **attrs)
        attrs['office_id'] = hash_key

        data, errors = OfficeSchema().load(attrs)

        self.assertTrue(getattr(OfficeSchema, '_declared_fields')['office_id'].required)
        self.assertDictEqual(errors, {})
        self.assertDictEqual(data.attribute_values, expected_model.attribute_values)

    def test_dump(self):
        model = Office(hash_key=hash_key, **attrs)
        attrs['office_id'] = hash_key

        data, errors = OfficeSchema().dump(model)

        self.assertDictEqual(errors, {})
        self.assertDictEqual(data, attrs)
