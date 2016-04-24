
api_keys = ['AIzaSyDTsEj1fyHnK0ZuKUE-4ibcsLn3--dIOqQ', 'AIzaSyDPxsz5WxM_rqmM6ROL97Gthf48qEk5rs0', 'AIzaSyCA05mXImoTbKc_wB9ruDZlJbn4_6FuyA8']


keys_len = len(api_keys)


def get_api_key(seed):
    index = seed % keys_len
    return api_keys[index]