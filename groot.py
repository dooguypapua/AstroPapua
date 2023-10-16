'''
 𝗔𝘀𝘁𝗿𝗼𝗣𝗮𝗽𝘂𝗮
 ---------------------------------------------------
| -*- coding: utf-8 -*-                             |
| title            : groot.py                       |
| description      : internal functions             |
| author           : dooguypapua                    |
| lastmodification : 20231004                       |
| version          : haumea (v0.9)                  |
| python_version   : 3.8.5                          |
 ---------------------------------------------------
'''

import os
import sys
import json
import subprocess
import itertools
import gzip
import inspect
import functools
import concurrent.futures
import datetime
import traceback
from tqdm import tqdm
from functools import lru_cache
from operator import itemgetter
import univar
import galaxim


'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                          INTERNAL FUNCTIONS
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

def has_decorator(func):
    '''
    DESCRIPTION
        Check if a function has a decorator
    UPDATE
        10/04/23
    COMMENT
    '''
    members = inspect.getmembers(func)
    # Recherchez l'attribut '__wrapped__' dans les attributs de la fonction
    for name, value in members:
        if name == '__wrapped__':
            return True
    # Si aucun '__wrapped__' n'a été trouvé, la fonction n'a pas de décorateur
    return False


def errorToGrootHead(funcName, e, onlyError = False):
    '''
    DESCRIPTION
        Display a Exception error with Groot head
    UPDATE
        10/04/23
    COMMENT
    '''    
    exc_type, exc_obj, exc_tb = sys.exc_info()
    traceback_details = traceback.extract_tb(sys.exc_info()[2])
    last_trace = traceback_details[-1]
    file_name = last_trace[0]
    error_value = [f"Found in '{last_trace[0]}' line {traceback_details[-1][1]}"]
    error_value.append("")
    error_value.append(str(e))
    if onlyError is True:
        return funcName+"#"+exc_type.__name__+"#"+"#".join(error_value)
    else:
        galaxim.grootHead("func_error", {'func_name': funcName, 'error_type': exc_type.__name__, 'error_value': error_value})


def load_json(pathJSON):
    '''
    DESCRIPTION
        Load a JSON file
    UPDATE
        10/04/23
    COMMENT
    '''
    try:
        if pathJSON.endswith(".gz"):
            with gzip.open(pathJSON, "r") as json_file:
                dico = json.load(json_file)
        else:
            with open(pathJSON, 'r') as json_file:
                dico = json.load(json_file)
        return dico
    except UnicodeDecodeError:
        raise UnicodeDecodeError("\"pathJSON\"Unable to load json file\n\""+pathJSON+"\"")
    except AttributeError:
        raise AttributeError("\"pathJSON\"Unable to load json file\n\""+pathJSON+"\"")


def dump_json(dico, pathJSON, indent=4):
    '''
    DESCRIPTION
        Dump a JSON file
    UPDATE
        10/04/23
    COMMENT
    '''    
    try:
        if pathJSON.endswith(".gz"):
            with gzip.open(pathJSON, "wt") as outfile:
                json.dump(dico, outfile, indent=indent)
        else:
            with open(pathJSON, 'w') as outfile:
                json.dump(dico, outfile, indent=indent)
    except UnicodeDecodeError:
        raise UnicodeDecodeError("\"pathJSON\"Unable to dump json file\n\""+pathJSON+"\"")
    except AttributeError:
        raise AttributeError("\"pathJSON\"Unable to dump json file\n\""+pathJSON+"\"")                


