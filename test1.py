from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import unittest

class BestDealsAround(unittest.TestCase):
    


    @classmethod
    def setUpClass(self):
        print("Tip: for accurate results of your query, try typing in '[name of game] [console] game'")
        query = input("Enter the name of the game you want to look up: ")
        self.query = query
        self.array = []



    def setUp(self):
        
        
        service = Service()
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service,options=options)
        self.wait = WebDriverWait(self.driver,10)
        self.timer = 1 #Web pages takes time to load, even after the page is loaded. Depending on your system, this can be higher or lower.
        
        
    
    def test_ebay(self):
        
        #A bit harder to implement. The cheapest deal around, but quality is vast. You may not even find what you're looking for.
        
        
        start_time = time.time()
        self.driver.get("https://ebay.com/")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME,'body')))#Sometimes we can just wait until the body is loaded. If there is additional loading after this, more time is required.
        dropbox = Select(self.driver.find_element(By.ID, 'gh-cat'))
        dropbox.select_by_index(34)
        dropbox = self.driver.find_element(By.ID, 'gh-ac')
        dropbox.send_keys(self.query)
        dropbox.send_keys(Keys.RETURN)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME,'body')))


        
        #go from low to high
        #breakpoint()
   
        listofitems = self.driver.find_elements(By.CSS_SELECTOR,'.s-item__wrapper')

        #Unfortunately, sponsored content is shadow root (closed). Meaning you can't fetch them to this machine. This is why you might not get what you're looking for.



        hyperlink = listofitems[1].find_element(By.CSS_SELECTOR,'.s-item__link').get_attribute('href')
        self.driver.get(hyperlink)


     
        
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.x-price-primary')))
        #breakpoint()

           

        maincontent = self.driver.find_element(By.ID,'mainContent')##finds the div we only care about, mainCotent
        price = self.driver.find_element(By.CSS_SELECTOR,'.x-price-primary').text


        price = price.lstrip("US $")
        price = float(price)
        #breakpoint()
        titleelement = maincontent.find_element(By.CSS_SELECTOR,'.x-item-title__mainTitle')
        title = titleelement.text
        
        end_time = time.time()
        total_time = end_time-start_time#time it took to do this thing
        self.array.append({"title": title,"url": hyperlink, "price": price,"time":total_time})
      
    

    def test_amazon(self):
    #Prediction: A bit harder to implement due to sponsors. Middle-tier pricing. Reliable quality.
        start_time = time.time()
        self.driver.get("https://www.amazon.com/")
        dropbox = ""
        whileflag = False
        while(not(whileflag)):
            try:
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME,'body')))##sometyimes the dropdownbox just... doesn't show up. So loop until it does.
                dropbox = Select(self.driver.find_element(By.ID,'searchDropdownBox'))
                whileflag = True
            except:
                whileflag = False
                self.driver.refresh()
        
        
        dropbox.select_by_visible_text("Video Games")
        self.wait.until(EC.presence_of_element_located((By.ID,'twotabsearchtextbox')))
        searchbox = self.driver.find_element(By.ID,'twotabsearchtextbox')
        searchbox.send_keys(self.query)
        searchbox.send_keys(Keys.RETURN)


        self.wait.until(EC.presence_of_element_located((By.TAG_NAME,'body')))
        listofitems = self.driver.find_elements(By.CSS_SELECTOR,'.s-result-item')##Get all the elements that have the class = s-result-item. All the search results have this class.
        
        getridoff = []
        for item in listofitems:
            if 'Sponsored' in item.text:
                getridoff.append(item)##get rid of all the elements that have 'Sponsored' in its name. This is not sponsored by Raid Shadow Legends.


        for item in getridoff:
            listofitems.remove(item)

        elementwithhyperlink = listofitems[1].find_element(By.CSS_SELECTOR,'.a-link-normal')
        hyperlink = elementwithhyperlink.get_attribute('href')
        self.driver.get(hyperlink)#Go to the most relevent page

        
        self.wait.until(EC.presence_of_element_located((By.ID,'productTitle')))
        
        title = self.driver.find_element(By.ID,'productTitle').text
        #breakpoint()
        
        self.wait.until(EC.presence_of_element_located((By.ID,'apex_offerDisplay_desktop')))#this is the offer found on the right of the screen
        pricecontainer = self.driver.find_element(By.ID,'apex_offerDisplay_desktop')
        #print(pricecontainer.text)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.a-price-whole')))
        newpriceelement = pricecontainer.find_element(By.CSS_SELECTOR,'.a-price-whole')
        wholenumber = newpriceelement.text
        wholenumber = wholenumber[:2]+ "." #first two chars. and a period
        fractionnumber = pricecontainer.find_element(By.CSS_SELECTOR,'.a-price-fraction')#perhaps the third-party vendors have been deals... but conditions can differ wildly. Let's just leave that deicision to the user
        price = wholenumber+fractionnumber.text
        price = float(price)
        end_time = time.time()
        total_time = end_time - start_time
        self.array.append({"title": title,"url": hyperlink, "price": price,"time":total_time})

    
    def test_gamestop(self):
        #Estimated: the quickest and easiest to implement but pricey (gamestop always has the worst deals...)
        print("Warning: Gamestop has anti-botting mechanism that can put your IP on their blacklist.")
        start_time = time.time()
        self.driver.get("https://www.gamestop.com/")
        if(self.driver.title=="Access Denied"):
            self.fail("You are on GameStop's blacklist. Get a VPN.")
        hyperlink = ""
        inputbox = self.wait.until(EC.presence_of_element_located((By.NAME,'q')))
        inputbox.send_keys(self.query)
        time.sleep(self.timer)
        inputbox.send_keys(Keys.RETURN)
        try:
            firstresult = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.product-tile-link')))
            hyperlink = firstresult.get_attribute('href')
            self.driver.get(hyperlink)
        except:
            self.fail("No result found")
        
        title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.product-name'))).text
        price = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.fromPriceLabel'))).text #pro-memberships can lead to slightly better results.
        price = price.lstrip("$")
        end_time = time.time()
        total_time = end_time - start_time

        self.array.append({"title": title,"url": hyperlink, "price": price,"time":total_time})
    
        

    
    def tearDown(self):
        self.driver.quit()

    @classmethod
    def tearDownClass(self):
        print("Tearing down...")
        min_price_item = min(self.array, key=lambda x: x["price"])

        print("details of the lowest item:")
        print("Title: "+ min_price_item['title'])
        print("Price: "+ str(min_price_item['price']))
        print("Time to complete this test: "+str(min_price_item['time'])+" Seconds\n")
        print("URL: " + min_price_item['url'])

        if(min_price_item == None):
            print("Nothing? You sure you typed in the results right?")


if __name__=='__main__':
    unittest.main()