
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.metrics import accuracy_score
import pickle
import os


class BaseModel:

    def __init__(self):
        pass

    @classmethod
    def from_file(cls, filename):
        """
        Load a model from a file
        """
        if not os.path.exists(filename):
            print("[!] Load model: File {} doesn't exist!".format(filename))
            return None

        with open(filename, "rb") as modelbuffer:
            model = pickle.load(modelbuffer)
            return model

    def save(model, filename, overwrite=True):
        """
        Save the model to a specified filename
        """
        if os.path.exists(filename):
            if overwrite:
                print("... Overwriting {}".format(filename))
            else:
                print("[!] File {} exists, model not written!".format(filename))

        with open(filename, "wb") as modelbuffer:
            pickle.dump(model, modelbuffer)


class LinearModel(BaseModel, LogisticRegression):

    def __init__(self):
        pass
