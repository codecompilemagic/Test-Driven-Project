from selenium import webdriver
import unittest

###### The comments inside '#' are used for USER STORY to build the test
###### The comments inside '"""' are used to describe the function or application usage 


""" The test Class inherits from unittest """
class NewVisitorTest(unittest.TestCase):
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
		self.browser.implicitly_wait(3)

	""" Currently using tearDown() to stop our browser """
	def tearDown(self):
		self.browser.quit()

	""" Any method whose name starts with test is a test method
		and will be run by the test runner.
		You can have more than one test_ method per class.
		Readable names for test methods are a good idea """
	def test_can_start_a_list_and_retrieve_it_later(self):
		# User visits to-do app
		# User goes to check the homepage
		self.browser.get('http://localhost:8000')

		# User notices the page title and header mention to-do lists
		""" Instead of --->  assert 'To-Do' in browser.title, "Browser title was " + browser.title
			we user self.assertIn to make our test assertions
			unittest provides lots of helper functions like this (assertEqual, assertTrue, assertFalse, etc) 

			self.fail just fails no matter what, producing the error message given """
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!')

		# User is invited to enter a to-do item straight away

		# User types "Buy apples and milk" into a text box

		# When the user hits enter, the page updates, and now the page lists
		# "1: Buy apples and milk" as an item in a to-do list

		# There is still a text box inviting/prompting the user to add another item
		# The user enters "Make apple pie for dessert"

		# The user is not sure if the site will remember the list. Then the user sees
		# that the site has generated a unique URL for user -- there is some
		# explanatory text

		# The user visits the URL - and the to-do list is still there

		# Satisfied, the user goes to take a bath
		# browser.quit()

if __name__ == '__main__':
	""" unittest.main() launches the unittest test runner
		which will automatically find test classes and methods
		in the file and run them.

		warning = 'ignore' surppresses a ResourceWarning. 
		Remove it if no warning is issued after removal """
	# unittest.main(warnings='ignore')
	unittest.main()