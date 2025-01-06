from analysis import reaction_analysis
from unittest import TestCase
from datetime import datetime
from helpers.db import Message
from unittest.mock import MagicMock

messages = [Message(row_id=87, text='dummy message', type=1, date=datetime(2024, 12, 28, 4, 52, 33, 882479), is_emote=False, embedding=None, sender_name='Armaan'), Message(row_id=87, text='dummy message', type=1, date=datetime(2024, 12, 28, 4, 52, 33, 882479), is_emote=False, embedding=None, sender_name='Armaan'), Message(row_id=87, text='Loved an image', type=1, date=datetime(2024, 12, 28, 4, 52, 33, 882479), is_emote=False, embedding=None, sender_name='Armaan')]

class ClientTests(TestCase):
    def test_react_frequency(self):
        result = reaction_analysis.react_frequency(messages)

        self.assertEqual(result['Armaan']['frequency'], 1)
        self.assertEqual(result['Armaan']['reaction_frequency']['loved'], 1)

    def test_react_percentage(self):
        reaction_analysis.get_message_total = MagicMock(return_value={"Armaan": 4})
        result = reaction_analysis.get_react_percentage(messages)
        self.assertEqual(result['Armaan'], 25)