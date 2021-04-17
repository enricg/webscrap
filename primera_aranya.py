__author__ = 'HAMASITO'

from scrapy.item import Item, Field
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

# Problema: Extraure informació d'StackOverflow: Problemes

class Pregunta(Item):
    pregunta = Field()
    id = Field()

class StackOverFlowSpider(Spider):
    name ="MiPrimerSpider"
    start_urls = ['https://stackoverflow.com/questions/']
    def parse(self, response):
        sel = Selector(response)
        preguntas = sel.xpath('//div[@id="questions"]/div')

        # Iterar sobre totes les preguntes
        for i, elem in enumerate(preguntas):
            item = ItemLoader(Pregunta(), elem)
            item.add_xpath('pregunta', './/h3/a/text()')
            item.add_value('id', i)
            yield item.load_item()
