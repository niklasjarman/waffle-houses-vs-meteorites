from scrapy.item import Item, Field


class StackItem(Item):
    name = Field()
    address = Field()
    city = Field()
    state = Field()
    zip_code = Field()
    latitude = Field()
    longitude = Field() 