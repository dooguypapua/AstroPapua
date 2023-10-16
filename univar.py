'''
 𝗔𝘀𝘁𝗿𝗼𝗣𝗮𝗽𝘂𝗮
 ---------------------------------------------------
| -*- coding: utf-8 -*-                             |
| title            : univar.py                      |
| description      : globals variables              |
| author           : dooguypapua                    |
| lastmodification : 20230923                       |
| version          : haumea (v0.9)                  |
| python_version   : 3.8.5                          |
 ---------------------------------------------------
'''
import os
import glob
import random
import tempfile
from colour import Color
from time import time
import inspect
from collections import OrderedDict
from wonderwords import RandomWord
import groot



'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                          DISPLAY VARIABLES                                            
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

# ***** Colors theme ***** #
colorProfile = "SublimeVivid"
hexGradientStart = "#fc466b"
hexGradientMiddle = "#9e52b4"
hexGradientEnd = "#3f5efb"
astroRed = "212;64;89"
astroGreen = "95;211;141"
astroOrange = "226;100;65"
astroPurple = "130;72;104"
astroGrey = "200;200;200"
astroMajor = "200;200;200"
astroMinor = "150;150;150"
astroLightGrey = "100;100;100"

# ***** Main gradient ***** #
dicoGradient = {}
colorsLeft = list(Color(hexGradientStart).range_to(Color(hexGradientMiddle),50))
colorsRight = list(Color(hexGradientMiddle).range_to(Color(hexGradientEnd),50))
for color in colorsLeft + colorsRight[1:]:
    rgb = tuple(int(str(color)[1:][i:i+2], 16) for i in (0, 2, 4))
    dicoGradient[len(dicoGradient)] = f"{rgb[0]};{rgb[1]};{rgb[2]}"
firstKrColor = dicoGradient[0]
lastKrColor = dicoGradient[len(dicoGradient)-1]

# ***** Space Invaders ***** #
dicoInvader = {
               'ufo':["       ▄▄       ",
                      "    ▄▄████▄▄    ",
                      "  ▄██████████▄  ",
                      "▄██▄██▄██▄██▄██▄",
                      "  ▀█▀  ▀▀  ▀█▀  "],
               'crab':["  ▀▄   ▄▀  ",
                       " ▄█▀███▀█▄ ",
                       "█▀███████▀█",
                       "█ █▀▀▀▀▀█ █",
                       "   ▀▀ ▀▀   "],
               'octopus':[" ▄▄████▄▄  ",
                          "██████████ ",
                          "██▄▄██▄▄██ ",
                          " ▄▀▄▀▀▄▀▄  ",
                          "▀        ▀ "],
               'squid':["   ▄██▄    ",
                        " ▄██████▄  ",
                        "███▄██▄███ ",
                        "  ▄▀▄▄▀▄   ",
                        " ▀ ▀  ▀ ▀  "]
              }

# ***** AstroPapua banner ***** #
banner = ["    \           |                     _ \                                "+dicoInvader['ufo'][0],
         "   _ \     __|  __|   __|  _ \       |   |  _` |  __ \   |   |   _` |    "+dicoInvader['ufo'][1],
         "  ___ \  \__ \  |    |    (   |      ___/  (   |  |   |  |   |  (   |    "+dicoInvader['ufo'][2],
         "_/    _\ ____/ \__| _|   \___/      _|    \__,_|  .__/  \__,_| \__,_|    "+dicoInvader['ufo'][3],
         "                                                 _|                      "+dicoInvader['ufo'][4]]

# ***** tqdm pbar format *****#
barFormat = "\x1b[1;38;2;"+firstKrColor+"m|\x1b[0m"
barFormat += "\x1b[1;38;2;"+astroMajor+"m{percentage: 3.0f}%|{bar}| {n_fmt}/{total_fmt} {desc}  \x1b[0m"
barFormat += "\x1b[1;38;2;"+lastKrColor+"m|\x1b[0m"


'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                          INTERNAL VARIABLES                                            
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

# ***** Versioning *****#
version = "haumea (v0.9)"

