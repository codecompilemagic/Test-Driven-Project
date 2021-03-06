from selenium import webdriver
""" Keys allow us to use input keys like ENTER, Ctrl, etc """
from selenium.webdriver.common.keys import Keys

import unittest

from django.test import LiveServerTestCase
import re

###### The comments inside '#' are used for USER STORY to build the test
###### The comments inside '"""' are used to describe the function or application usage 


""" The test Class inherits from unittest """
# class NewVisitorTest(unittest.TestCase):
class NewVisitorTest(LiveServerTestCase):
	""" setUp() and tearDown() are special methods which get run
		before and after each test.
		They are similar to try/except """

	""" Currently using setUp() to start our browser """
	def setUp(self):
		self.browser = webdriver.Chrome('C:\Users\Zigmyal\Desktop\dir\chromedriver_win32\chromedriver')
		""" implicitly_wait() tells Selenium to wait for 
			given seconds if needed.
			However, it is best for small apps. For more complex
			and larger apps, explicit wait algorithms are required """
		# self.browser.implicitly_wait(3)

	""" Currently using tearDown() to stop our browser """
	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	""" Any method whose name starts with test is a test method
		and will be run by the test runner.
		You can have more than one test_ method per class.
		Readable names for test methods are a good idea """
	def test_can_start_a_list_and_retrieve_it_later(self):
		# User visits to-do app
		# User goes to check the homepage
		# self.browser.get('http://localhost:8000')
		self.browser.get(self.live_server_url)

		# User notices the page title and header mention to-do lists
		""" Instead of --->  assert 'To-Do' in browser.title, "Browser title was " + browser.title
			we user self.assertIn to make our test assertions
			unittest provides lots of helper functions like this (assertEqual, assertTrue, assertFalse, etc) 

			self.fail just fails no matter what, producing the error message given """
		self.assertIn('To-Do', self.browser.title)
		""" find_element_by_tag_name() returns an element
			and raises an exception if it can't find it """
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		

		# User is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

		# User types "Buy apples and milk" into a text box
		inputbox.send_keys('Buy apples and milk')

		# When the user hits enter, the page updates, and now the page lists
		# "1: Buy apples and milk" as an item in a to-do list
		inputbox.send_keys(Keys.ENTER)
		""" Testing for a new url """
		user_list_url = self.browser.current_url
		# assertRegex() is a helper function from unittest
		# that checks whether a string matches a regular expression
		self.assertRegexpMatches(user_list_url, '/lists/.+')

		

		""" Using time.sleep() to pause the test during execution """
		# import time
		# time.sleep(8)

		# table = self.browser.find_element_by_id('id_list_table')
		""" find_elements_by_tag_name() returns a list, which may be empty """
		# rows = table.find_elements_by_tag_name('tr')

		""" any() Python function will return True when atleast 
			one of the elements is found/exists.
			Inside the any() function is a generator expresion
			<--- Note: Python also has a all() function ---> """
		############# modifying the function below #############	
		# self.assertTrue(
		# 	any(row.text == '1: Buy apples and milk' for row in rows),
		# 	# Error message to display if not found
		# 	'New to-do item did not appear in table -- it was: \n%s' %table.text,
		# )

		# self.assertIn('1: Buy apples and milk', [row.text for row in rows])
		self.check_for_row_in_list_table('1: Buy apples and milk')

		# There is still a text box inviting/prompting the user to add another item
		# The user enters "Make apple pie for dessert"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Make apple pie for dessert')
		inputbox.send_keys(Keys.ENTER)
		
		

		# The page updates again, and now shows both items on her list
		""" Code check """
		# table = self.browser.find_element_by_id('id_list_table')
		# rows = table.find_elements_by_tag_name('tr')
		# self.assertIn('1: Buy apples and milk', [row.text for row in rows])
		# self.assertIn('2: Make apple pie for dessert', [row.text for row in rows])

		""" Using helper method to replace the Code check """
		self.check_for_row_in_list_table('1: Buy apples and milk')
		self.check_for_row_in_list_table('2: Make apple pie for dessert')

		# self.fail('Finish the test!')

		# The user is not sure if the site will remember the list. Then the user sees
		# that the site has generated a unique URL for user -- there is some
		# explanatory text

		# The user visits the URL - and the to-do list is still there

		# Satisfied, the user goes to take a bath
		# browser.quit()



		###### Now a new user, user2, comes along to the site #######
		## We use a new browser session to make sure that no information
		## of the previous user is coming through from cookies, etc
		self.browser.quit()

		self.browser = webdriver.Chrome('C:\Users\Zigmyal\Desktop\dir\chromedriver_win32\chromedriver')

		# User2 visits the home page. There is no sing of previous users list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		
		self.assertNotIn('Buy apples and milk', page_text)
		self.assertNotIn('Make apple pie for dessert', page_text)


		# User2 starts a new list by entering a new item
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy cookies')
		inputbox.send_keys(Keys.ENTER)


		# User2 gets their own unique URL
		user2_list_url = self.browser.current_url
		self.assertRegexpMatches(user2_list_url, '/lists/.+')
		self.assertNotEqual(user2_list_url, user_list_url)


		# Again, there is no trace of previous user's lists
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy apples and milk', page_text)
		self.assertIn('Buy cookies', page_text)


# if __name__ == '__main__':
	""" unittest.main() launches the unittest test runner
		which will automatically find test classes and methods
		in the file and run them.

		warning = 'ignore' surppresses a ResourceWarning. 
		Remove it if no warning is issued after removal """
	# unittest.main(warnings='ignore')
	# unittest.main()