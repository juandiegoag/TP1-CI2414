from scrapy.spiders import BaseSpider
from urllib2 import urlopen
import scrapy
import Queue
from scrapy import Request
import os
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from stemming.porter2 import stem


class CalpurniaSpider(scrapy.Spider):
    name = "CalpurniaCrawler"
    allowed_domains = ["wiki.archlinux.org"]
    start_urls = ['https://wiki.archlinux.org/']

    
    URLsDiccc = {}
    indexId = 1
    termDiccc = {}
    #os.remove("*.json")
    #print("File Removed!")s

    start_urls = [
        'https://wiki.archlinux.org/',
    ]
  
    def parse(self, response):
        next_page = "https://wiki.archlinux.org/"

        if not response.url in self.URLsDiccc.keys():        
            self.URLsDiccc[ response.url ] = self.indexId
            self.indexId +=  1
            content = response.css('#content')

            for word in content.css('p *::text').re(r'\w+'):
                stemmedword = stem(word) #aplica stemming a cada palabra
                # si la palabra no existe en el diciconario de postings, la agrega, y la empareja con un set vacio
                if stemmedword not in self.termDiccc:
                    self.termDiccc[stemmedword] = set()
                # este o no en el diccionario, si la encontro, tiene que agregarla a la lista de postings. Asociada al documento.  
                self.termDiccc[stemmedword].add(self.indexId-1)
                yield {
                    response.url: stemmedword
                }

        hrefs = response.css('a').xpath('@href').extract()
        for ref in hrefs:
            if not ref.startswith( "https://wiki.archlinux.org/"):
                print( "\ndroped url " + ref + "\n")
            else:
                if ref in self.URLsDiccc.keys():
                    print("omiting already parsed page from hrefs found")
                else:
                    print( "\n\n next page: " + ref  + "\n\n" )
                    yield Request(ref, callback=self.parse)
        #imprime el diccionario palabra - set ------> postings
        print self.termDiccc
    
      
    