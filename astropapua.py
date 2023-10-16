'''
 𝗔𝘀𝘁𝗿𝗼𝗣𝗮𝗽𝘂𝗮
 ---------------------------------------------------
| -*- coding: utf-8 -*-                             |
| title            : astropapua.py                  |
| description      : galactic hub                   |
| author           : dooguypapua                    |
| lastmodification : 20230923                       |
| version          : haumea (v0.9)                  |
| python_version   : 3.8.5                          |
 ---------------------------------------------------
'''
import sys
import shutil
import univar
import groot
import galaxim


'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                          DISPLAY AND CHECK                                                                                       
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

# ***** Display title and help (if required) ***** #
galaxim.displayTitle()
# No args => display functions list
if len(sys.argv) < 2 or sys.argv[1] in ["-h", "-help", "--help"]:
    galaxim.displayFunctionsList()

# ***** Check function name and correspunding module ***** #
runModule = ""
runFct = sys.argv[1]
for moduleName in univar.dicoAstroFunc:
    if runFct in univar.dicoAstroFunc[moduleName]:
        runModule = moduleName
        break
# Error: Undefined function
if runModule == "":
    galaxim.grootHead("func_error", {'func_name': runFct, 'error_type': "bad call", 'error_value': ["Undefined function"]})

# ***** Display function usag ***** #
if len(sys.argv) < 3 or len(set(["-h", "-help", "--help"]) & set(sys.argv)) > 0:
    galaxim.displayFunctionUsage(runModule, runFct)


'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                          ASTROPAPUA LAUNCHER                                          
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

# ***** Retrieve function parameters ***** #
for i in range(2,len(sys.argv),1):
    try: 
        argName = sys.argv[i].split("=")[0]
        argValue = sys.argv[i].split("=")[1]
        argType = univar.dicoAstroFunc[runModule][runFct]['dicoArgs'][argName]['argType']
        # Apply type
        if argType == "str":
            argValue = str(argValue)
        elif argType == "int":
            argValue = int(argValue)
        elif argType == "float":
            argValue = float(argValue)
        # Boolean type
        elif argType == "bool":
            if argValue.lower() == "true":
                argValue = True
            elif argValue.lower() == "false":
                argValue= False
        univar.dicoAstroFunc[runModule][runFct]['dicoRun'][argName] = argValue
    except IndexError:
        galaxim.grootHead("func_error", {'func_name': runFct, 'error_type': "bad call", 'error_value': ["Malformed CLI argument \""+sys.argv[i]+"\""]})                
    except KeyError:
        galaxim.grootHead("func_error", {'func_name': runFct, 'error_type': "bad call", 'error_value': [argName+" parameter is unkwown"]})

# ***** Launch AstroPapua function ***** #
# Module and function
module = __import__(runModule)
function = getattr(module, runFct)
# Display running groot
galaxim.grootHead("launch", univar.dicoAstroFunc[runModule][runFct]['dicoRun'], runModule, runFct)
# Add callerName and remove empty argument
univar.dicoAstroFunc[runModule][runFct]['dicoRun']['callerName'] = "astropapua"
univar.dicoAstroFunc[runModule][runFct]['dicoRun'] = dict((k, v) for k, v in univar.dicoAstroFunc[runModule][runFct]['dicoRun'].items() if v != '')
# Launch function
galaxim.printgradientline("╭───── "+runFct+" "+"─"*(84-len(runFct))+"╮\n", True)
function(**univar.dicoAstroFunc[runModule][runFct]['dicoRun'])
galaxim.printgradientline("╰"+"─"*91+"╯\n", True)


'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                            POSTPROCESSING                                            
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

# ***** Display groot finish status ***** #
galaxim.grootHead("finish", univar.astroProfile['dicoProcess'], runModule, runFct)

# ***** Save execution profile to a file ***** #
groot.saveProfile(univar.astroProfile['dicoProcess'], "/tmp/profile.tsv")

# ***** Remove temporary folder ***** #
try:
    shutil.rmtree(univar.tmpDir)
except FileNotFoundError:
    pass