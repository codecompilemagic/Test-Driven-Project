""" The TestCase imported from django.test
	is a modified version of unittest.TestCase
	and has some Django-specific features """

from django.test import TestCase

from django.core.urlresolvers import resolve
from lists.views import home_page

from django.http import HttpRequest
from django.template.loader import render_to_string

# Create your tests here.
class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		""" resolve() is the function Django uses internally to
			resolve URLs and find what view function it should map to.
			'/' represents the root of the site. """
		found = resolve('/')
		self.assertEqual(found.func, home_page)


	def test_home_page_returns_correct_html(self):
		""" Creating a HttpRequest object, which Django sees
			when a user's browser asks for a page """
		request = HttpRequest()

		""" Passing the home_page() view to response.
			It is an instance of HttpResponse class """
		response = home_page(request)

		""" asserting .content of response has specific properties
		
			we use b'' syntax to compare because response.content 
			is RAW BYTES, not a Python string """
		# self.assertTrue(response.content.startswith(b'<html>'))

		""" render_to_string() requires a request=request argument 
			in Django 1.9+, however it will work without the request
			argument in Django 1.8 and prior 

			render_to_string manually renders a template for 
			comparison in the assertEqual() statement """
		expected_html = render_to_string('home.html', request=request)

		""" We want the <title> tag in somewhere in the middle
			with the words 'To-Do lists' in it because that's what
			we specified in our functional test. """
		
		### (1) testing bytes with bytes here ###
		# self.assertIn(b'<title>To-Do lists</title>', response.content)
		# self.assertTrue(response.content.endswith(b'</html>'))

		""" We use .decode() to convert the response.content bytes into
			a Python unicode string, which allows us to compare strings
			with strings, instead of bytes with bytes like in (1) """
		self.assertEqual(response.content.decode(), expected_html)


	def test_home_page_can_save_a_POST_request(self):
		# The 3 statements below represents Setup
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		# The single statement below represents Exercise
		""" Calling home_page(), te function under test """
		response = home_page(request)

		# The statement below represents Assert
		self.assertIn('A new list item', response.content.decode())

		""" Testing if the view is passing in the correct
			value for new_item_text """
		expected_html = render_to_string('home.html', 
			{'new_item_text': 'A new list item'}, request=request)
		
		self.assertEqual(response.content.decode(), expected_html)