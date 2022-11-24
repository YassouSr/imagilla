import os
import joblib
import requests
import io
import numpy as np
from PIL import Image
from . import config

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

from tensorflow.keras.applications.vgg16 import preprocess_input, VGG16
from tensorflow.keras.layers import Dropout, Flatten, Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD

from annoy import AnnoyIndex


class ReverseSearch:
    def __init__(self):
        self.baseModel = VGG16(weights="imagenet", include_top=False, input_tensor=Input(shape=config.IMG_SHAPE), pooling="max")

    
    def create_model(self, img_shape, base):
        headModel = base.output
        headModel = Flatten(name="flatten")(headModel)
        headModel = Dense(512, activation="relu")(headModel)
        headModel = Dropout(0.5)(headModel)
        headModel = Dense(len(config.CLASSES), activation="softmax")(headModel)
        model = Model(inputs=base.input, outputs=headModel)
        opt = SGD(lr=1e-4, momentum=0.9)
        model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
        return model
    
    def prepare_image(self, memory):
        if memory.mode != "RGB":
            memory = memory.convert("RGB")
        image = memory.resize((config.IMG_SHAPE[0], config.IMG_SHAPE[1]), Image.NEAREST)
        image = np.expand_dims(np.array(image), axis=0)
        image = preprocess_input(image)
        return image
    
    def prepare_image_through_url(self, url):
        res = requests.get(url)
        image = Image.open(io.BytesIO(res.content))
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = image.resize((config.IMG_SHAPE[0], config.IMG_SHAPE[1]), Image.NEAREST)
        image = np.expand_dims(np.array(image), axis=0)
        image = preprocess_input(image)
        return image
    
    def predict_class(self, prepared_img, shape, model, classes):
        preds = model.predict(prepared_img)[0]
        highest_prob = np.argmax(preds)
        label = classes[highest_prob]
        return label, preds[highest_prob]*100

    def extractor_query(self, prepared_img, model):
        feat  = model.predict(prepared_img)
        feat  = np.array(feat)
        feat = np.array(feat.flatten())
        return np.expand_dims(feat, axis=0)
    
    def search_sisters(self, prepared_img):
        model = self.create_model(config.IMG_SHAPE, self.baseModel)
        model.load_weights(config.WEIGHTS_PATH)
        label   = self.predict_class(prepared_img, config.IMG_SHAPE, model, config.CLASSES)
        feat = self.extractor_query(prepared_img, self.baseModel)
        
        # load the index based on image label
        index_name = config.INDEXES[config.CLASSES.index(label[0])]
        index_path = os.path.join(config.INDEX_PATH ,index_name)
        index = AnnoyIndex(config.FEATS_DIM, metric='euclidean')
        index.load(index_path, prefault=False) 
        
        # get index of similar images to query image
        neigh = index.get_nns_by_vector(feat[0], config.No_SISTERS)
        
        # load query sisters names 
        feat_name = os.path.join(config.FEATURES_PATH , config.FEATURES[config.CLASSES.index(label[0])])
        img_names = joblib.load(feat_name)
        full_url  = os.path.join(config.DATAPATH ,label[0])
        
        results = []
        
        for img_index in neigh:
            results.append(os.path.sep.join([full_url, img_names[img_index]]))
            
        return label[0], np.array(results).reshape(8,12)
