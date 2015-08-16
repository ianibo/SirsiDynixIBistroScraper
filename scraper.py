# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

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

# for other data https://classic.scraperwiki.com/docs/python/python_datastore_guide/

import scraperwiki
import lxml.html
import hashlib
import re
from splinter import Browser
import sys, traceback, logging, shutil, platform
from string import ascii_lowercase

dev_mode = False;

# This us used to create a version of the tag content with the awful pipe subfield indicator substitution stripped out
subfield_indicator_regex = re.compile(ur"\|.",re.UNICODE)
# subfield_indicator_regex = re.compile(r"(\\|b)")
# print 'testing regex', subfield_indicator_regex.sub('XXX','a |b c |s d |d')

marc_extract_rules = {
  '245' : { 
    'targetColumn' : 'Title',
    'allowRepeated' : False
  }
}


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

def scrape_item_info(browser, resource_properties):
  print 'Getting item info'
  # bibinfo_div = driver.find_element_by_name('bibinfo') - It's class not name
  # title = bibinfo_div.find_element_by
  return

def scrape_catalog_info(browser, resource_properties):
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
    indicators = row.find_by_xpath("./td[1]")
    tag_content = row.find_by_xpath("./td[2]")
    # print 'Handling content %s' % tag_content.text
    inner_anchor = tag_content.find_by_xpath("./a")
    v = None
    if len(inner_anchor) == 1 :
      # v = inner_anchor[0].text.decode('windows-1252','replace')
      # v = unicode(inner_anchor[0].text, 'windows-1252', 'ignore')
      v = inner_anchor[0].text
    else:
      v = tag_content.text


    # decoded_v = unicode(v,'latin-1')
    decoded_v = v

    # print "Got tag %s indicators %s value %s" % ( marc_tag.text, indicators.text, decoded_v )


    action = marc_extract_rules.get(marc_tag.text)

    if action is not None :
        # print 'Processing', marc_tag.text, 'as ', action['targetColumn'], 'Set to', decoded_v
        # iBistro says it's sending us UTF8 in the header, but then nicely passes windows-1252. Attempt to work
        # around by calling decode.
        resource_properties[action['targetColumn']] = subfield_indicator_regex.sub('',decoded_v);

  return

def scrape_resource_page(browser) :
  print 'scraping a resource'
  resource_properties = {}
  scrape_item_info(browser, resource_properties)
  scrape_catalog_info(browser, resource_properties)

  # Make a key from the title [And some other fields to make the md5 unique]
  if resource_properties.get('Title') is not None :
      m = hashlib.md5()
      # This only works on ascii characters - 
      m.update(resource_properties.get('Title').encode('ascii','ignore'))
      resource_properties['hashCode'] = m.hexdigest()
  else :
      print 'Non title - cant md5 it'

  return resource_properties

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

      for a in ascii_lowercase :
        scrape_a_letter(browser,''+a)
        for b in ascii_lowercase :
          scrape_a_letter(browser,''+a+b)
          for c in ascii_lowercase :
            scrape_a_letter(browser,''+a+b+c)
            for d in ascii_lowercase :
              scrape_a_letter(browser,''+a+b+c+d)

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

  return



def scrape_a_letter(browser,letter) :
  print 'scraping', letter

  browser.visit('http://library.sheffield.gov.uk/uhtbin/webcat')

  print 'starting'

  print "Looking for power search button"
  power_search_button = browser.find_by_xpath('//a[contains(text(),"Power Search")]').first
  power_search_button.click()

  browser.select("match_on", "PARTIAL")
  # match_on partial adds the wildcard for us [And never tells us] and terminates the string at that point *bangs head*
  browser.fill("searchdata3", letter)
  # Send enter to cause the search to execute
  button = browser.find_by_xpath(
    '//input[@class="searchbutton" and @value="Search"]'
  ).first
  button.click()

  print 'Waiting for first item in results page to appear'

  # Wait for the search results page to finish loading
  if not browser.is_element_present_by_id('VIEW1', wait_time=60):
    raise Exception('Failed to find VIEW1')

  # Debugging
  if dev_mode:
    browser.save_screenshot('screen_0002.png') # save a screenshot to disk

  print 'Clicking button with name VIEW^1'

  # Now click the details button for search result 1
  browser.find_by_name('VIEW^1').first.click()

  print 'Waiting for details page to finish loading'

  # Wait for the details page to finish loading
  if browser.is_element_present_by_name('VOPTIONS', wait_time=60):
    print 'Got full details page'

  print 'got form_type input control.. good to continue'

  if dev_mode:
    browser.save_screenshot('screen_0003.png') # save a screenshot to disk

  select_full_holidings_and_marc_tags(browser)

  if dev_mode:
    browser.save_screenshot('screen_0005.png') # save a screenshot to disk

  data = scrape_resource_page(browser)

  try:
    while browser.is_element_present_by_name('SCROLL^F', wait_time=60):
      if data is not None :
        scraperwiki.sqlite.save(unique_keys=['hashCode'], data=data)
        print 'Processing data = ', data
        print 'Moving to next record'
      else :
        print("** NO DATA **");
  
      next_link = browser.find_by_name('SCROLL^F');
      next_link.click()
      data = scrape_resource_page(browser)
  except:
    print "Exception looking for NEXT - looks like we reached the end of the results - on to next nonce"

  print("Looks like we reached the end of the next page links...");

  return

print 'DoIt'
scrape_ibistro();
print 'DoneIt'
