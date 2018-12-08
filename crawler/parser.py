from bs4 import BeautifulSoup
import mysql.connector
import socket
import urllib


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, url):
        self.url = url
        self.soup = self.soupify(url)
        self._title = None
        self._source = None
        self._images = None
        self._ingredients = None
        self._directions = None
        self._calories = None

    def soupify(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                return BeautifulSoup(response.read(), "html.parser")
        except urllib.error.HTTPError as e:
            raise ParserError(str(e))
        except urllib.error.URLError as e:
            raise ParserError(str(e))
        except socket.error as e:
            raise ParserError(str(e))

    @property
    def title(self):
        if self._title is None:
            self._title = self.getTitle()
        return self._title

    @property
    def source(self):
        if self._source is None:
            self._source = self.getSource()
        return self._source

    @property
    def images(self):
        if self._images is None:
            self._images = self.getImages()
        return self._images

    @property
    def ingredients(self):
        if self._ingredients is None:
            self._ingredients = self.getIngredients()
        return self._ingredients

    @property
    def directions(self):
        if self._directions is None:
            self._directions = self.getDirections()
        return self._directions

    @property
    def calories(self):
        if self._calories is None:
            self._calories = self.getCalories()
        return self._calories

    def getTitle(self):
        raise NotImplementedError("Must implement getTitle() function.")

    def getSource(self):
        raise NotImplementedError("Must implement getSource() function.")

    def getImages(self):
        raise NotImplementedError("Must implement getImages() function.")

    def getIngredients(self):
        raise NotImplementedError("Must implement getIngredients() function.")

    def getDirections(self):
        raise NotImplementedError("Must implement getDirections() function.")

    def getCalories(self):
        raise NotImplementedError("Must implement getCalories() function.")

    def store(self, database=None, jsonfile=None):
        if database:
            self._storeDB(database)
        elif jsonfile:
            self._storeJSON(jsonfile)

    def _storeDB(self, db):
        cursor = db.cursor()

        # Insert into Recipe and get the auto-incremented recipe_id.
        cursor.execute("INSERT INTO Recipe (name, source, url) VALUES (%s, %s, %s)",
                       (self.title, self.source, self.url))
        cursor.execute("SELECT recipe_id FROM Recipe WHERE name = %s AND source_url = %s",
                       (self.title, self.url))
        recipeId = cursor.fetchall()[0][0]

        # Insert all images for recipe_id
        for image in self.images:
            cursor.execute("INSERT INTO RecipeImages (recipe_id, url) VALUES (%s, %s)",
                           (recipeId, image))

        # Insert all newly discovered raw ingredients
        for ingredient in self.ingredients:
            try:
                cursor.execute(
                    "INSERT INTO Ingredients (name) VALUES (%s)",
                    (ingredient,))
            except mysql.connector.IntegrityError as e:
                if not e.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                    raise
                continue  # We already have this raw ingredient info

        # Establish recipe-ingredients relationship
        for ingredient in self.ingredients:
            cursor.execute("SELECT ingredient_id FROM Ingredients WHERE name = %s", (ingredient,))
            ingredientId = cursor.fetchall()[0][0]
            cursor.execute(
                "INSERT INTO RecipeIngredients (recipe_id, ingredient_id) VALUES (%s, %s)",
                (recipeId, ingredientId))

        # Insert all directions for recipe_id
        for direction in self.directions:
            cursor.execute(
                "INSERT INTO Directions (recipe_id, step, direction) VALUES (%s, %s, %s)",
                (recipeId, direction['step'], direction['direction']))

    def _storeJSON(self, jsonfile):
        pass
