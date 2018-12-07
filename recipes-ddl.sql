CREATE DATABASE recipes;
USE recipes;

CREATE TABLE Recipe(
    recipe_id INT NOT NULL UNIQUE KEY AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL PRIMARY KEY,
    source VARCHAR(30),
    source_url VARCHAR(100),
    calories INT,
    servings INT
);

CREATE TABLE RecipeImages(
    recipe_id INT,
    url VARCHAR(100) NOT NULL
);

CREATE TABLE Ingredients(
    ingredient_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL UNIQUE KEY,
    tags VARCHAR(200)
);

CREATE TABLE RecipeIngredients(
    recipe_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    amount FLOAT,
    unit VARCHAR(10),
    extra_descriptions VARCHAR(100)
);

CREATE TABLE Directions(
    recipe_id INT NOT NULL PRIMARY KEY,
    direction VARCHAR(500) NOT NULL,
    step INT NOT NULL
);
