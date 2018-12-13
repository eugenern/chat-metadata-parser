"""
A collection of types of features that a chat message may contain and
the formats in which they should be described by the parser
"""

#!/usr/bin/env python3

# -------
# imports
# -------

import re
from urllib.request import urlopen
from html.parser import HTMLParser

# -----------------
# class definitions
# -----------------

class Feature:
    """A description of the concept of a feature in a chat message"""

    def __init__(self, message):
        pass

    def __str__(self):
        pass

class Mentions(Feature):
    """A mention is a string used to tag another user"""

    def __init__(self, message):
        super().__init__(message)
        self.tags = re.findall(r'(?<!\S)@(\w+)', message)

    def __str__(self):
        if not self.tags:
            return ''
        tags_string = ',\n'.join('  "{0}"'.format(tag) for tag in self.tags)
        json_string = '\n'.join((' "mentions": [', tags_string, ' ]'))
        return json_string

class Links(Feature):
    """A link is a URL to a website"""

    def __init__(self, message):
        super().__init__(message)
        self.urls = re.findall(r'\bhttp\S+', message)
        self.titles = get_titles(self.urls)

    def __str__(self):
        if not self.urls:
            return ''
        urls_strings = ['   "url": "{0}"'.format(url) for url in self.urls]
        titles_strings = ['   "title": "{0}"'.format(title) for title in self.titles]
        bracketed_links_strings = []
        for link in zip(urls_strings, titles_strings):
            link_string = ',\n'.join(link)
            bracketed_link_string = '\n'.join(('  {', link_string, '  }'))
            bracketed_links_strings.append(bracketed_link_string)
        links_string = ',\n'.join(bracketed_links_strings)
        json_string = '\n'.join((' "links": [', links_string, ' ]'))
        return json_string

class Emoticons(Feature):
    """An emoticon is text representation of a visual image"""

    def __init__(self, message):
        super().__init__(message)
        self.emoticons = re.findall(r'(?<!\S)\((\w{1,15})\)(?!\S)', message)

    def __str__(self):
        if not self.emoticons:
            return ''
        emoticons_string = ',\n'.join('  "{0}"'.format(emoticon) for emoticon in self.emoticons)
        json_string = '\n'.join((' "emoticons": [', emoticons_string, ' ]'))
        return json_string

class Words(Feature):
    """A count of non-feature words in the message"""

    def __init__(self, message):
        super().__init__(message)
        m_count = len(Mentions(message).tags)
        l_count = len(Links(message).urls)
        e_count = len(Emoticons(message).emoticons)
        self.w_count = len(message.split()) - (m_count + l_count + e_count)

    def __str__(self):
        json_string = ' "words": ' + str(self.w_count)
        return json_string

# ----------------
# helper functions
# ----------------

def get_titles(urls):
    """Given a list of urls, get a list of the corresponding titles"""

    titles = []
    for url in urls:
        with urlopen(url) as response:
            encoding = response.info().get_content_charset(failobj="utf-8")
            html = response.read().decode(encoding)
            title_parser = TitleParser()
            title_parser.feed(html)
            titles.append(title_parser.title.strip())
    return titles

# --------------
# helper classes
# --------------

class TitleParser(HTMLParser):
    """A helper class used to parse HTML for a title"""

    def __init__(self):
        super().__init__()
        self.title = ''
        self.tag_is_title = False

    def handle_starttag(self, tag, attrs):
        if not self.title and tag == 'title':
            self.tag_is_title = True

    def handle_endtag(self, tag):
        if self.tag_is_title and tag == 'title':
            self.tag_is_title = False

    def handle_data(self, data):
        if self.tag_is_title:
            self.title = data
