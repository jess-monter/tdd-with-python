import json
from django.test import TestCase

from lists.models import List, Item


class ListAPI(TestCase):
    base_url = '/api/lists/{}/'

    def test_get_returns_json_200(self):
        list_ = List.objects.create()
        response = self.client.get(self.base_url.format(list_.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_returns_items_for_correct_list(self):
        other_list = List.objects.create()
        Item.objects.create(text='item 1', list=other_list)
        our_list = List.objects.create()
        item1 = Item.objects.create(text='item 1', list=our_list)
        item2 = Item.objects.create(text='item 2', list=our_list)
        response = self.client.get(self.base_url.format(our_list.id))
        self.assertEqual(
            json.loads(response.content.decode()),
            [
                {'id': item1.id, 'text': 'item 1'},
                {'id': item2.id, 'text': 'item 2'},
            ]
        )

    def test_POSTing_a_new_item(self):
        list_ = List.objects.create()
        response = self.client.post(
            self.base_url.format(list_.id),
            data={'text': 'new item'}
        )
        self.assertEqual(response.status_code, 201)
        new_item = list_.item_set.first()
        self.assertEqual(new_item.text, 'new item')

