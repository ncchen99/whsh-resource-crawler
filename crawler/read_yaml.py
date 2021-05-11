import yaml


def get_request_urls(file):
    with open(file, "r") as stream:
        data = yaml.load(stream, Loader=yaml.FullLoader)
    return data
