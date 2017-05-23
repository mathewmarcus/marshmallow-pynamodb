====================
marshmallow-pynamodb
====================
.. image:: https://badge.fury.io/py/marshmallow-pynamodb.svg
    :target: http://badge.fury.io/py/marshmallow-pynamodb
    :alt: Latest version
.. image:: https://travis-ci.org/mathewmarcus/marshmallow-pynamodb.svg?branch=master
    :target: https://travis-ci.org/mathewmarcus/marshmallow-pynamodb
    :alt: Travis-CI

`PynamoDB <https://pynamodb.readthedocs.io/en/latest/>`_ integration with the  `marshmallow <https://marshmallow.readthedocs.io/en/latest/>`_ (de)serialization library.

Installation
============
From PyPi::

    $ pip install marshmallow-pynamodb

From GitHub::

    $ pip install git+https://github.com/mathewmarcus/marshmallow-pynamodb#egg=marshmallow_pynamodb

Declare your models
===================

.. code-block:: python

    from pynamodb.models import Model
    from pynamodb.attributes import UnicodeAttribute

    class User(Model):
        class Meta:
            table_name = "user"
        email = UnicodeAttribute(null=True)
        first_name = UnicodeAttribute(range_key=True)
        last_name = UnicodeAttribute(hash_key=True)

Generate marshmallow schemas
============================

.. code-block:: python

    from marshmallow_pynamodb import ModelSchema

    class UserSchema(ModelSchema):
        class Meta:
            model = User

    user_schema = UserSchema()


(De)serialize your data
=======================

.. code-block:: python

    user = User(last_name="Smith", first_name="John")

    user_schema.dump(user).data
    # {u'first_name': u'John', u'last_name': u'Smith', u'email': None}

    user_schema.load({"last_name": "Smith", "first_name": "John"}).data
    # user<Smith>


Nested models? No problem
=========================

.. code-block:: python

    from marshmallow_pynamodb.schema import ModelSchema

    from pynamodb.models import Model
    from pynamodb.attributes import ListAttribute, MapAttribute, NumberAttribute, UnicodeAttribute

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

        office_id = NumberAttribute(hash_key=True)
        address = Location()
        employees = ListAttribute(of=OfficeEmployeeMap)


    class OfficeSchema(ModelSchema):
        class Meta:
            model = Office


    OfficeSchema().load({'office_id': 789,
                         'address': {'latitude': 6.98454,
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
                                                            'name': 'yal'}}]}).data
    # Office<789>


License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/mathewmarcus/marshmallow-pynamodb/blob/master/LICENSE.txt>`_ file for more details.
