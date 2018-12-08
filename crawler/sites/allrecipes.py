
from parser import Parser
import nltk
import re


class AllRecipesError(Exception):
    pass


BASE_URL = "http://allrecipes.com"
parenthesesRegex = re.compile(r"\([^()]*\)")


class AllRecipes(Parser):
    def __init__(self, recipeId):
        super().__init__(f"{BASE_URL}/recipe/{recipeId}")

    def getTitle(self):
        return self.soup.find("title").text.split("Recipe")[0].strip()

    def getSource(self):
        return BASE_URL

    def getImages(self):
        images = []
        ul = self.soup.find('ul', class_='photo-strip__items')
        if ul is None:
            ul = self.soup.find('div', class_='image-filmstrip')
        imageObjects = ul.find_all('img')
        if len(imageObjects) < 1:
            raise AllRecipesError("[ERROR] No image found.")
        for img in imageObjects:
            images.append(img['src'].strip())
        return images

    def getIngredients(self):
        ingredients = []
        ingredientObjects = self.soup.find_all("span", itemprop="recipeIngredient")
        count = len(ingredientObjects)
        if not ingredientObjects:
            ingredientObjects = self.soup.find_all("span", class_="recipe-ingred_txt")
            count = len(ingredientObjects) - 3  # 2 spans with "Add all" and 1 empty
        if count < 1:
            raise AllRecipesError(f"[ERROR] Ingredient count: {count}")
        for i in range(count):
            ingredients.append(ingredientObjects[i].text.strip())
        return ingredients

    def getDirections(self):
        directions = []
        directionsString = ""

        # concat all directions to one string
        directionObjects = self.soup.find_all("li", class_="instructions-section-item")
        if directionObjects:
            for li in directionObjects:
                directionsString += " " + li.find("p").text.strip()
        else:
            directionObjects = self.soup.find_all("span", class_="recipe-directions__list--item")
            count = len(directionObjects) - 1  # 1 empty span at end
            for i in range(count):
                directionsString += " " + directionObjects[i].text.strip()

        # use nltk to split direction string into sentences
        individualDirections = nltk.sent_tokenize(directionsString)
        count = len(individualDirections)
        if count < 1:
            raise AllRecipesError(f"[ERROR] Direction count: {count}")
        for i in range(count):
            direction = {}
            direction["step"] = i + 1
            direction["direction"] = individualDirections[i].strip()
            directions.append(direction)

        return directions
