""" The TestCase imported from django.test
	is a modified version of unittest.TestCase
	and has some Django-specific features """

from django.test import TestCase

from django.core.urlresolvers import resolve
from lists.views import home_page

from django.http import HttpRequest

# Create your tests here.
class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		""" resolve() is the function Django uses internally to
			resolve URLs and fine what view function it should map to.
			'/' represents the root of the site. """
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		""" Creating a HttpRequest object, which Django sees
			when a user's browser asks for a page """
		request = HttpRequest()

		""" Passing the home_page() view to response.
			It is an instance of a class called HttpResponse """
		response = home_page(request)

		""" asserting .content of response has specific properties
		
			we use b'' syntax to compare because response.content 
			is RAW BYTES, not a Python string """
		self.assertTrue(response.content.startswith(b'<html>'))

		""" We want the <title> tag in somewhere in the middle
			with the words 'To-Do lists' in it because that's what
			we specified in our functional test. """
		self.assertIn(b'<title>To-Do lists</title>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))