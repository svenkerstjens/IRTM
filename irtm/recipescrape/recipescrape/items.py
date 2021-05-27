# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipescrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class RecipeItem(scrapy.Item):
    name = scrapy.Field()
    preparation_time = scrapy.Field()
    cooking_time = scrapy.Field()
    serving = scrapy.Field()
    sub_recipe_names = scrapy.Field()
    ingredients_with_properties = scrapy.Field()
    all_ingredients = scrapy.Field()
    sub_recipe_ingredients = scrapy.Field()
    methods = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
