import scrapy


class AutoRuSpider(scrapy.Spider):
    name = "autoru"
    start_urls = ['https://auto.ru/sankt-peterburg/cars/nissan/all/']

    def parse(self, response):
        for href in response.css('div.ListingItem-module__columnCellSummary a::attr(href)'):
            yield response.follow(href, callback=self.parse_card)

        for href in response.css('div.ListingPagination-module__sequenceControls a::attr(href)'):
            yield response.follow(href, callback=self.parse)

    def need_skip(self, response):
        is_sold = response.css('div.CardSold__info').get() != None
        is_new = False
        return is_sold or is_new

    def parse_card(self, response):
        if self.need_skip(response):
            return None

        name = response.css('div.CardSidebarActions__title::text').get()
        price = response.css('span.OfferPriceCaption__price::text').get()
        year = response.css('span.CardInfoRow__cell a::text').get()

        mileage_row = response.css('li.CardInfoRow_kmAge')
        mileage_element = mileage_row.css("span.CardInfoRow__cell")[1]
        mileage = mileage_element.css("::text").get()

        owners_row = response.css('li.CardInfoRow_ownersCount')
        owners_element = owners_row.css("span.CardInfoRow__cell")[1]
        owners = owners_element.css("::text").get()

        photo_link = response.css('img.ImageGalleryDesktop__image').attrib['src'];

        yield {
            'name': name,
            'year': year,
            'price': price,
            'mileage': mileage,
            'owners': owners,
            'link:': response.url,
            'image_link': response.urljoin(photo_link)
        }