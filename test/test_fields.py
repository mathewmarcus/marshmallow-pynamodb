from marshmallow import fields
from marshmallow import missing
from marshmallow.exceptions import ValidationError
from marshmallow_pynamodb.fields import PynamoSet, NumberSet, UnicodeSet
from unittest import TestCase
from mock import patch, MagicMock


class TestPynamoSet(TestCase):
    @patch('marshmallow.fields.List.__init__', return_value=None)
    def test_init(self, mock_List_init):
        pynamo_set = PynamoSet(fields.Number, required=True)

        mock_List_init.assert_called_once_with(fields.Number, required=True)
        self.assertTrue(hasattr(pynamo_set, 'strict_unique'))
        self.assertTrue(pynamo_set.strict_unique)

    @patch('marshmallow.fields.List.__init__', return_value=None)
    def test_init_strict_unique_false(self, mock_List_init):
        pynamo_set = PynamoSet(fields.String, strict_unique=False, required=True)

        mock_List_init.assert_called_once_with(fields.String, required=True)
        self.assertTrue(hasattr(pynamo_set, 'strict_unique'))
        self.assertFalse(pynamo_set.strict_unique)

    @patch('marshmallow.fields.List._deserialize', side_effect=lambda x, y, z: x)
    def test_deserialize_strict_unique_false(self, mock_List_deserialize):
        pynamo_set = PynamoSet(fields.Number, strict_unique=False, required=True)
        value = [1, 2, 3, 3, 2, 1]
        attr = 'attr'
        data = {attr: value}
        expected_deserialized_value = set(value)

        actual_deserialized_value = pynamo_set._deserialize(value, attr, data)
        
        mock_List_deserialize.assert_called_once_with(value, attr, data)
        self.assertSetEqual(expected_deserialized_value, actual_deserialized_value)

    @patch('marshmallow.fields.List._deserialize', side_effect=lambda x, y, z: x)
    def test_deserialize(self, mock_List_deserialize):
        pynamo_set = PynamoSet(fields.Number, required=True)
        value = [1, 2, 3, 3, 2, 1]
        attr = 'attr'
        data = {attr: value}
        expected_deserialized_value = set(value)

        self.assertRaises(ValidationError, pynamo_set._deserialize, value, attr, data)
        mock_List_deserialize.assert_called_once_with(value, attr, data)

    @patch('marshmallow.fields.List._serialize')
    def test_serialize(self, mock_List_serialize):
        value = {1, 2, 3}
        attr = 'attr'
        data = {attr: value}
        pynamo_set = PynamoSet(fields.Number, required=True)
        pynamo_set._serialize(value, attr, data)

        mock_List_serialize.assert_called_once_with(value, attr, data)


class TestNumberSet(TestCase):
    @patch('marshmallow_pynamodb.fields.PynamoSet.__init__')
    def test_init(self, mock_NumberSet_init):
        pynamo_set = NumberSet(required=True)

        mock_NumberSet_init.assert_called_once_with(fields.Number, required=True)


class TestUnicodeSet(TestCase):
    @patch('marshmallow_pynamodb.fields.PynamoSet.__init__')
    def test_init(self, mock_UnicodeSet_init):
        pynamo_set = UnicodeSet(required=True)

        mock_UnicodeSet_init.assert_called_once_with(fields.String, required=True)
