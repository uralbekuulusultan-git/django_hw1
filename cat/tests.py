from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .cat import Cat


class CatLogicTests(TestCase):
    def test_feed_changes_fullness_and_happiness(self):
        cat = Cat(name='Барсик')

        cat.feed()

        self.assertEqual(cat.fullness, 55)
        self.assertEqual(cat.happiness, 45)

    def test_sleeping_cat_cannot_be_fed(self):
        cat = Cat(name='Барсик', is_sleeping=True)

        cat.feed()

        self.assertEqual(cat.fullness, 40)
        self.assertEqual(cat.happiness, 40)

    def test_play_wakes_sleeping_cat_and_lowers_happiness(self):
        cat = Cat(name='Барсик', is_sleeping=True)

        cat.play()

        self.assertFalse(cat.is_sleeping)
        self.assertEqual(cat.happiness, 35)
        self.assertEqual(cat.fullness, 40)

    @patch('cat.cat.randint', return_value=2)
    def test_play_changes_stats_without_rage(self, _):
        cat = Cat(name='Барсик')

        cat.play()

        self.assertEqual(cat.happiness, 55)
        self.assertEqual(cat.fullness, 30)

    @patch('cat.cat.randint', return_value=1)
    def test_play_can_make_cat_angry(self, _):
        cat = Cat(name='Барсик')

        cat.play()

        self.assertEqual(cat.happiness, 0)
        self.assertEqual(cat.fullness, 30)

    def test_overfeeding_lowers_happiness_and_values_are_capped(self):
        cat = Cat(name='Барсик', fullness=95, happiness=90)

        cat.feed()

        self.assertEqual(cat.fullness, 100)
        self.assertEqual(cat.happiness, 65)


class CatViewTests(TestCase):
    def test_index_page_has_greeting_form(self):
        response = self.client.get(reverse('index'))

        self.assertContains(response, 'Вас приветствует симулятор кота')
        self.assertContains(response, 'Для начала введите имя кота', html=False)
        self.assertContains(response, 'введите имя кота')
        self.assertContains(response, 'Создать')

    def test_create_cat_redirects_to_info_page(self):
        response = self.client.post(reverse('index'), {'name': 'Мурка'})

        self.assertRedirects(response, reverse('cat_info'))
        self.assertEqual(self.client.session['cat']['name'], 'Мурка')

    def test_info_page_shows_initial_cat_stats(self):
        self.client.post(reverse('index'), {'name': 'Мурка'})

        response = self.client.get(reverse('cat_info'))

        self.assertContains(response, 'Мурка')
        self.assertContains(response, '1 год')
        self.assertContains(response, '40 / 100')
        self.assertContains(response, 'Покормить')

    def test_action_form_updates_cat_and_redirects_back(self):
        self.client.post(reverse('index'), {'name': 'Мурка'})

        response = self.client.post(reverse('cat_info'), {'action': 'feed'})

        self.assertRedirects(response, reverse('cat_info'))
        self.assertEqual(self.client.session['cat']['fullness'], 55)
        self.assertEqual(self.client.session['cat']['happiness'], 45)

# Create your tests here.
