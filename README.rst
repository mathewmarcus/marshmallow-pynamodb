========
marshmallow-pynamodb
========

|pypi-package|

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

.. |pypi-package| image:: https://badge.fury.io/py/marshmallow-pynamodb.svg
    :target: http://badge.fury.io/py/marshmallow-pynamodb
    :alt: Latest version

License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/mathewmarcus/marshmallow-pynamodb/blob/master/LICENSE.txt>`_ file for more details.
