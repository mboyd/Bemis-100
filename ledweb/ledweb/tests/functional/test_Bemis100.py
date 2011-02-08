from ledweb.tests import *

class TestBemis100Controller(TestController):

    def test_index(self):
        response = self.app.get(url(controller='Bemis100', action='index'))
        # Test response...
