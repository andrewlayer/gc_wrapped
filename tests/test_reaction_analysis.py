from analysis import reaction_analysis
from unittest import TestCase
from datetime import datetime
from helpers.db import Message

messages = [Message(row_id=87, text='￼Caves ', type=1, date=datetime(2024, 12, 28, 4, 52, 33, 882479), is_emote=False, embedding=None, sender_name='Armaan'), Message(row_id=109, text='CAV', type=1, date=datetime(2024, 12, 28, 8, 0, 44, 434680), is_emote=False, embedding=None, sender_name='+12162181789'), Message(row_id=216, text='￼Bulk gang ', type=1, date=datetime(2024, 12, 28, 18, 33, 42, 733786), is_emote=False, embedding=None, sender_name='+12169067123'), Message(row_id=217, text='Going on 24 years ', type=1, date=datetime(2024, 12, 28, 18, 34, 2, 449727), is_emote=False, embedding=None, sender_name='+12169067123'), Message(row_id=218, text='Loved an image', type=1, date=datetime(2024, 12, 28, 18, 34, 37, 775701), is_emote=False, embedding=None, sender_name='+12163154781'), Message(row_id=219, text='Huge ', type=1, date=datetime(2024, 12, 28, 18, 35, 9, 490506), is_emote=False, embedding=None, sender_name='+12162181789'), Message(row_id=220, text='Holy shit ', type=1, date=datetime(2024, 12, 28, 18, 35, 11, 78656), is_emote=False, embedding=None, sender_name='+12162181789'), Message(row_id=226, text='25*', type=1, date=datetime(2024, 12, 28, 18, 41, 5, 599166), is_emote=False, embedding=None, sender_name='+12166825083'), Message(row_id=227, text='looking big my boi ', type=1, date=datetime(2024, 12, 28, 18, 41, 13, 399001), is_emote=False, embedding=None, sender_name='+12166825083'), Message(row_id=229, text='what gym is that?', type=1, date=datetime(2024, 12, 28, 18, 41, 54, 882657), is_emote=False, embedding=None, sender_name='+12166825083')]

class ClientTests(TestCase):
    def test_react_frequency(self):
        result = reaction_analysis.react_frequency(messages)

        self.assertEqual(result['+12163154781']['frequency'], 1)
        self.assertEqual(result['+12163154781']['reaction_frequency']['loved'], 1)