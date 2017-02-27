""" The TestCase imported from django.test
	is a modified version of unittest.TestCase
	and has some Django-specific features """

from django.test import TestCase

from django.core.urlresolvers import resolve
from lists.views import home_page

from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item

class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'The second list item'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first list item')
		self.assertEqual(second_saved_item.text, 'The second list item')

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

		# Check if a new Item has been saved to the database
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()		# objects.first() is the same as doing objects.all()[0]
		self.assertEqual(new_item.text, 'A new list item')	# check that the item's text is correct

		# The statement below represents Assert
		# self.assertIn('A new list item', response.content.decode())

		""" Testing if the view is passing in the correct
			value for new_item_text """
		# expected_html = render_to_string('home.html', 
		# 	{'new_item_text': 'A new list item'}, request=request)
		
		# self.assertEqual(response.content.decode(), expected_html)

		# no longer expect a response with a .content rendered by template
	# Response will represent an HTTP redirect,
	# so we should have status code 302, and points the browser
	# to a new location
	""" Good unit testing practice says
		that each test should only test one thing """
	def test_home_page_redirects_after_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/')

	def test_home_page_only_saves_items_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(), 0)