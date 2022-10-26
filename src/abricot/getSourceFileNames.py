import os
from program.configuration import Configuration

sourceFiles = None


def getSourceFileNames() -> list[str]:
    return sourceFiles


def prepareGetSourceFileNames(config: Configuration):
    global sourceFiles
    if config.file:
        sourceFiles = [config.file]
        return

    basedir = '.'
    res = []
    if config.dir:
        basedir = config.dir
    # recursiveley get all files in the current directory
    for root, dirs, files in os.walk(basedir):
        if any([direc.startswith('.') for direc in root.split('/')[1:]]):
            continue
        for file in files:
            filename = os.path.join(root, file)
            if filename.startswith('./'):
                filename = filename[2:]
            if filename in config.ignored:
                continue
            res.append(filename)
    sourceFiles = res
