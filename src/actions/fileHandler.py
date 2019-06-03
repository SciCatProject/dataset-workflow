import urllib.request
import shutil


def main(_dict):
    if 'url' in _dict and 'fileName' in _dict:
        url = _dict['url']
        file_name = _dict['fileName']
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        with open(file_name) as file:
            line = file.readline()
            return {"fileName": file_name, "data": line}
    else:
        return {"error": "Either url of filename not provided"}
