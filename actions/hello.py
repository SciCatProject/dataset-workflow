import os


def main(_dict):
    if 'name' in _dict:
        name = _dict['name']
    else:
        name = "stranger"
    greeting = "Hello " + name + "! From OpenWhisk " + os.getcwd()
    print(greeting)
    return {"greeting": greeting}
