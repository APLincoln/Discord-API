"""This will be used for testing the response from the moderation handler."""

import unittest
import app.handlers.azure_moderation as azure_moderation

# {'blocklistsMatch': [], 'categoriesAnalysis': [{'category': 'Hate', 'severity': 2}, {'category': 'SelfHarm', 'severity': 0}, {'category': 'Sexual', 'severity': 0}, {'category': 'Violence', 'severity': 0}]}

class TestAzureResponseHandling(unittest.TestCase):
    """This class is used for testing the response handling from CSS"""

    def test_hate(self):
        """Test for the handling hate in the response"""
        test_response = {'blocklistsMatch': [], 'categoriesAnalysis': [{'category': 'Hate', 'severity': 2}]}

        result = azure_moderation.handle_response(response = test_response, threshold = 0)

        expected_results = [{'severity': 2, 'type': 'Hate'}]

        self.assertEqual(expected_results, result)

    def test_self_harm(self):
        """Test for handling self harm in the response"""
        test_response = {'blocklistsMatch': [], 'categoriesAnalysis': [{'category': 'SelfHarm', 'severity': 2}]}

        result = azure_moderation.handle_response(response = test_response, threshold = 0)

        expected_results = [{'severity': 2, 'type': 'SelfHarm'}]

        self.assertEqual(expected_results, result)

    def test_sexual(self):
        """Test for handling sexual in the response"""
        test_response = {'blocklistsMatch': [], 'categoriesAnalysis': [{'category': 'Sexual', 'severity': 2}]}

        result = azure_moderation.handle_response(response = test_response, threshold = 0)

        expected_results = [{'severity': 2, 'type': 'Sexual'}]

        self.assertEqual(expected_results, result)

    def test_violence(self):
        """Test for handling violence in the response"""
        test_response = {'blocklistsMatch': [], 'categoriesAnalysis': [{'category': 'Violence', 'severity': 2}]}

        result = azure_moderation.handle_response(response = test_response, threshold = 0)

        expected_results = [{'severity': 2, 'type': 'Violence'}]

        self.assertEqual(expected_results, result)

    def test_all(self):
        """Test for all the cases together"""
        test_response = {'blocklistsMatch': [], 'categoriesAnalysis': [{'category': 'Hate', 'severity': 2}, {'category': 'SelfHarm', 'severity': 2}, {'category': 'Sexual', 'severity': 2}, {'category': 'Violence', 'severity': 2}]}

        result = azure_moderation.handle_response(response = test_response, threshold = 0)

        expected_results = [{'severity': 2, 'type': 'Hate'}, {'severity': 2, 'type': 'SelfHarm'}, {'severity': 2, 'type': 'Sexual'}, {'severity': 2, 'type': 'Violence'}]

        self.assertEqual(expected_results, result)

    def test_no_moderation(self):
        """Test for no moderation required"""
        test_response = {'blocklistsMatch': [], 'categoriesAnalysis': [{'category': 'Hate', 'severity': 0}, {'category': 'SelfHarm', 'severity': 0}, {'category': 'Sexual', 'severity': 0}, {'category': 'Violence', 'severity': 0}]}

        result = azure_moderation.handle_response(response = test_response, threshold = 2)

        expected_results = []

        self.assertEqual(expected_results, result)