
from parser import ParserError
import argparse
import mysql.connector
import random
import sys
import time

sys.path.append('sites')
from allrecipes import AllRecipes

argparser = argparse.ArgumentParser()
argparser.add_argument("--checkpoint", type=int, default=6663)
args = argparser.parse_args()

db = mysql.connector.connect(host="localhost", user="root", passwd="root", db="recipes")

random.seed()


print("=============== [Allrecipes] ===============")
for recipeId in range(args.checkpoint, 27000):
    print(f"Processing {recipeId}...  ", end='')
    try:
        allRecipesItem = AllRecipes(recipeId)
    except ParserError as e:
        print(str(e))
        time.sleep(random.randint(10, 60))
        continue
    allRecipesItem.store(database=db)
    db.commit()
    print("done.")
    time.sleep(random.randint(10, 60))
