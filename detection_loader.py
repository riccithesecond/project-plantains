import os

def load_detections(path):
    rules = []
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(('.yaml', '.yml')):
                rules.append({'name': file})
    return rules