from loguru import logger
import joblib
import time
from datetime import datetime
import json

from sentence_transformers import SentenceTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

GLOBAL_CONFIG = {
    "model": {
        "featurizer": {
            "sentence_transformer_model": "all-mpnet-base-v2",
            "sentence_transformer_embedding_dim": 768,
        },
        "classifier": {"serialized_model_path": "./data/news_classifier.joblib"},
    },
    "service": {"log_destination": "./data/logs.out"},
}


class TransformerFeaturizer(BaseEstimator, TransformerMixin):
    def __init__(self, dim, sentence_transformer_model):
        self.dim = dim
        self.sentence_transformer_model = sentence_transformer_model

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_t = []
        for doc in X:
            X_t.append(self.sentence_transformer_model.encode(doc))
        return X_t


class NewsCategoryClassifier:
    def __init__(self, config: dict) -> None:
        self.config = config
        sentence_transfomer = SentenceTransformer(
            "sentence-transformers/{model}".format(
                model=GLOBAL_CONFIG["model"]["featurizer"]["sentence_transformer_model"]
            )
        )
        dim = GLOBAL_CONFIG["model"]["featurizer"]["sentence_transformer_embedding_dim"]
        featurizer = TransformerFeaturizer(dim, sentence_transfomer)
        model = joblib.load(
            GLOBAL_CONFIG["model"]["classifier"]["serialized_model_path"]
        )
        self.classes = model.classes_

        self.pipeline = Pipeline(
            [("transformer_featurizer", featurizer), ("classifier", model)]
        )

    def predict_proba(self, model_input) -> dict:

        preds = self.pipeline.predict_proba([model_input]).flatten()
        labels = self.classes

        return dict(zip(labels, preds))

    def predict_label(self, model_input) -> str:

        return self.pipeline.predict([model_input])
