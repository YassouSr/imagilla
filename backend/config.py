import os
from django.conf import settings

IMG_SHAPE = (224, 224, 3)

FEATS_DIM = 512

No_SISTERS = 96

CLASSES = ["Bread", "Dairy product", "Dessert", 
           "Egg",   "Fried food",    "Meat", 
           "Noodles-Pasta", "Rice",  "Seafood", 
           "Soup",  "Vegetable-Fruit"
          ]

FEATURES = ["bread_filenames.joblib",  "dairy_filenames.joblib",     "dessert_filenames.joblib", 
           "egg_filenames.joblib",    "friedfood_filenames.joblib", "meat_filenames.joblib",
           "pasta_filenames.joblib",  "rice_filenames.joblib",      "seafood_filenames.joblib",   
           "soup_filenames.joblib",   "fruit_filenames.joblib"]

INDEXES = ["breadIndex.ann",  "dairyIndex.ann",     "dessertIndex.ann", 
           "eggIndex.ann",    "friedfoodIndex.ann", "meatIndex.ann",
           "pastaIndex.ann",  "riceIndex.ann",      "seafoodIndex.ann",   
           "soupIndex.ann",   "fruitIndex.ann"]

DATAPATH = "https://res.cloudinary.com/imagesearchv1/image/upload/w_400,h_400/"

WEIGHTS_PATH = os.path.sep.join([settings.BASE_DIR, "models", "weights.h5"])

FEATURES_PATH  = os.path.sep.join([settings.BASE_DIR, "models"])

INDEX_PATH  = os.path.sep.join([settings.BASE_DIR, "models"])
