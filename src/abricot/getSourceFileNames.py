import os
from program.configuration import Configuration

def getSourceFileNames(config: Configuration) -> list[str]:
    if config.file:
        return [config.file]
    
    basedir = '.'
    res = []
    if config.dir:
        basedir = config.dir 
    # recursiveley get all files in the current directory
    for root, dirs, files in os.walk(basedir):
        for file in files:
            filename = os.path.join(root, file)
            if filename.startswith('./'):
                filename = filename[2:]
            if filename in config.ignored:
                continue
            res.append(filename)
    return res