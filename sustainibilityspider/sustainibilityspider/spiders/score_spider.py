import scrapy
import logging
import unicodedata
import sqlite3
import pandas as pd

class ScoreSpider(scrapy.Spider):
    name = "sussywussy"

    def start_requests(self):
        yield scrapy.Request(url='http://af-foodpro1.campus.ads.umass.edu/foodpro.net/location.aspx', callback=self.parseMain)

    def parseMain(self, response):
        hrefs = response.xpath("//span[contains(@class, 'locationchoices')]/a/@href").getall()
        for href in hrefs:
            yield scrapy.Request(url=response.urljoin(href), callback=self.parseLocation)
    
    def parseLocation(self, response):
        df = pd.DataFrame(columns=['LOCATION', 'MEAL', 'DESCS', 'BIO', 'VEG', 'SUS', 'WHOLE', 'HAL', 'VEGAN', 'LOCAL', 'RECIPE'])
        
        title = response.xpath("//div[contains(@class,'headlocation')]/text()").get()
        logging.info(title)
        mealxpaths = response.xpath("//div[contains(@class, 'shortmenumeals')]")
        if mealxpaths:
            for mealxpath in mealxpaths:
                mealname = mealxpath.xpath(".//text()").get()
                tables = mealxpath.xpath(".//ancestor::table[1]/ancestor::table[1]")
                descxpaths = tables.xpath(".//div[contains(@class,'shortmenucats')]/span")
                if descxpaths:
                    for descxpath in descxpaths:
                        desc = descxpath.xpath(".//text()").get().strip(" -")
                        row = descxpath.xpath(".//ancestor::tr[1]/following-sibling::tr[1]")
                        recipes = []
                        while not row.xpath(".//td/div[contains(@class,'shortmenucats')]") and row:
                            recipe = row.xpath(".//td/div[contains(@class,'shortmenurecipes')]/span/text()").get()
                            isBioticFree = bool(row.xpath(".//img[contains(@src, 'icon-antibfr.jpg')]"))
                            isVeg = bool(row.xpath(".//img[contains(@src, 'icon-veg.jpg')]"))
                            isSus = bool(row.xpath(".//img[contains(@src, 'icon-sus.jpg')]"))
                            isWholeGrn = bool(row.xpath(".//img[contains(@src, 'icon-whlgrn.jpg')]"))
                            isHal = bool(row.xpath(".//img[contains(@src, 'icon-hal.jpg')]"))
                            isVegan = bool(row.xpath(".//img[contains(@src, 'icon-vegan.jpg')]"))
                            isLocal = bool(row.xpath(".//im g[contains(@src, 'icon-loc.jpg')]"))
                            recipes.append(unicodedata.normalize('NFKD', recipe).strip())
                            row = row.xpath("./following-sibling::tr[1]")
                            new_row = {'LOCATION': title, 'MEAL': mealname, 'DESCS': desc, 'BIO': isBioticFree, 'VEG': isVeg, 'SUS': isSus, 'WHOLE': isWholeGrn, 'HAL': isHal, 'VEGAN': isVegan, 'LOCAL': isLocal, 'RECIPE': recipe}
                            df = df.append(new_row, ignore_index = True)
                        logging.info(recipes)
        con = sqlite3.connect('../database/susresults.db')
        df.to_sql("susresults", con, if_exists="replace")
        