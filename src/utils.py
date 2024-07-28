import json
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

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def read_text_file(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return data

def get_all_txt_files_in_dirs_and_subdirs(dir_path):
    import os
    txt_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files

def write_json_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# read jsonl file function
def read_jsonl_file(file_path):
    # set the default to be the .env file
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data




if __name__ == "__main__":
    # print the content of the file
    print(read_env_file('.env'))