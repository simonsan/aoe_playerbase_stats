import json
import pickle


def convert_from_json_to_pickle(input_json_path, output_pickle_path):
    with open(input_json_path, encoding="utf8", mode="r") as handle:
        data = json.load(handle)

    with open(output_pickle_path, mode="wb") as handle:
        pickle.dump(data, handle)
