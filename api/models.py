"""
These models represent the responses that we are sending to the clients.
They are not saved into the DB, but they can be serialized by the serializers
in serializers.py.
"""

class ResponseItem:
    """
    Each individual response will have a practice and a weight
    associated to it. The practice is a data.models.practice
    instance.
    """
    def __init__(self, practice, weight):
        self.practice = practice
        self.weight = weight


class Response:
    """
    The response will contain an array of all practices and their
    weight, as well as an array of the three suggestions and their
    weight.
    """
    def __init__(self, practices, suggestions):
        self.practices = practices
        self.suggestions = suggestions
