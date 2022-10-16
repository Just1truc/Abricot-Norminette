
class log_service:

    """ Log service """

    def __init__(self, save : True | False = False):
        self.base : str = "[Abricot]"
        self.line_number : int = 0
        self.log_trace = []
        self.save_logs = save

    def register_log(self, string : str) -> str:
        """ Add new generated log """
        if self.save_logs:
            self.log_trace.append(string)
        self.line_number += 1
        return string

    def gen_log(self, lvl, text):
        """ Generate log with intensity lvl """
        return self.register_log(f'{self.line_number} - {self.base} | ({lvl}) | {text}')

    def warning(self, text):
        """ Generate warning lvl log """
        return self.gen_log("WARNING", text)

    def error(self, text):
        """ Generate error lvl log """
        return self.gen_log("ERROR", text)

    def info(self, text):
        """ Generate info lvl log """
        return self.gen_log("INFO", text)

    def success(self, text):
        """ Generate success lvl log """
        return self.gen_log("SUCCESS", text)