
PhantomJS 2.0 testing


When running with a non-std port like 9001 this error

    Injecting configuration and compiling...
     Injecting scraper and running...
     DoIt
     platform Linux
     Python   sys.version_info(major=2, minor=7, micro=9, releaselevel='final', serial=0)
     selenium 2.47.1
     No version info for  scraperwiki
     Unexpected error:  (<class 'selenium.common.exceptions.WebDriverException'>, WebDriverException(), <traceback object at 0x7f340eccbf80>)
       File "scraper.py", line 131, in scrape_ibistro
         driver = webdriver.PhantomJS('./phantomjs_2_0_0_linux_64', service_args=["--webdriver-loglevel=DEBUG", "--webdriver=9001"]) # or add to your PATH
       File "/app/.heroku/python/lib/python2.7/site-packages/selenium/webdriver/phantomjs/webdriver.py", line 51, in __init__
         self.service.start()
       File "/app/.heroku/python/lib/python2.7/site-packages/selenium/webdriver/phantomjs/service.py", line 83, in start
         "Can not connect to GhostDriver on port {}".format(self.port))
     DoneIt

When running with defaults same error

    Injecting configuration and compiling...
     Injecting scraper and running...
     DoIt
     platform Linux
     Python   sys.version_info(major=2, minor=7, micro=9, releaselevel='final', serial=0)
     selenium 2.47.1
     No version info for  scraperwiki
     Unexpected error:  (<class 'selenium.common.exceptions.WebDriverException'>, WebDriverException(), <traceback object at 0x7fa617271f80>)
       File "scraper.py", line 131, in scrape_ibistro
         driver = webdriver.PhantomJS('./phantomjs_2_0_0_linux_64', service_args=["--webdriver-loglevel=DEBUG"]) # or add to your PATH
       File "/app/.heroku/python/lib/python2.7/site-packages/selenium/webdriver/phantomjs/webdriver.py", line 51, in __init__
         self.service.start()
       File "/app/.heroku/python/lib/python2.7/site-packages/selenium/webdriver/phantomjs/service.py", line 83, in start
         "Can not connect to GhostDriver on port {}".format(self.port))
     DoneIt


But running locally gives

    
    (oaf)ibbo@xuss:~/dev/SirsiDynixIBistroScraper$ python scraper.py 
    DoIt
    platform Linux
    Python  sys.version_info(major=2, minor=7, micro=9, releaselevel='final', serial=0)
    selenium 2.47.1
    No version info for  scraperwiki
    starting
    Waiting for first item in results page to appear
    Clicking button with name VIEW^1
    Waiting for details page to finish loading
    Waiting for details page
    Got full details page
    got form_type input control.. good to continue
    selecting full holdings and marc tags
    Waiting for details page
    Got full details page
    done
    scraping a resource
    Getting item info
    Getting catalog info
    Get marc_data table
    Handling content   am i
    Got tag 000 indicators   value   am i
    Handling content   BDZ0022028421
    Got tag 001 indicators   value   BDZ0022028421
    Handling content   StDuBDS
    Got tag 003 indicators   value   StDuBDS
    Handling content   20150128014912.0
    Got tag 005 indicators   value   20150128014912.0
    Handling content   140113r20142013enk 000 f|eng|d
    Got tag 008 indicators   value   140113r20142013enk 000 f|eng|d
    Handling content   9780099580881 (pbk.) :|c�7.99
    Got tag 020 indicators   value   9780099580881 (pbk.) :|c�7.99
    Handling content   StDuBDS|beng|cStDuBDS|dStDuBDSZ|erda
    Got tag 040 indicators   value   StDuBDS|beng|cStDuBDS|dStDuBDSZ|erda
    Handling content   PR6058.A69147
    Got tag 050 indicators  4 value   PR6058.A69147
    Handling content   THR|2ukslc
    Got tag 072 indicators  7 value   THR|2ukslc
    Handling content   823.92|223
    Got tag 082 indicators 04  value   823.92|223
    Handling content   Harris, Robert,|d1957-|eauthor.|?UNAUTHORIZED
    Got tag 100 indicators 1  value None
    Handling content   An officer and a spy /|cRobert Harris.
    Got tag 245 indicators 13  value None
    Handling content   1st paperback ed
    Got tag  indicators   value   1st paperback ed
    Handling content   London :|bArrow Books,|c2014.|?UNAUTHORIZED
    Got tag 260 indicators   value   London :|bArrow Books,|c2014.|?UNAUTHORIZED
    Handling content   611 pages ;|c20 cm
    Got tag 300 indicators   value   611 pages ;|c20 cm
    Handling content   text|2rdacontent
    Got tag 336 indicators   value   text|2rdacontent
    Handling content   unmediated|2rdamedia
    Got tag 337 indicators   value   unmediated|2rdamedia
    Handling content   volume|2rdacarrier
    Got tag 338 indicators   value   volume|2rdacarrier
    Handling content   Originally published: London: Hutchinson, 2013.
    Got tag 500 indicators   value   Originally published: London: Hutchinson, 2013.
    Handling content   Paris, January 1895. Army officer Georges Picquart witnesses a convicted spy, Captain Alfred Dreyfus, being humiliated in front of 20,000 spectators baying 'Death to the Jew!' The officer is promoted and put in command of shadowy intelligence unit, the Statistical Section. The spy is shipped off to a lifetime of solitary confinement on Devil's Island and his case seems closed forever. But gradually Picquart comes to believe there is something rotten at the heart of the Statistical Section.
    Got tag 520 indicators 8  value   Paris, January 1895. Army officer Georges Picquart witnesses a convicted spy, Captain Alfred Dreyfus, being humiliated in front of 20,000 spectators baying 'Death to the Jew!' The officer is promoted and put in command of shadowy intelligence unit, the Statistical Section. The spy is shipped off to a lifetime of solitary confinement on Devil's Island and his case seems closed forever. But gradually Picquart comes to believe there is something rotten at the heart of the Statistical Section.
    Handling content   Dreyfus, Alfred,|d1859-1935|vFiction.|?UNAUTHORIZED
    Got tag 600 indicators 10  value None
    Handling content   Picquart, Georges,|d1854-1914|vFiction.|?UNAUTHORIZED
    Got tag 600 indicators 10  value None
    Handling content   France|xHistory, Military|vFiction.|?UNAUTHORIZED
    Got tag 651 indicators  0 value None
    Handling content   Suspense fiction.
    Got tag 655 indicators  0 value None
    Handling content   Thriller.|2ukslc|?UNAUTHORIZED
    Got tag 655 indicators  7 value None
    Handling content   3 6 7 8 9 12 14 27 33 34 39 41 46 48
    Got tag 596 indicators   value   3 6 7 8 9 12 14 27 33 34 39 41 46 48
    DoneIt
    (oaf)ibbo@xuss:~/dev/SirsiDynixIBistroScraper$ 
    
