import os
import re

def abricotize(filename: str) -> None:
    filecontent = None
    try:
        with open("/tmp/fruitmixer/sources/%s" % filename, 'r') as f:
            filecontent = f.read()
    except IOError:
        print("Cannot open file: {}".format(filename))
        exit(1)
    
    if filecontent is None:
        print("File is empty")
        exit(1)
    
    functions_calls = [f for f in filecontent.splitlines() if re.match(r'^\w+\(\)$', f)]
    filecontent = filecontent.replace("import vera", "import abricot")
    res = ""
    for line in filecontent.splitlines():
        if line == functions_calls[0]:
            res += "def checker():\n"
        if line in functions_calls:
            res += "    "
        res += "%s\n" % line
    filecontent = res
    filecontent = filecontent.replace("vera.getSourceFileNames()", "abricot.getSourceFileNames()")
    filecontent = filecontent.replace("vera.", "abricot.")
    filecontent = re.sub(r'(INFO|MINOR|MAJOR)\:C\-', "", filecontent)

    if filename.endswith("C-G3.py"):
        filecontent = filecontent.replace("if not is_source_file(file) and not is_header_file(file):", "if not is_header_file(file):")

    cwd = os.path.dirname(__file__)
    with open("%s/../src/rules/%s" % (cwd, filename.replace("-", "_")), 'w') as f:
        f.write(filecontent)

def get_banana_rules():
    os.system("rm -rf /tmp/fruitmixer")
    os.system("mkdir /tmp/fruitmixer")
    os.system("mkdir /tmp/fruitmixer/sources")
    os.system("git clone git@github.com:Epitech/banana-coding-style-checker.git /tmp/fruitmixer/remote")
    os.system("cp /tmp/fruitmixer/remote/vera/rules/*.py /tmp/fruitmixer/sources")
    os.system("rm -rf /tmp/fruitmixer/remote")

def add_additional_rules():
    cwd = os.path.dirname(__file__)
    os.system("cp %s/../src/additional/*.py %s/../src/rules/" % (cwd, cwd))
    
def main():
    get_banana_rules()
    os.system("mkdir /tmp/fruitmixer/destination")
    for (dirpath, dirnames, filenames) in os.walk("/tmp/fruitmixer/sources"):
        for filename in filenames:
            if filename.endswith(".py"):
                abricotize(filename)
    add_additional_rules()
    os.system("rm -rf /tmp/fruitmixer/")

main()
