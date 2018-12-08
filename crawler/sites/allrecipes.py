
from parser import Parser
import nltk
import re


BASE_URL = "http://allrecipes.com"
parenthesesRegex = re.compile(r"\([^()]*\)")


class AllRecipes(Parser):
    def __init__(self, recipeId):
        super().__init__(f"{BASE_URL}/{recipeId}")

    def getTitle(self):
        return self.soup.find("title").text.split("Recipe")[0].strip()

    def getSource(self):
        return BASE_URL

    def getImages(self):
        images = []
        ul = self.soup.find('ul', class_='photo-strip__items')
        if ul is None:
            ul = self.soup.find('div', class_='image-filmstrip')
        for img in ul.find_all('img'):
            images.append(img['src'])
        return images

    def getIngredients(self):
        ingredients = []
        for span in self.soup.find_all("span", itemprop="recipeIngredients"):
            ingredients.append(span.text)
        return ingredients

    def getDirections(self):
        directions = []
        directionsString = ""

        # concat all directions to one string
        directionObjects = self.soup.find_all("li", class_="instructions-section-item")
        if directionObjects:
            for li in directionObjects:
                directionsString += " " + li.find("p").text
        else:
            directionObjects = self.soup.find_all("span", class_="recipe-directions__list--item")
            count = len(directionObjects) - 1  # 1 empty span at end
            for i in range(count):
                directionsString += " " + directionObjects[i].text

        # use nltk to split direction string into sentences
        individualDirections = nltk.sent_tokenize(directionsString)
        for i in range(0, len(individualDirections)):
            direction = {}
            direction["step"] = i + 1
            direction["direction"] = individualDirections[i]
            directions.append(direction)

        return directions
