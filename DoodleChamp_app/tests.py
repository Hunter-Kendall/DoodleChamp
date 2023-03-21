import random
from django.test import TestCase
from DoodleChamp_app.models import Words
from DoodleChamp_app.words import word_list, word_dict

class WordsModelTest(TestCase):

    def test_saving_words_and_retrieving_them_randomly(self):
        for i in word_list:
            Words.objects.create(word = i, point_value = word_dict[i])
            
        lvl_1 = Words.objects.filter(point_value = 50)#132 words
        lvl_2 = Words.objects.filter(point_value = 100)#174 words
        lvl_3 = Words.objects.filter(point_value = 150)#51 words
        lvl_4 = Words.objects.filter(point_value = 200)#8 words
        #imagine the index is set ot random.randint(0, num_of_words) instead of 7
        self.assertEqual(lvl_1.values()[7], {'id': 17, 'word': 'band', 'point_value': 50})
        self.assertEqual(lvl_2.values()[7], {'id': 20, 'word': 'basket', 'point_value': 100})
        self.assertEqual(lvl_3.values()[7], {'id': 62, 'word': 'carriage', 'point_value': 150})
        self.assertEqual(lvl_4.values()[7], {'id': 355, 'word': 'wedding dress', 'point_value': 200})
        


