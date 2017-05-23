from marshmallow_pynamodb import ModelSchema

from pynamodb.attributes import ListAttribute, MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.models import Model

from unittest import TestCase

from os import environ


class Location(MapAttribute):
    latitude = NumberAttribute()
    longitude = NumberAttribute()
    name = UnicodeAttribute()


class Person(MapAttribute):
    firstName = UnicodeAttribute()
    lastName = UnicodeAttribute()
    age = NumberAttribute()


class OfficeEmployeeMap(MapAttribute):
    office_employee_id = NumberAttribute()
    person = Person()
    office_location = Location()


class Office(Model):
    class Meta:
        table_name = 'OfficeModel'
        host = "http://localhost:{}".format(environ['DOCKER_PORT'])

    office_id = NumberAttribute(hash_key=True)
    address = Location()
    employees = ListAttribute(of=OfficeEmployeeMap)


class OfficeSchema(ModelSchema):
    class Meta:
        model = Office


class TestValidatedModelSchema(TestCase):
    def setUp(self):
        if not Office.exists():
            Office.create_table(read_capacity_units=1, write_capacity_units=1)

        self.hash_key = 789
        self.attrs = {'address': {'latitude': 6.98454,
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

    def test_load(self):
        self.attrs['office_id'] = self.hash_key

        data, errors = OfficeSchema().load(self.attrs)

        self.assertTrue(getattr(OfficeSchema, '_declared_fields')['office_id'].required)
        self.assertDictEqual(errors, {})

        self.assertIsInstance(data, Office)
        self.assertEqual(data.attribute_values['office_id'], self.hash_key)
        self.assertIsInstance(data.attribute_values['address'], Location)
        self.assertIsInstance(data.attribute_values['employees'], list)
        self.assertIsInstance(data.attribute_values['employees'][0], OfficeEmployeeMap)
        self.assertIsInstance(data.attribute_values['employees'][0]['person'], Person)
        self.assertIsInstance(data.attribute_values['employees'][0]['office_location'], Location)

    def test_load_fails_dict_level_0(self):
        self.attrs['office_id'] = 'foobar'

        data, errors = OfficeSchema().load(self.attrs)

        self.assertDictEqual(errors, {'office_id': [u'Not a valid number.']})

    def test_load_fails_dict_level_gt_0(self):
        self.attrs['office_id'] = self.hash_key
        self.attrs['employees'][0]['office_location']['latitude'] = 'foobar'

        data, errors = OfficeSchema().load(self.attrs)

        self.assertDictEqual(errors, {'employees': {0: {'office_location': {'latitude': [u'Not a valid number.']}}}})

    def test_dump(self):
        model = Office(hash_key=self.hash_key, **self.attrs)
        self.attrs['office_id'] = self.hash_key

        data, errors = OfficeSchema().dump(model)

        self.assertDictEqual(errors, {})
        self.assertDictEqual(data, self.attrs)

    def test_save_and_get_dict(self):
        self.attrs['office_id'] = self.hash_key

        office = OfficeSchema().load(self.attrs).data
        office.save()

        office_model = Office.get(789)
        office_json = OfficeSchema().dump(office_model).data

        self.assertDictEqual(office_json, self.attrs)

    def test_objs_serialization(self):
        self.maxDiff = None

        self.attrs['office_id'] = self.hash_key

        john = Person(
            firstName='John',
            lastName='Smith',
            age=45,
        )
        jane = Person(
            firstName='Jane',
            lastName='Doe',
            age=33,
        )
        loc = Location(
            latitude=6.98454,
            longitude=172.38832,
            name='some_location'
        )
        loc1 = Location(
            latitude=-24.0853,
            longitude=144.87660,
            name='other_location'
        )
        loc2 = Location(
            latitude=-20.57989,
            longitude=92.30463,
            name='yal'
        )
        emp1 = OfficeEmployeeMap(
            office_employee_id=123,
            person=john,
            office_location=loc1
        )
        emp2 = OfficeEmployeeMap(
            office_employee_id=456,
            person=jane,
            office_location=loc2
        )

        office = Office(
            office_id=self.hash_key,
            address=loc,
            employees=[emp1, emp2]
        )

        office_json = OfficeSchema().dump(office).data
        self.assertDictEqual(office_json, self.attrs)

    def tearDown(self):
        Office(hash_key=self.hash_key).delete()
