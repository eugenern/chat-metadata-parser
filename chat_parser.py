"""
Given a chat message, identify its features and present them as a JSON string
"""

#!/usr/bin/env python3

# -------
# imports
# -------

from sys import stdin
import features

# ----------------
# parser functions
# ----------------

def format_json(message_features):
    """
    Display the features of a chat message in a JSON-style string.
    """
    feature_json = ',\n'.join(message_features)
    json = '\n'.join(('{', feature_json, '}'))
    return json

def parse(message):
    """
    Parse a given chat message string for features and format them
    into a JSON string.
    """
    message_features = []
    for feature in (features.Emoticons, features.Mentions, features.Links, features.Words):
        feature_string = str(feature(message))
        if feature_string:
            message_features.append(feature_string)

    output = format_json(message_features)
    return output

# ----
# main
# ----

if __name__ == '__main__':
    chat_message = stdin.readline()
    result = parse(chat_message)
    print(result)