def saveProfile(dicoProfile: dict, pathOUT: str):
    '''
    DESCRIPTION
        Save function profile trace
    UPDATE
        10/04/23
    COMMENT
    '''    
    OUT = open(pathOUT, "w")
    OUT.write("process_num\tfunction\tduration\tcpu (%)\tmemory (Mo)\tkwargs\n")
    cptOrder = 1
    for fctName in dicoProfile:
        for processNum in dicoProfile[fctName]:
            processEntry = dicoProfile[fctName][processNum]
            # Format elapse time
            delta = datetime.timedelta(seconds=processEntry['execution_time'])
            seconds_remaining = delta.seconds
            hours, remainder = divmod(seconds_remaining, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_duration = f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s"
            formatted_ram = str(round((processEntry['memory_usage']), 1)).replace(".", ",")+"Mo"
            OUT.write(str(processNum).zfill(3)+"\t"+fctName+"\t"+str(formatted_duration))
            OUT.write("\t"+str(processEntry['cpu_usage']).replace(".", ",")+"\t"+formatted_ram)
            OUT.write("\t"+str(processEntry['kwargs'])+"\n")
    OUT.close()


def read_file(file_path: str, excludeFirstKr: str = "#"):
    '''
    DESCRIPTION
        Fast file read
    UPDATE
        10/04/23
    COMMENT
    '''    
    if not os.path.isfile(file_path):
        raise FileNotFoundError("Unable to read file\n\""+file_path+"\"")
    lstLines = []
    with open(file_path) as f:
        for line in f:
            if line[0] != excludeFirstKr:
                lstLines.append(line[:-1])
    return lstLines


def cat_lstfiles(lstFiles, pathOUT):
    '''
    DESCRIPTION
        Concatenate files from a path list
    UPDATE
        10/04/23
    COMMENT
    '''    
    lstExistingFiles = []
    for file in lstFiles:
        if os.path.isfile(file):
            lstExistingFiles.append(file)
    os.system("touch "+pathOUT)
    if len(lstFiles) != 0:
        os.system("cp "+lstExistingFiles[0]+" "+pathOUT)
        for i in range(1, len(lstExistingFiles), 1):
            os.system("cat "+lstExistingFiles[i]+" >> "+pathOUT)


def path_converter(pathToConvert):
    '''
    DESCRIPTION
        Convert windows to unix path
    UPDATE
        10/04/23
    COMMENT
    '''    
    if pathToConvert == "":
        return pathToConvert
    elif "\\" in pathToConvert:
        pathConverted = pathToConvert.replace("C:\\", "/mnt/c/").replace("\\", "/")
    else:
        pathConverted = pathToConvert
    if pathConverted[-1] == "/":
        return pathConverted[:-1]
    else:
        return pathConverted


def get_input_files(pathIN, fctName, fileExt=[""], filter=None):
    '''
    DESCRIPTION
        Get input files from file path or folder path, count and pathsize
    UPDATE
        10/04/23
    COMMENT
    '''    
    lstAllFiles = []
    setFiles = set()
    pathIN = path_converter(pathIN)
    if os.path.isfile(pathIN):
        lstAllFiles.append(pathIN)
    elif os.path.isdir(pathIN):
        for file in os.listdir(pathIN):
            lstAllFiles.append(pathIN+"/"+file)
    # Check extension
    for file in lstAllFiles:
        for ext in fileExt:
            if file.endswith(ext) and (filter is None or filter in file):
                setFiles.add(file)
    return list(sorted(setFiles))


def reverse_complement(seq):
    '''
    DESCRIPTION
        Reverse complement a DNA sequence
    UPDATE
        10/04/23
    COMMENT
    '''    
    tab = str.maketrans("ACTGN", "TGACN")
    return seq.translate(tab)[::-1]


def to_ranges(listIN):
    '''
    DESCRIPTION
        Group integer list by range
    UPDATE
        10/04/23
    COMMENT
    '''    
    listIN = sorted(set(listIN))
    for key, group in itertools.groupby(enumerate(listIN),
                                        lambda t: t[1] - t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]


def longest_common_substring(x: str, y: str):
    '''
    DESCRIPTION
        FIND longest substring between two strings
    UPDATE
        10/04/23
    COMMENT
    '''
    # function to find the longest common substring
    # Memorizing with maximum size of the memory as 1
    @lru_cache(maxsize=1)
    # function to find the longest common prefix
    def longest_common_prefix(i: int, j: int) -> int:
        if 0 <= i < len(x) and 0 <= j < len(y) and x[i] == y[j]:
            return 1 + longest_common_prefix(i + 1, j + 1)
        else:
            return 0
    # diagonally computing the subproblems
    # to decrease memory dependency

    def digonal_computation():    
        # upper right triangle of the 2D array
        for k in range(len(x)):
            yield from ((longest_common_prefix(i, j), i, j)
                        for i, j in zip(range(k, -1, -1), range(len(y) - 1, -1, -1)))
        # lower left triangle of the 2D array
        for k in range(len(y)):
            yield from ((longest_common_prefix(i, j), i, j)
                        for i, j in zip(range(k, -1, -1), range(len(x) - 1, -1, -1)))
    # returning the maximum of all the subproblems
    return max(digonal_computation(), key=itemgetter(0), default=(0, 0, 0))


'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                         SUBPROCESS FUNCTIONS
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

def get_cmd_output(cmd):
    '''
    DESCRIPTION
        Read bash command output
    UPDATE
        10/04/23
    COMMENT
    '''    
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    if p_status != 0:
        raise RuntimeError("System command failed\n\""+cmd+"\"")
    else:
        return output.decode().strip()


def scotty(dicoThread):
    '''
    DESCRIPTION
        Parallelize AstroPapua function
    UPDATE
        10/04/23
    COMMENT
    '''
    galaxim.printExecution(f"Construct thread pool","minor","threads")
    # create a thread pool with 12 threads
    astroPool = concurrent.futures.ThreadPoolExecutor(max_workers=12)
    futures = []  # Liste pour stocker les futures
    for key in dicoThread:
        # get module and function
        for script_name in univar.dicoAstroFunc:
            if dicoThread[key]['target'] in univar.dicoAstroFunc[script_name]:
                module = __import__(script_name)
                objFct = getattr(module, dicoThread[key]['target'])
                # update the partial object with the dictionary of arguments
                partial_worker = functools.partial(objFct, **dicoThread[key]['args'])
                # update the wrapper of the partial object
                functools.update_wrapper(partial_worker, objFct)
                # submit tasks to the pool
                future = astroPool.submit(partial_worker)
                futures.append(future)
                break
    galaxim.printExecution(f"Launch thread pool","minor","threads")
    pbar = tqdm(total=len(dicoThread), ncols=93, leave=False, desc="", file=sys.stdout, bar_format=univar.barFormat)
    # Utilisez concurrent.futures.as_completed pour surveiller les tâches terminées
    for completed_future in concurrent.futures.as_completed(futures):
        # update the progress bar
        pbar.update()
        # Récupérez le résultat de la tâche terminée
        result = completed_future.result()
    pbar.close()
    # wait for all tasks to complete
    astroPool.shutdown(wait=True)
    galaxim.printExecution(f"Finish thread pool","minor","threads")
    # return number of error
    setError = set()
    for completed_future in concurrent.futures.as_completed(futures):
        if completed_future.result() != "SUCCESS":
            setError.add(completed_future.result())
    for error in setError:
        galaxim.grootHead("func_error", {'func_name': error.split("#")[0], 'error_type': error.split("#")[1], 'error_value': error.split("#")[2:]}, exitAfter = False)
    if len(setError) > 0:
        exit("\n")
