========
marshmallow-pynamodb
========

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

    author_schema.dump(user).data
    # {u'first_name': u'John', u'last_name': u'Smith', u'email': None}

    author_schema.load({"last_name": "Smith", "first_name": "John"}).data
    # user<Smith>
