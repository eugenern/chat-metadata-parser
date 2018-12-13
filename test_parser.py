"""
Integration tests for the parser's functionalities
"""

#!/usr/bin/env python3

# -------
# imports
# -------

import unittest
import chat_parser

# ----------
# Test Cases
# ----------

class TestParser(unittest.TestCase):
    """Tests the parser's overall functionality"""

    def test_single_mention(self):
        """Give the parse function a message with 1 mention."""

        message = '@john hey, you around?'
        result = '{\n "mentions": [\n  "john"\n ],\n "words": 3\n}'
        self.assertEqual(chat_parser.parse(message), result)

    def test_multiple_emoticons(self):
        """Give the parse function a message with 2 emoticons."""

        message = 'Good morning! (smile) (coffee)'
        result = '{\n "emoticons": [\n  "smile",\n  "coffee"\n ],\n "words": 2\n}'
        self.assertEqual(chat_parser.parse(message), result)

    def test_emoticons_and_links(self):
        """Give the parse function a message with emoticons and links."""

        message = ('The World Series is starting soon! (cheer) https://www.mlb.com/ and '
                   'https://espn.com')
        result = ('{\n "emoticons": [\n  "cheer"\n ],\n "links": [\n  {\n   "url": '
                  '"https://www.mlb.com/",\n   "title": "MLB.com | The Official Site of Major '
                  'League Baseball"\n  },\n  {\n   "url": "https://espn.com",\n   "title": "ESPN: '
                  'The Worldwide Leader in Sports"\n  }\n ],\n "words": 7\n}')
        self.assertEqual(chat_parser.parse(message), result)

    def test_all_features(self):
        """Give the parse function a message with all features."""

        message = ('@mary @john (success) such a cool feature! Check this out: '
                   'https://journyx.com/features-and-benefits/data-validation-tool')
        result = ('{\n "emoticons": [\n  "success"\n ],\n "mentions": [\n  "mary",\n  "john"\n ],'
                  '\n "links": [\n  {\n   "url": "https://journyx.com/features-and-benefits/data-'
                  'validation-tool",\n   "title": "Data Validation & Corrections for Timesheets | '
                  'Journyx"\n  }\n ],\n "words": 7\n}')
        self.assertEqual(chat_parser.parse(message), result)

# ----
# main
# ----
if __name__ == '__main__':
    unittest.main()
