
import argparse
import mysql.connector
import logging
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

handler = logging.handlers.WatchedFileHandler('crawler.log')
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel('INFO')
logger.addHandler(handler)

print("=============== [Allrecipes] ===============")
for recipeId in range(args.checkpoint, 27000):
    logging.info(f"Processing {recipeId}...  ", end='')
    try:
        allRecipesItem = AllRecipes(recipeId)
        allRecipesItem.store(database=db)
        db.commit()
        logging.info("done.")
        time.sleep(random.randint(10, 60))
    except Exception as e:
        logging.error(str(e))
        time.sleep(random.randint(10, 60))
        continue
