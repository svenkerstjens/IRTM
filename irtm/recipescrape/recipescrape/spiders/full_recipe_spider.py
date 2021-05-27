import scrapy
from ..items import RecipeItem

# urls for recipes starting with each letter of the alphabet
urls = []
pages = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z', '0-9']
for page in pages:
    urls.append('https://www.bbc.co.uk/food/recipes/a-z/{}/1#featured-content'.format(page))


class RecipeSpider(scrapy.Spider):
    name = 'allrecipes'
    start_urls = urls

    def parse(self, response, **kwargs):
        '''
        Opens each recipe on the page and goes to the next page
        '''
        for href in response.css('.gel-layout__item.gel-1\/2.gel-1\/3\@m.gel-1\/4\@xl a::attr(href)').getall():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_recipe)
        next_page = response.css('a.pagination__link::attr(href)')[-1].get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_recipe(self, response, **kwargs):
        '''
        Scrapes all features from the recipe page
        '''
        name = response.css('h1.gel-trafalgar.content-title__text::text').get()
        preparation_time = response.css('p.recipe-metadata__prep-time::text').get()
        cooking_time = response.css('p.recipe-metadata__cook-time::text').get()
        serving = response.css('p.recipe-metadata__serving::text').get()
        sub_recipe_names = response.css('h3.recipe-ingredients__sub-heading::text').getall()
        ingredients_with_properties = [ingredient.css('::text').getall() for ingredient in
                                       response.css('.recipe-ingredients__list-item')]
        all_ingredients = response.css(
            'ul.recipe-ingredients__list li a.recipe-ingredients__link::text').getall()
        sub_recipe_ingredients = [recipe.css('::text').getall() for recipe in
                                  response.css('.recipe-ingredients__list')]
        methods = [step.css('::text').getall() for step in response.css('.recipe-method__list-item-text')]
        author = response.css('.chef.gel-brevier a::attr(title)').get()
        description = response.css('.recipe-description__text::text').getall()

        recipe = RecipeItem()

        recipe['name'] = name
        recipe['preparation_time'] = preparation_time
        recipe['cooking_time'] = cooking_time
        recipe['serving'] = serving
        recipe['all_ingredients'] = all_ingredients
        recipe['ingredients_with_properties'] = ingredients_with_properties
        recipe['sub_recipe_names'] = sub_recipe_names
        recipe['sub_recipe_ingredients'] = sub_recipe_ingredients
        recipe['methods'] = methods
        recipe['author'] = author
        recipe['description'] = description

        yield recipe
