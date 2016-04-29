# Enter an API Key in the api_keys list as a string
api_keys = []


keys_len = len(api_keys)


def get_api_key(seed):
    index = seed % keys_len
    return api_keys[index]