# ***** Profiling ***** #
# Execution identifier
lstMoons = ["Actaea","Adrastea","Aegaeon","Aegir","Aegis","Aitne","Albiorix","Alexhelios","Alvaldi","Amalthea","Ananke","Angrboda","Anthe","Aoede","Arche","Ariel","Atlas","Autonoe","Bebhionn","Beli","Belinda","Bergelmir","Bestla","Bianca","Caliban","Callirrhoe","Callisto","Calypso","Carme","Carpo","Chaldene","Charon","Cleoselene","Cordelia","Cressida","Cupid","Cyllene","Dactyl","Daphnis","Deimos","Desdemona","Despina","Dia","Dimorphos","Dione","Dysnomia","Eggther","Eirene","Elara","Enceladus","Epimetheus","Erinome","Erriapus","Ersa","Euanthe","Eukelade","Eupheme","Euporie","Europa","Eurydome","Farbauti","Fenrir","Ferdinand","Fornjot","Francisco","Galatea","Ganymede","Geirrod","Gerd","Gorgoneion","Greip","Gridr","Gunnlod","Halimede","Harpalyke","Hati","Hegemone","Helene","Helike","Hermippe","Herse","Himalia","Hippocamp","Hiaka","Hydra","Hyperion","Hyrrokkin","Iapetus","Ijiraq","Illmare","Io","Iocaste","Isonoe","Janus","Jarnsaxa","Juliet","Jupiter","Jupiter","Kale","Kallichore","Kalyke","Kari","Kerberos","Kiviuq","Kore","Laomedeia","Larissa","Leda","Loge","Lysithea","Mab","Margaret","Megaclite","Methone","Metis","Mimas","Miranda","Mneme","Moon","Mundilfari","Naiad","Namaka","Narvi","Nereid","Neso","Nix","Oberon","Ophelia","Orthosie","Paaliaq","Pallene","Pan","Pandia","Pandora","Pasiphae","Pasithee","Peggy","Perdita","Philophrosyne","Phobos","Phoebe","Polydeuces","Portia","Praxidike","Prometheus","Prospero","Proteus","Psamathe","Puck","Remus","Rhea","Romulus","Rosalind","Sao","Setebos","Siarnaq","Sinope","Skamandrios","Skathi","Skoll","Skrymir","Sponde","Squannit","Stephano","Styx","Surtur","Suttungr","Sycorax","Tarqeq","Tarvos","Taygete","Telesto","Tethys","Thalassa","Thebe","Thelxinoe","Themisto","Thiazzi","Thrymr","Thyone","Titan","Titania","Trinculo","Triton","Umbriel","Valetudo","Vanth","Weywot","Xiangliu","Ymir"]
moon = random.choice(lstMoons).lower()
r = RandomWord()
adjective = r.word(include_parts_of_speech=["adjectives"],word_min_length=3, word_max_length=8, regex="[a-z]+")
uuid = "AP_"+adjective+"_"+moon
# Profile dictionnary
astroProfile = { 'main_start':time(), 'end':-1, 'dicoProcess':{} }

# ***** Paths *****#
srcDir = os.path.dirname(os.path.abspath(__file__))
tmpDir = tempfile.gettempdir()+"/"+uuid
os.makedirs(tmpDir)

# ***** Main AstroPapua functions dictionnary ***** #
dicoAstroFunc = {}
for script in glob.glob(srcDir + "/*.py"):
    script_name = os.path.basename(script).replace(".py", "")
    if script_name not in ["astropapua", "univar", "cosmodeco", "galaxim", "groot"]:
        dicoAstroFunc[script_name] = OrderedDict()
        module = __import__(script_name)
        # module attributes
        all_attributes = dir(module)
        # Browse functions
        function_names = [attr for attr in all_attributes if inspect.isfunction(getattr(module, attr)) and attr != "profile"]
        for function_name in function_names:
            if function_name not in ['hyperdrive']:
                dicoAstroFunc[script_name][function_name] = {'descr':"", 'update':"", 'comment':"", 'dicoArgs':OrderedDict(), 'dicoRun':OrderedDict()}
                objFct = getattr(module, function_name)
                # Don t consider function without decorator
                if groot.has_decorator(objFct) is True:
                    # get function doc
                    for line in inspect.getdoc(objFct).splitlines():
                        if "DESCRIPTION" in line:
                            prevField = "descr"
                        elif "UPDATE" in line:
                            prevField = "update"
                        elif "COMMENT" in line:
                            prevField = "comment"
                        else:
                            if dicoAstroFunc[script_name][function_name][prevField] == "":
                                dicoAstroFunc[script_name][function_name][prevField] += line.lstrip()
                            else:
                                dicoAstroFunc[script_name][function_name][prevField] += "\n"+line.lstrip()
                    ordDictSignature = inspect.signature(objFct).parameters
                    for argName in ordDictSignature:
                        if argName == "callerName":
                            continue
                        dicoAstroFunc[script_name][function_name]['dicoArgs'][argName] = {}
                        dicoAstroFunc[script_name][function_name]['dicoRun'][argName] = ""
                        dicoAstroFunc[script_name][function_name]['dicoArgs'][argName]['argType'] = str(ordDictSignature[argName]).split(": ")[1].split(" = ")[0]
                        try:
                            dicoAstroFunc[script_name][function_name]['dicoArgs'][argName]['argDefault'] = str(ordDictSignature[argName]).split(": ")[1].split(" = ")[1].replace("'", "").replace("\"", "")
                            # Apply type
                            if dicoAstroFunc[script_name][function_name]['dicoArgs'][argName]['argType'] == "":
                                dicoAstroFunc[script_name][function_name]['dicoRun'][argName] = str(ordDictSignature[argName]).split(": ")[1].split(" = ")[1].replace("'", "").replace("\"", "")
                            elif dicoAstroFunc[script_name][function_name]['dicoArgs'][argName]['argType'] == "int":
                                dicoAstroFunc[script_name][function_name]['dicoRun'][argName] = int(str(ordDictSignature[argName]).split(": ")[1].split(" = ")[1].replace("'", "").replace("\"", ""))
                            elif dicoAstroFunc[script_name][function_name]['dicoArgs'][argName]['argType'] == "float":
                                dicoAstroFunc[script_name][function_name]['dicoRun'][argName] = float(str(ordDictSignature[argName]).split(": ")[1].split(" = ")[1].replace("'", "").replace("\"", ""))
                            # Boolean type
                            elif dicoAstroFunc[script_name][function_name]['dicoArgs'][argName]['argType'] == "bool":
                                if str(ordDictSignature[argName]).split(": ")[1].split(" = ")[1].lower() == "true":
                                    dicoAstroFunc[script_name][function_name]['dicoRun'][argName] = True
                                elif str(ordDictSignature[argName]).split(": ")[1].split(" = ")[1].lower() == "false":
                                    dicoAstroFunc[script_name][function_name]['dicoRun'][argName] = False
                        except IndexError:
                            pass
