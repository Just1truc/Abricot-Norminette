import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: fruitmixer.py <file>")
        sys.exit(1)
    filename = sys.argv[1]
    filecontent = None
    try:
        with open(filename, 'r') as f:
            filecontent = f.read()
    except IOError:
        print("Cannot open file: {}".format(filename))
        sys.exit(1)
    
    if filecontent is None:
        print("File is empty")
        sys.exit(1)
    
    functions = [f for f in filecontent.splitlines() if f.startswith("def check_")]
    first_function = functions[0]
    first_function_name = first_function.split(" ")[1].split("(")[0]
    filecontent = filecontent.replace(first_function, "def checker():")
    filecontent = filecontent.replace("%s()" % first_function_name, "")
    filecontent = filecontent.replace("vera.report", "abricot.report")
    print(filecontent)

main()

    