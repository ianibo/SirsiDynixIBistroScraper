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
import sys, traceback, logging, shutil, platform

dev_mode = False;

# This might be relevant https://groups.google.com/forum/#!msg/phantomjs/uKTIEYenw78/to4rWFJ8sDgJ
# This seems to suggest some kind of timeout issue : https://github.com/burnash/gspread/issues/157#issuecomment-53970265
def wait_for_details_page(driver):
  print 'Waiting for details page'
  # Wait for the details page to finish loading
  WebDriverWait(driver, 30).until(
    # Looks like presence of is our problem!
    # expected_conditions.presence_of_element_located((By.NAME, "form_type"))
    expected_conditions.visibility_of_element_located((By.CLASS_NAME, "bibinfo"))
  )
  print 'Got full details page'
  return


def select_full_holidings_and_marc_tags(driver):
  print 'selecting full holdings and marc tags'
  change_holdings_display_link = driver.find_element_by_name('VOPTIONS')
  change_holdings_display_link.click()

  # Wait for options page to display
  WebDriverWait(driver, 30).until(
    expected_conditions.visibility_of_element_located((By.NAME, "SCROLL^S"))
  )

  unformatted_option =  Select(driver.find_element_by_name('vopt_unformatted'))
  unformatted_option.select_by_value('Y');
  view_option =  Select(driver.find_element_by_name('vopt_elst'))
  view_option.select_by_value('ALL');
  if dev_mode :
    driver.save_screenshot('screen_0004.png')
  ok_button = driver.find_element_by_name('SCROLL^S');
  ok_button.click();
  wait_for_details_page(driver);
  print 'done'
  return

def scrape_item_info(driver):
  print 'Getting item info'
  # bibinfo_div = driver.find_element_by_name('bibinfo') - It's class not name
  # title = bibinfo_div.find_element_by
  return

def scrape_catalog_info(driver):
  print 'Getting catalog info'
  item_info_tab = driver.find_element_by_id('tab3')
  item_info_tab.click()
  # Do we need to wait for the content?

  print 'Get marc_data table'
  raw_data_table = driver.find_element_by_xpath("//a[@name='marc_data']/following-sibling::table")

  trs = raw_data_table.find_elements(By.TAG_NAME, "tr")
  for row in trs:
    marc_tag = row.find_element_by_xpath("./th")
    # print "procesing tag %s" % marc_tag.text()
    indicators = row.find_element_by_xpath("./td[1]")
    tag_content = row.find_element_by_xpath("./td[2]")
    print 'Handling content %s' % tag_content.text
    inner_anchor = tag_content.find_elements_by_xpath("./a")
    v = None
    if len(inner_anchor) == 1 :
      value = inner_anchor[0].text
    else:
      v = tag_content.text

    print "Got tag %s indicators %s value %s" % ( marc_tag.text, indicators.text, v )
  return

def scrape_resource_page(driver) :
  print 'scraping a resource'
  scrape_item_info(driver)
  scrape_catalog_info(driver)
  return


def scrape_ibistro() :
  try:
    print "platform %s" % platform.system()

    # driver = webdriver.PhantomJS('phantomjs') # or add to your PATH
    # driver = webdriver.PhantomJS('./phantomjs_1_9_2_linux_64', service_args=["--webdriver-loglevel=DEBUG", "--load-images=false"]) # or add to your PATH
    driver = webdriver.PhantomJS('./phantomjs_1_9_2_linux_64', service_args=["--webdriver-loglevel=DEBUG"]) # or add to your PATH
    driver.set_window_size(1024, 768) # optional

    # The plan is to use this
    # for i in range(ord('a'), ord('n')+1):
    #    print chr(i),
    # To submit a query for every letter and number then iterate the results, indexing by a hash of the identifers [to cope with dups]
    # We'll do the following for each ord - in testing just the a$s  [$ is a wildcard!]
    # Good selenium docs here:: http://selenium-python.readthedocs.org/en/latest/locating-elements.html

    # Whack up the debug to see if we can figure out why this throws a Bad Status Line exception when running remotely
    # driver.set_debuglevel(1)
    # Get the front page
    driver.get('http://library.sheffield.gov.uk/uhtbin/webcat')

    print 'starting'

    # Save screenshot for debug
    if dev_mode :
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

    print 'Waiting for first item in results page to appear'

    # Wait for the search results page to finish loading
    WebDriverWait(driver, 30).until(
            expected_conditions.visibility_of_element_located((By.ID, "VIEW1"))
    )

    # Debugging
    if dev_mode:
      driver.save_screenshot('screen_0002.png') # save a screenshot to disk

    print 'Clicking button with name VIEW^1'

    # Now click the details button for search result 1
    view_record_1_button = driver.find_element_by_name('VIEW^1')
    view_record_1_button.click()
    # Currently blows up here due to problem with phantomjs 1.9.0

    print 'Waiting for details page to finish loading'

    # Wait for the details page to finish loading
    wait_for_details_page(driver)

    print 'got form_type input control.. good to continue'

    if dev_mode:
      driver.save_screenshot('screen_0003.png') # save a screenshot to disk

    select_full_holidings_and_marc_tags(driver)

    if dev_mode:
      driver.save_screenshot('screen_0005.png') # save a screenshot to disk

    scrape_resource_page(driver)


  except:
    print "Unexpected error:", sys.exc_info()
    # logging.exception("Error")
    # traceback.print_exc()
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback)

  # Eek this is __dirty__ - copy the ghostdriver.log to stdout so it appears on the morph.io screen for easy [easier] debugging
  if dev_mode is True:
    with open("ghostdriver.log", "r") as f:
      shutil.copyfileobj(f, sys.stdout)


  # Extra notes
  # https://realpython.com/blog/python/headless-selenium-testing-with-python-and-phantomjs/
  return

print 'DoIt'
scrape_ibistro();
print 'DoneIt'
