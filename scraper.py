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
from splinter import Browser
import sys, traceback, logging, shutil, platform

dev_mode = False;


def select_full_holidings_and_marc_tags(browser):
  print 'selecting full holdings and marc tags'
  browser.find_by_name('VOPTIONS').first.click()

  if not browser.is_element_present_by_name('SCROLL^S', wait_time=30):
      raise Exception("Failed to find SCROLL^S")

  browser.select("vopt_unformatted", "Y")
  browser.select("vopt_elst", "ALL")
  if dev_mode :
    brower.screenshot('screen_0004.png')
  browser.find_by_name('SCROLL^S').first.click()

  if browser.is_element_present_by_name("VOPTIONS", wait_time=15):
      print 'Got full details page'

  print 'done'
  return

def scrape_item_info(browser):
  print 'Getting item info'
  # bibinfo_div = driver.find_element_by_name('bibinfo') - It's class not name
  # title = bibinfo_div.find_element_by
  return

def scrape_catalog_info(browser):
  print 'Getting catalog info'

  browser.find_by_id('tab3').first.click()
  # Do we need to wait for the content?

  print 'Get marc_data table'
  raw_data_table = browser.find_by_xpath(
      "//a[@name='marc_data']/following-sibling::table"
  )

  trs = raw_data_table.find_by_tag("tr")
  for row in trs:
    marc_tag = row.find_by_xpath("./th")
    # print "procesing tag %s" % marc_tag.text()
    indicators = row.find_by_xpath("./td[1]")
    tag_content = row.find_by_xpath("./td[2]")
    print 'Handling content %s' % tag_content.text
    inner_anchor = tag_content.find_by_xpath("./a")
    v = None
    if len(inner_anchor) == 1 :
      value = inner_anchor[0].text
    else:
      v = tag_content.text

    print "Got tag %s indicators %s value %s" % ( marc_tag.text, indicators.text, v )
  return

def scrape_resource_page(browser) :
  print 'scraping a resource'
  scrape_item_info(browser)
  scrape_catalog_info(browser)
  return

def report_module(name):
  inf = sys.modules[name]
  if hasattr( inf, '__version__' ):
    print name, inf.__version__
  else:
    print "No version info for ", name


def scrape_ibistro() :
  try:
    print "platform %s" % platform.system()
    print "Python ", sys.version_info
    report_module('splinter');
    report_module('scraperwiki');

    with Browser('phantomjs') as browser:

        # The plan is to use this
        # for i in range(ord('a'), ord('n')+1):
        #    print chr(i),
        # To submit a query for every letter and number then iterate the results, indexing by a hash of the identifers [to cope with dups]
        # We'll do the following for each ord - in testing just the a$s  [$ is a wildcard!]
        # Good selenium docs here:: http://selenium-python.readthedocs.org/en/latest/locating-elements.html

        # Whack up the debug to see if we can figure out why this throws a Bad Status Line exception when running remotely
        # driver.set_debuglevel(1)
        # Get the front page
        print 'Get front page'
        browser.visit('http://library.sheffield.gov.uk/uhtbin/webcat')

        print 'starting'

        # Save screenshot for debug
        if dev_mode :
            browser.screenshot('screen_0001.png') # save a screenshot to disk

        # Find the search field combo
        # Say we want to search by title
        browser.select("srchfield1", "TI^TITLE^SERIES^Title Processing^title")

        # find the search input text control
        # Send the query a$ [Or the ord above]
        browser.fill("searchdata1", "a$")
        # Send enter to cause the search to execute
        button = browser.find_by_xpath(
            '//input[@class="searchbutton" and @value="Search"]'
        ).first
        button.click()

        print 'Waiting for first item in results page to appear'

        # Wait for the search results page to finish loading
        if not browser.is_element_present_by_id('VIEW1', wait_time=30):
            raise Exception('Failed to find VIEW1')

        # Debugging
        if dev_mode:
            browser.save_screenshot('screen_0002.png') # save a screenshot to disk

        print 'Clicking button with name VIEW^1'

        # Now click the details button for search result 1
        browser.find_by_name('VIEW^1').first.click()
        # Currently blows up here due to problem with phantomjs 1.9.0

        print 'Waiting for details page to finish loading'

        # Wait for the details page to finish loading
        if browser.is_element_present_by_name('VOPTIONS', wait_time=15):
            print 'Got full details page'

        print 'got form_type input control.. good to continue'

        if dev_mode:
            browser.save_screenshot('screen_0003.png') # save a screenshot to disk

        select_full_holidings_and_marc_tags(browser)

        if dev_mode:
            browser.save_screenshot('screen_0005.png') # save a screenshot to disk

        scrape_resource_page(browser)

        while browser.is_element_present_by_name('SCROLL^F', wait_time=15):
            print 'Moving to next record'
            next_link = browser.find_by_name('SCROLL^F');
            next_link.click()
            scrape_resource_page(browser)
            



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
