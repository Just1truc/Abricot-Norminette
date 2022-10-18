import json
from textwrap import indent
from program.profile import rules
from program.print import printc, Colors

SEVERITIES_STRING = {
    1: "INFO",
    2: "MINOR",
    3: "MAJOR"
}

SEVERITIES_COLORS = {
    "INFO": Colors.CYAN,
    "MINOR": Colors.YELLOW,
    "MAJOR": Colors.RED
}


class OutputManager():
    def __init__(self, output):
        self.output = output
        self.result = []
        self.summary = {
            "INFO": 0,
            "MINOR": 0,
            "MAJOR": 0
        }

    def groupBy(self, type):
        self.result = []
        for rule in self.output:
            files = self.output[rule]
            ruleData = rules[rule]
            if (type == "file"):
                self.groupByFile(ruleData, files)
            elif (type == "type"):
                self.groupByType(ruleData, files)

    def groupByFile(self, ruleData, files):
        severity = SEVERITIES_STRING[ruleData.severity.value]
        for file in files:
            self.summary[severity] += 1
            try:
                index = next(i for i, item in enumerate(
                    self.result) if item["group"] == file[0])
            except:
                self.result.append({
                    "title": "‣ In File %s" % file[0],
                    "group": file[0],
                    "meta": {
                        "file": file[0]
                    },
                    "errors": []
                })
                index = len(self.result) - 1
            self.result[index]["errors"].append({
                "file": file[0],
                "line": file[1],
                "code": ruleData.code,
                "message": ruleData.description,
                "severity": severity
            })

    def groupByType(self, ruleData, files):
        severity = SEVERITIES_STRING[ruleData.severity.value]
        self.result.append({
            "title": "‣ [%s] %s" % (ruleData.code, ruleData.name),
            "group": ruleData.code,
            "meta": {
                "code": ruleData.code,
                "name": ruleData.name,
                "message": ruleData.description,
                "severity": severity
            },
            "errors": []
        })
        index = len(self.result) - 1
        for file in files:
            self.summary[severity] += 1
            self.result[index]["errors"].append({
                "file": file[0],
                "line": file[1],
                "code": ruleData.code,
                "message": ruleData.description,
                "severity": severity
            })

    def printRuleViolation(self, error, plain=False):
        if plain:
            print("[%s] (%s) - %s. (%s:%d)" % (error["severity"],
                  error["code"], error["message"], error["file"], error["line"]))
        else:
            print("   ", end="")
            printc("[%s] (%s)" % (error["severity"], error["code"]),
                   color=SEVERITIES_COLORS[error["severity"]], bold=True, end=" ")
            print("- %s." % error["message"], end=" ")
            printc("(%s:%d)" %
                   (error["file"], error["line"]), color=Colors.GREY)

    def printSummary(self, plain=False):
        printc("Here's your report:", bold=(not plain))
        if plain:
            print("[MAJOR] : %d" % (self.summary["MAJOR"]), end=" | ")
            print("[MINOR] : %d" % (self.summary["MINOR"]), end=" | ")
            print("[INFO] : %d" % (self.summary["INFO"]))
        else:
            printc("[MAJOR]", color=SEVERITIES_COLORS["MAJOR"],
                   bold=True, end=" : ")
            printc("%d" % self.summary["MAJOR"], end=" | ")
            printc("[MINOR]", color=SEVERITIES_COLORS["MINOR"],
                   bold=True, end=" : ")
            printc("%d" % self.summary["MINOR"], end=" | ")
            printc("[INFO]", color=SEVERITIES_COLORS["INFO"],
                   bold=True, end=" : ")
            printc("%d" % self.summary["INFO"])

    def outputDefault(self, plain=False):
        if (len(self.result) == 0):
            printc("No Coding style error detected : Code clean", color=(Colors.NONE if plain else Colors.GREEN), bold=(not plain))
            return
        for step in self.result:
            printc(step["title"], bold=(not plain))
            for error in step["errors"]:
                self.printRuleViolation(error, plain=plain)
            print("")
        self.printSummary(plain=plain)

    def outputJson(self):
        print(json.dumps(self.result, indent=4))

    def outputCSV(self):
        print("severity,error,file,line")
        for group in self.result:
            for error in group["errors"]:
                print("%s,%s,%s,%d" % (
                    error["severity"], error["code"], error["file"], error["line"]))

    def showAs(self, type):
        if (type == "default"):
            return self.outputDefault()
        if (type == "json"):
            return self.outputJson()
        if (type == "csv"):
            return self.outputCSV()
        if (type == "plain"):
            return self.outputDefault(plain=True)
