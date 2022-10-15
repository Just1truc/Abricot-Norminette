import os
import re

def abricotize(filename: str) -> None:
    filecontent = None
    try:
        with open("sources/%s" % filename, 'r') as f:
            filecontent = f.read()
    except IOError:
        print("Cannot open file: {}".format(filename))
        exit(1)
    
    if filecontent is None:
        print("File is empty")
        exit(1)
    
    functions = [f for f in filecontent.splitlines() if f.startswith("def check_")]
    first_function = functions[0]
    first_function_name = first_function.split(" ")[1].split("(")[0]
    filecontent = filecontent.replace("import vera", "import abricot")
    filecontent = filecontent.replace(first_function, "def checker(config):")
    filecontent = filecontent.replace("%s()" % first_function_name, "")
    filecontent = filecontent.replace("vera.getSourceFileNames()", "abricot.getSourceFileNames(config)")
    filecontent = filecontent.replace("vera.", "abricot.")
    filecontent = re.sub(r'(INFO|MINOR|MAJOR)\:C\-', "", filecontent)

    with open("destination/%s" % filename.replace("-", "_"), 'w') as f:
        f.write(filecontent)

def get_banana_rules():
    print("remove sources")
    os.system("rm -rf sources")
    print("create sources")
    os.system("mkdir sources")
    print("clone banana coding style checker")
    os.system("git clone git@github.com:Epitech/banana-coding-style-checker.git")
    print("move banana coding style checker to sources")
    os.system("cp banana-coding-style-checker/vera/rules/*.py sources")
    print("remove banana coding style checker")
    os.system("rm -rf banana-coding-style-checker")
    print("Done getting banana rules")

def main():
    get_banana_rules()
    os.system("rm -rf destination")
    os.system("mkdir destination")
    for (dirpath, dirnames, filenames) in os.walk("sources"):
        for filename in filenames:
            if filename.endswith(".py"):
                abricotize(filename)

main()

    