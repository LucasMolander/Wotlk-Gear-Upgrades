import json

class FileUtil(object):

    @staticmethod
    def getJSONContents(filePath):
        print('\nDoing getJSONContents()...\n')
        with open(filePath, 'r') as f:
            return json.loads(f.read())
