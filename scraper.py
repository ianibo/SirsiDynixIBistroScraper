# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
import scraperwiki
import lxml.html
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions

# driver = webdriver.PhantomJS('phantomjs') # or add to your PATH
driver = webdriver.PhantomJS('./phantomjs_1_9_2_linux_64') # or add to your PATH
driver.set_window_size(1024, 768) # optional

# The plan is to use this
# for i in range(ord('a'), ord('n')+1):
#    print chr(i),
# To submit a query for every letter and number then iterate the results, indexing by a hash of the identifers [to cope with dups]
# We'll do the following for each ord - in testing just the a$s  [$ is a wildcard!]
# Good selenium docs here:: http://selenium-python.readthedocs.org/en/latest/locating-elements.html

# Get the front page
driver.get('http://library.sheffield.gov.uk/uhtbin/webcat')

# Save screenshot for debug
driver.save_screenshot('screen_0001.png') # save a screenshot to disk

# Find the search field combo
searchFieldCombo = Select(driver.find_element_by_name('srchfield1'))
# Say we want to search by title
searchFieldCombo.select_by_value('TI^TITLE^SERIES^Title Processing^title')
# find the search input text control
searchInput = driver.find_element_by_name('searchdata1')
# Send the query a$ [Or the ord above]
searchInput.send_keys('a$')
# Send enter to cause the search to execute
searchInput.send_keys(Keys.ENTER)

# Wait for the search results page to finish loading
WebDriverWait(driver, 30).until(
        expected_conditions.presence_of_element_located((By.ID, "VIEW1"))
)

# Debugging
driver.save_screenshot('screen_0002.png') # save a screenshot to disk

# Now click the details button for search result 1
view_record_1_button = driver.find_element_by_name('VIEW^1')
view_record_1_button.click()
# Currently blows up here due to problem with phantomjs 1.9.0

# Wait for the details page to finish loading
#WebDriverWait(driver, 30).until(
#        expected_conditions.presence_of_element_located((By.ID, "hiddenlpsubmitdiv"))
#)


driver.save_screenshot('screen_0003.png') # save a screenshot to disk

# inputElement.send_keys('1')
# inputElement.send_keys(Keys.ENTER)
# inputElement.submit() 
# sbtn.click()
