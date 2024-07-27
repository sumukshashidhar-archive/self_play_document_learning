def read_env_file(file_path='.env'):
    # set the default to be the .env file
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key_value = line.split('=', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    config[key] = value
    return config

if __name__ == "__main__":
    # print the content of the file
    print(read_env_file('.env'))