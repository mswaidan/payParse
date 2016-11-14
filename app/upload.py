import os

uploadFolder = '../tmp'

class  writeFile(file):
    file.save(os.path.join(uploadFolder,file))
