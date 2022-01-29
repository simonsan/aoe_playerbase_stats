import json
import lzma
import pickle


def convert_from_json_to_pickle(input_json_path, output_pickle_path):
    with open(input_json_path, encoding="utf8", mode="r") as handle:
        data = json.load(handle)

    with open(output_pickle_path, mode="wb") as handle:
        pickle.dump(data, handle)


def compress_pickle(input_path, output_path):
    with open(input_path, mode="rb") as handle:
        # We are aware of Pickle security implications
        data = pickle.load(handle)  # nosec

    with lzma.open(output_path, mode="wb") as handle:
        pickle.dump(data, handle)
