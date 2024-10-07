import pandas as pd
import yaml


def load_config_file(path):
    stream = open(path, 'r')
    dictionary = yaml.safe_load(stream) 
    stream.close()
    return dictionary


stream = open("config.yaml", 'wr')
dictionary = yaml.safe_load(stream) 
stream.close()
rawDataPath = dictionary["data"]

data = pd.read_csv(rawDataPath)
print(data["label"])