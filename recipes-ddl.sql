CREATE DATABASE recipes;
USE recipes;

DROP TABLE Recipe;
DROP TABLE RecipeImages;
DROP TABLE Ingredients;
DROP TABLE RecipeIngredients;
DROP TABLE Directions;

CREATE TABLE Recipe(
    recipe_id INT NOT NULL UNIQUE KEY AUTO_INCREMENT,
    name VARCHAR(300) NOT NULL PRIMARY KEY,
    source VARCHAR(300),
    url VARCHAR(300)
);

CREATE TABLE RecipeImages(
    recipe_id INT,
    url VARCHAR(300) NOT NULL
);

CREATE TABLE Ingredients(
    ingredient_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(300) NOT NULL UNIQUE KEY
);

CREATE TABLE RecipeIngredients(
    recipe_id INT NOT NULL,
    ingredient_id INT NOT NULL
);

CREATE TABLE Directions(
    recipe_id INT NOT NULL,
    step INT NOT NULL,
    direction VARCHAR(500) NOT NULL
);
