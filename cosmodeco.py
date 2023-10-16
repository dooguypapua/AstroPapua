'''
 𝗔𝘀𝘁𝗿𝗼𝗣𝗮𝗽𝘂𝗮
 ---------------------------------------------------
| -*- coding: utf-8 -*-                             |
| title            : cosmodeco.py                   |
| description      : python decorators              |
| author           : dooguypapua                    |
| lastmodification : 20230923                       |
| version          : haumea (v0.9)                  |
| python_version   : 3.8.5                          |
 ---------------------------------------------------
'''
import sys
import os
import functools
import inspect
import time
import cProfile
import tracemalloc
import psutil
import univar
from numpy import mean
from galaxim import grootHead
import groot


'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                        MAIN ASTROPAPUA DECORATOR                                      
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''
def hal9000(func):
    '''
    DESCRIPTION
        The grand Architect
    UPDATE
        10/04/23
    COMMENT
    '''    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Type checking
        expected_types = func.__annotations__
        type_error_value = []
        for arg_name, arg_value in kwargs.items():
            arg_typeName = type(arg_value).__name__
            expected_type = expected_types.get(arg_name)
            if expected_type and not isinstance(arg_value, expected_type):
                type_error_value.append(f"{arg_name}: required '{expected_types.get(arg_name).__name__}' but found '{arg_typeName}'")
        # Value checking
        value_error_value = []
        required_params = set(f.name for f in inspect.signature(func).parameters.values() if f.default == f.empty)
        kwargs_params = set(kwargs.keys())
        for param in required_params - kwargs_params:
            value_error_value.append(f"{param} is required")
        # Error handling
        try:
            if len(type_error_value) > 0 or len(value_error_value) > 0:
                error_value = type_error_value + value_error_value
                grootHead("func_error", {'func_name': func.__name__, 'error_type': "bad call", 'error_value': error_value})
            else:
                # Init profiling
                tracemalloc.start()
                pr = cProfile.Profile()
                pr.enable()
                start_time = time.perf_counter()
                if func.__name__ not in univar.astroProfile['dicoProcess']:
                    univar.astroProfile['dicoProcess'][func.__name__] = {}
                processNum = len(univar.astroProfile['dicoProcess'][func.__name__])
                univar.astroProfile['dicoProcess'][func.__name__][processNum] = {
                                                                   'start_time':start_time,
                                                                   'end_time':"",
                                                                   'execution_time':"",
                                                                   'cpu_usage':"",
                                                                   'memory_usage':"",
                                                                   'kwargs':kwargs
                                                                 }
                # Exécuter la fonction
                result = func(*args, **kwargs)
                # Stop profiling
                end_time = time.perf_counter()
                pr.disable()
                tracemalloc.stop()
                # Compute cpu, ram and time
                univar.astroProfile['dicoProcess'][func.__name__][processNum]['execution_time'] = end_time - start_time
                univar.astroProfile['dicoProcess'][func.__name__][processNum]['cpu_usage'] = psutil.cpu_percent()
                univar.astroProfile['dicoProcess'][func.__name__][processNum]['memory_usage'] = psutil.virtual_memory().used / (1024 * 1024)
                # function return
                return result
        except Exception as e:
            groot.errorToGrootHead(func.__name__, e)
    return wrapper
