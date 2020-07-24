import scrapy

class HepsiSpider1(scrapy.Spider):
    name = "productlist"
    page_count = 1
    url_count = 0
    next_url = []
    start_urls = [
        'https://www.hepsiburada.com/projeksiyon-sistemleri-c-285390'
    ] 
    product_number = 1
    def parse (self, response):
        if self.url_count < 1:
            sayfa_sayisi = response.css("div.pagination li a::attr(href)").getall() 
            x = len(sayfa_sayisi)
            sonuncu_sayfa = sayfa_sayisi[x-1]
            for b in range(len(sonuncu_sayfa)):
               if sonuncu_sayfa[b] == "=":
                   a = b
                   break
            sonuncu_sayfa_sayisi = int(sonuncu_sayfa[a+1:])
            for i in range(sonuncu_sayfa_sayisi):
               self.next_url += ["https://www.hepsiburada.com/projeksiyon-sistemleri-c-285390?sayfa={}".format(i+1)]
               self.page_count += 1
        elif 1 <= self.url_count < self.page_count :
            urun_listesi = response.css("div.box.product a::attr(href)").getall()
            for urun in urun_listesi:
                url = "https://www.hepsiburada.com" + urun
                yield scrapy.Request(url , callback = self.parse_page)
        
        next2_url = self.next_url[self.url_count]
        self.url_count += 1
        if next2_url is not None: 
            yield scrapy.Request(url = next2_url, callback= self.parse)

    def parse_page(self, response):
        
        urun_adi = response.css("div.hide-title header.title-wrapper span.product-name::text").get()
        urun_markasi = response.css("div.hide-title span.brand-name a::attr(href)").get()
        yorumlar = response.css("div.ReviewCard-module-34AJ_ div.ReviewCard-module-2dVP9 span[itemprop='description']::text").getall()
        evet_hayir_sayisi = response.css("div.ReviewCard-module-3DD_U span::text").getall()
        toplam_yildiz_sayisi = response.css("div.ReviewCard-module-3Y36S div.RatingPointer-module-1OKF3 svg path::attr(fill)").getall()
        
        with open("products.txt", "a", encoding = "utf-8") as dosya:
            
            dosya.write( str(self.product_number) + ". urun " + str(urun_adi) + "\n")
            dosya.write(str(urun_markasi[1:].capitalize()) + "\n") 
            i = 1
            d = 1
            z = 0
            if len(yorumlar) != 0:
                for yorum in yorumlar:
                    dosya.write(str(self.product_number) + ". urun " + str(i) + ". yorum " + yorum + "\n")
                    dosya.write("evet sayisi = " + str(evet_hayir_sayisi[d]) + "    " )
                    dosya.write("hayir sayisi = " + str(evet_hayir_sayisi[d+3]) + "    " )
                    i +=1
                    d += 6
                    yildiz_sayisi = 0                
                    for y in range(5):                    
                        if toplam_yildiz_sayisi[z] == "#f28b00":
                            yildiz_sayisi += 1
                        z += 1
                    dosya.write("yildiz sayisi = " + str(yildiz_sayisi) + "\n")
            else:
                dosya.write("Yorum yok\n")
            self.product_number += 1



