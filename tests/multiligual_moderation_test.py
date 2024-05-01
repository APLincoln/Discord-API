import unittest
import app.handlers.azure_moderation as am

threshold = 2

class MultiLigualTest(unittest.TestCase):
    """This class will test the 10 most spoken languages to ensure multi lingual support"""

    def test_english(self):
        phrase = "fuck you cunt"
        result = am.azure_text_moderation(phrase, threshold=threshold)
        expected_result = [{'severity': 2, 'type': 'Hate'}]
        self.assertEqual(expected_result, result)

    def test_chinese(self):
        phrase = "他媽的你個賤人"
        result = am.azure_text_moderation(phrase, threshold=threshold)
        expected_result = [{'severity': 2, 'type': 'Hate'}]
        self.assertEqual(expected_result, result)

    def test_spanish(self):
        phrase = "vete a la mierda coño"
        result = am.azure_text_moderation(phrase, threshold=threshold)
        expected_result = [{'severity': 2, 'type': 'Hate'}]
        self.assertEqual(expected_result, result)

    def test_hindi(self):
        phrase = "भाड़ में जाओ योनी"
        result = am.azure_text_moderation(phrase, threshold=threshold)
        expected_result = [{'severity': 2, 'type': 'Hate'}]
        self.assertEqual(expected_result, result)

    def test_arabic(self):
        phrase = "اللعنة عليك مهبل"
        result = am.azure_text_moderation(phrase, threshold=threshold)
        expected_result = [{'severity': 2, 'type': 'Hate'}]
        self.assertEqual(expected_result, result)

    def test_bengali(self):
        phrase = "তোমাকে চোদা চুদি"
        result = am.azure_text_moderation(phrase, threshold=threshold)
        expected_result = [{'severity': 2, 'type': 'Hate'}]
        self.assertEqual(expected_result, result)

    def test_portuguese(self):
        phrase = "foda-se sua boceta"
        result = am.azure_text_moderation(phrase, threshold=threshold)
        expected_result = [{'severity': 2, 'type': 'Hate'}]
        self.assertEqual(expected_result, result)

    def test_russian(self):
        phrase = "пошел на хуй пизда"
        result = am.azure_text_moderation(phrase, threshold=threshold)
        expected_result = [{'severity': 2, 'type': 'Hate'}]
        self.assertEqual(expected_result, result)

    def test_japanese(self):
        phrase = "ファック、クソ野郎"
        result = am.azure_text_moderation(phrase, threshold=threshold)
        expected_result = [{'severity': 2, 'type': 'Hate'}]
        self.assertEqual(expected_result, result)

    def test_urdu(self):
        phrase = "تم چوت بھاڑ میں جاؤ"
        result = am.azure_text_moderation(phrase, threshold=threshold)
        expected_result = [{'severity': 2, 'type': 'Hate'}]
        self.assertEqual(expected_result, result)
