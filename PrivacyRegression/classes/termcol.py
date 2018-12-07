import numpy as np

class termcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class utils:
    def ParseToFile(List, destination):
        """Parses List to destination file (one element per line)"""
        file = open(destination, "w")
        for element in np.nditer(List):
            #file = file / 10^7
            file.write(str(np.round(element, 2))+'\n')
        file.close
        
