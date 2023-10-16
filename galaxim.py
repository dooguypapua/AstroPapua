'''
 𝗔𝘀𝘁𝗿𝗼𝗣𝗮𝗽𝘂𝗮
 ---------------------------------------------------
| -*- coding: utf-8 -*-                             |
| title            : galaxim.py                     |
| description      : display and visuals            |
| author           : dooguypapua                    |
| lastmodification : 20230923                       |
| version          : haumea (v0.9)                  |
| python_version   : 3.8.5                          |
 ---------------------------------------------------
'''
import sys
from typing import Tuple
import univar
import datetime
import time
import random
from rich.console import Console
from rich.syntax import Syntax


'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                          DISPLAY FUNCTIONS
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

def grootHead(boolStatut: str, dicoInfo: dict, runModule: str = "", runFct: str = "", exitAfter: bool = True) -> Tuple[str, dict, str, str, bool]:
    '''
    DESCRIPTION
        Display groot head for 'func_error', 'finish' and 'launch' status
    UPDATE
        10/04/23
    COMMENT
    '''
    if boolStatut == "func_error":
        printgradientline("\n╰"+"─"*91+"╯\n", True)
    printgradientline("╭"+"─"*91+"╮\n", True)
    if boolStatut == "launch":
        colorPos = [1,2,6]
        grootInfos = ["","","="*66,"","","","="*66,""]
        grootInfos[1] = "Prepare for liftoff!".center(66," ")
        grootMouth = "__"
        grootColor = univar.astroOrange
        grootInfos[3] = " @Module    : "+runModule
        grootInfos[4] = " @Function  : "+runFct
        grootInfos[5] = " @Mission   : "+univar.uuid
        grootInfos[7] = " @Parameters: "
        cpt = 8
        argStrLenMax = max(len(key) for key in dicoInfo.keys())+1
        for argName in dicoInfo:
            if argName != "callerName":
                if dicoInfo[argName] == "":
                    grootInfos.append("  "+argName+" ".rjust(argStrLenMax-len(argName))+"=  None")
                else:
                    lstwrapInfo = text_wrapper(" "+str(dicoInfo[argName]), 50, ["/"], "left")
                    shift = len("  "+argName+" ".rjust(argStrLenMax-len(argName))+"= ")
                    grootInfos.append("  "+argName+" ".rjust(argStrLenMax-len(argName))+"= "+lstwrapInfo[0])
                    for wrapInfo in lstwrapInfo[1:]:
                        grootInfos.append(" ".rjust(shift+1)+wrapInfo)
            cpt += 1
    elif boolStatut == "finish":
        colorPos = [1,2]
        grootInfos = ["","","="*66]
        grootInfos[1] = "Mission accomplished!".center(66," ")
        grootMouth = "︶"
        grootColor = univar.astroGreen
        grootInfos.append(" N° |        TITLE        | CALL |     TIME    |  CPU  |  MEM")
        grootInfos.append("------------------------------------------------------------------")
        cptOrder = 1
        for fctName in dicoInfo:
            max_time = max_cpu = max_mem = 0
            for processNum in dicoInfo[fctName]:
                processEntry = dicoInfo[fctName][processNum]
                delta = datetime.timedelta(seconds=processEntry['execution_time'])
                max_time = max(max_time, delta.seconds)
                max_cpu = max(max_cpu,processEntry['cpu_usage'])
                max_mem = max(max_mem,processEntry['memory_usage'])
            # Format time
            hours, remainder = divmod(max_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_duration = f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s"
            # Format memory usage
            if max_mem / 1024 > 1:
                formatted_ram = str(round((max_mem / 1024), 1))+"Go"
            else:
                formatted_ram = str(round((max_mem), 1))+"Mo"
            grootInfos.append(str(cptOrder).zfill(2).center(4)+"|"+fctName.center(21)+"|"+str(len(dicoInfo[fctName])).center(6)+"|"+str(formatted_duration).center(13)+"|"+(str(max_cpu)+"%").center(7)+"|"+formatted_ram.center(9))
            cptOrder += 1
    elif boolStatut == "func_error":
        colorPos = [1,2,6]
        grootInfos = ["","","="*66,"","","","="*66,""]
        grootInfos[1] = "Warp drive malfunction!".center(66," ")
        runModule = ""
        for module in univar.dicoAstroFunc:
            if dicoInfo['func_name'] in univar.dicoAstroFunc[module]:
                runModule = module
        grootInfos[3] = " @Module    : "+runModule    
        grootInfos[4] = " @Function  : "+dicoInfo['func_name']
        grootInfos[5] = " @Category  : "+dicoInfo['error_type']
        cpt = 6
        for line in dicoInfo['error_value']:
            for subline in line.split("\n"):
                subline = subline.replace(univar.srcDir+"/", "")
                wrapInfo = text_wrapper(" "+subline, 50, [""], "left")
                if len(wrapInfo) == 1:
                    grootInfos.append(" "+subline)
                    cpt += 1
                else:
                    for i in range(len(wrapInfo)):
                        if i == 0:
                            grootInfos.append(" "+wrapInfo[i]+"...")
                        else:
                            grootInfos.append("   ..."+wrapInfo[i])
                        cpt += 1
        grootMouth = "︵"
        grootColor = univar.astroRed
    else:
        exit(f"Invalid boolStatut=\"{boolStatut}\". Valid value is \"launch\", \"finish\" or \"error\"")
    grootHeader = [
                   "       .^. .  _         ",
                   "      /: ||`\/ \~  ,    ",
                   "    , [   &    / \ y'   ",
                   "   {v':   `\   / `&~-,  ",
                   "  'y. '    |`   .  ' /  ",
                   "   \   '  .       , y   ",
                   "   v .        '     v   ",
                   "   V  .~.      .~.  V   ",
                   "   : (  0)    (  0) :   ",
                   "    i `'`      `'` j    ",
                   "     i     "+grootMouth+"    ,j     ",
                   "      `%`~....~'&       "
                  ]
    for i in range(max(len(grootInfos),12)):
        if i>=len(grootInfos): grootInfos.append("")
        if i>=len(grootHeader): grootHeader.append(" "*24)
        # Left part = groot
        printcolor("|", 1, univar.firstKrColor, "None", True)
        printcolor(grootHeader[i], 1, grootColor, "None", True)
        # Right part = info
        if i in colorPos:
            printcolor(grootInfos[i], 0, grootColor, "None", True)
            rjust = 92-len(grootHeader[i])-len(grootInfos[i])
        else:
            if "@" in grootInfos[i]:
                printcolor(grootInfos[i].split(":")[0].replace("@", "")+":", 1, univar.astroPurple, "None", True)
                printcolor(grootInfos[i].split(":")[1].replace("@", ""), 0, univar.astroGrey, "None", True)
                rjust = 93-len(grootHeader[i])-len(grootInfos[i])
            else:
                printcolor(grootInfos[i], 0, "150;150;150", "None", True)
                rjust = 92-len(grootHeader[i])-len(grootInfos[i])
        if "︶" in grootHeader[i] or "︵" in grootHeader[i]:
            printcolor("|".rjust(rjust-1)+"\n", 1, univar.lastKrColor, "None", True)
        else:
            printcolor("|".rjust(rjust)+"\n", 1, univar.lastKrColor, "None", True)
    printgradientline("╰"+"─"*91+"╯\n", True)
    if boolStatut == "func_error" and exitAfter is True:
        exit("\n")


def displayTitle():
    '''
    DESCRIPTION
        Display AstroPapua title banner
    UPDATE
        10/04/23
    COMMENT
    '''    
    # Check version name
    if len(univar.version) > 16:
        grootHead("func_error", {'func_name':"displayTitle", 'error_type':"bad argument", 'error_value':["version string length > 16"]})
    # First line
    title = ["╭───────────────────────────────────────────────────────────────────────────────────────────╮"]
    # Banner
    for bannerLine in univar.banner:
        title.append("| "+bannerLine+" |")
    # Create version horizontal line
    if len(univar.version) % 2 == 1:
        leftSignCount = int((18 - len(univar.version)) / 2)
        rightSignCount = leftSignCount - 1
    else:
        leftSignCount = rightSignCount = int((18 - len(univar.version)) / 2) - 1
    versionLine = "╰"+"─"*(73+leftSignCount)+" "+univar.version+" "+"─"*rightSignCount+"╯"
    title.append(versionLine)
    # Display
    print("")
    for titleLine in title:
        for i in range(len(titleLine)):
            printcolor(titleLine[i], 0, univar.dicoGradient[i], "None", True)
        print("")


def displayFunctionsList():
    '''
    DESCRIPTION
        Display AstroPapua function list
    UPDATE
        10/04/23
    COMMENT
    '''    
    invaderName = random.choice([el for el in list(univar.dicoInvader.keys()) if el != "ufo"])
    for script_name in univar.dicoAstroFunc:
        cptLine = 0
        printgradientline("╭"+"─"*91+"╮\n", True)
        printgradientline("| "+script_name.upper()+" ".rjust(90-len(script_name))+"|\n", True)
        printgradientline("|"+"-"*91+"|\n", True)
        for function_name in univar.dicoAstroFunc[script_name]:
            printgradientline("| ", True)
            displayLine = ["''' "+univar.dicoAstroFunc[script_name][function_name]['descr']+" '''"]
            displayLine.append(f"def {function_name}"+"(")
            toDisplay = ""
            for argName in univar.dicoAstroFunc[script_name][function_name]['dicoArgs']:
                toDisplay += f"{argName}: {univar.dicoAstroFunc[script_name][function_name]['dicoArgs'][argName]['argType']}"
                if "argDefault" in univar.dicoAstroFunc[script_name][function_name]['dicoArgs'][argName]:
                    toDisplay += f" = {univar.dicoAstroFunc[script_name][function_name]['dicoArgs'][argName]['argDefault']}"
                toDisplay += ", "
            toDisplay = toDisplay[:-2]+")"
            for subline in text_wrapper(toDisplay, 70, [","]):
                displayLine.append(subline)
            for i in range(len(displayLine)):
                if i == 0:
                    wrapText = displayLine[i]
                elif i == 1:
                    printgradientline("| ", True)
                    wrapText = displayLine[i]
                else:
                    printgradientline("| ", True)
                    wrapText = "    "+displayLine[i]
                syntax = Syntax(wrapText, "python", theme="native", background_color="default")
                console = Console(width=100000)
                console.print(syntax, end="")
                print(f"\033[F\033[{len(wrapText)+2}C", end=" ")
                print(" ".rjust(74-len(wrapText)), end=" ")
                try:
                    for j in range(len(univar.dicoInvader[invaderName][cptLine])):
                        printcolor(univar.dicoInvader[invaderName][cptLine][j], 0, univar.astroLightGrey, "None", True)
                except IndexError:
                    printcolor(" "*len(univar.dicoInvader[invaderName][0]), 0, univar.astroLightGrey, "None", True)
                printcolor("   |"+"\n", 0, univar.lastKrColor, "None", True)
                if cptLine == len(univar.dicoInvader[invaderName]):
                    invaderName = random.choice([el for el in list(univar.dicoInvader.keys()) if el != "ufo"])
                    cptLine = 0
                else:
                    cptLine += 1
        printgradientline("╰"+"─"*91+"╯\n", True)
    exit("\n")


def displayFunctionUsage(moduleName, fctName):
    '''
    DESCRIPTION
        Display AstroPapua function usage
    UPDATE
        10/04/23
    COMMENT
    '''    
    invaderName = random.choice([el for el in list(univar.dicoInvader.keys()) if el != "ufo"])
    printgradientline("╭"+"─"*91+"╮\n", True)
    printgradientline("| "+moduleName.upper()+" ".rjust(90-len(moduleName))+"|\n", True)
    printgradientline("|"+"-"*91+"|\n", True)
    printgradientline("|", True)
    displayLine = [" ''' "+univar.dicoAstroFunc[moduleName][fctName]['descr']+"'''"]
    displayLine.append("# Last updated "+univar.dicoAstroFunc[moduleName][fctName]['update'])
    displayLine.append(f"def {fctName}"+"(")
    for argName in univar.dicoAstroFunc[moduleName][fctName]['dicoArgs']:
        argLine = f"{argName.ljust(10)}: {univar.dicoAstroFunc[moduleName][fctName]['dicoArgs'][argName]['argType'].ljust(5)}"
        if "argDefault" in univar.dicoAstroFunc[moduleName][fctName]['dicoArgs'][argName]:
            argLine += f" = {univar.dicoAstroFunc[moduleName][fctName]['dicoArgs'][argName]['argDefault']}"
        displayLine.append(argLine)
    displayLine.append(")")
    cptLine = 0
    for i in range(len(displayLine)):
        if i == 0:
            wrapText = displayLine[i]
        elif i <= 2:
            printgradientline("| ", True)
            wrapText = displayLine[i]
        else:
            printgradientline("| ", True)
            wrapText = "    "+displayLine[i]
        syntax = Syntax(wrapText, "python", theme="native", background_color="default")
        console = Console(width=100000)
        console.print(syntax, end="")
        print(f"\033[F\033[{len(wrapText)+2}C", end=" ")
        print(" ".rjust(74-len(wrapText)), end=" ")
        try:
            for j in range(len(univar.dicoInvader[invaderName][cptLine])):
                printcolor(univar.dicoInvader[invaderName][cptLine][j], 0, univar.astroLightGrey, "None", True)
        except IndexError:
            printcolor(" "*len(univar.dicoInvader[invaderName][0]), 0, univar.astroLightGrey, "None", True)
        printcolor("   |"+"\n", 0, univar.lastKrColor, "None", True)
        if cptLine == len(univar.dicoInvader[invaderName]):
            invaderName = random.choice([el for el in list(univar.dicoInvader.keys()) if el != "ufo"])
            cptLine = 0
        else:
            cptLine += 1
    printgradientline("╰"+"─"*91+"╯\n", True)
    exit("\n")


def printcolor(text: str, style: str = None, rgbFG: str = None, rgbBG: str = None, colorBool: bool = False):
    '''
    DESCRIPTION
        Print text with ansi color
    UPDATE
        10/04/23
    COMMENT
    '''    
    # Disable if stdout is redirect to a file
    if sys.stdout.isatty():
        # decodeText = codecs.decode(text, "unicode_escape")
        if colorBool is True:
            if rgbBG != "None":
                print("\x1b["+str(style)+";38;2;"+rgbFG+";48;2;"+rgbBG+"m"+text+"\x1b[0m", end='')
            else:
                print("\x1b["+str(style)+";38;2;"+rgbFG+"m"+text+"\x1b[0m", end='')
        else:
            print(text, end='')


def printgradientline(text: str, colorBool: bool = False):
    '''
    DESCRIPTION
        Print AstroPapua gradient line
    UPDATE
        10/04/23
    COMMENT
    '''    
    cpt = 0
    for kr in text:
        printcolor(kr, 0, univar.dicoGradient[cpt], "None", colorBool)
        cpt += 1


def printExecution(text: str, tag: str, wrapperName: str) -> Tuple[str, str, str]:
    '''
    DESCRIPTION
        Print AstroPapua execution line
    UPDATE
        10/04/23
    COMMENT
    '''    
    if wrapperName in ["astropapua", "threads"]:
        # Duration display
        delta = datetime.timedelta(seconds=time.time() - univar.astroProfile['main_start'])
        seconds_remaining = delta.seconds
        hours, remainder = divmod(seconds_remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration = f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s"
        printcolor("| ", 1, univar.firstKrColor, "None", True)
        if tag == "major":
            printcolor(" ❰"+duration+"❱ "+text, 1, univar.astroMajor, "None", True)
        elif tag == "minor":
            printcolor(" ❰"+duration+"❱ "+text, 1, univar.astroMinor, "None", True)
        printcolor("|".rjust(87-len(duration)-len(text))+"\n", 1, univar.lastKrColor, "None", True)


def printDico(dico, indent=4):
    '''
    DESCRIPTION
        Pretty print a dictionnary
    UPDATE
        10/04/23
    COMMENT
    '''    
    pp = pprint.PrettyPrinter(indent=indent)
    pp.pprint(dico)


'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                            TEXT FUNCTIONS                                            
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

def text_justify(text, width):
    '''
    DESCRIPTION
        Justify a text
    UPDATE
        10/04/23
    COMMENT
    '''    
    words = text.split()
    if len(words) < 2:
        return text.ljust(width)
    if len(text) < width * 0.75:
        return text.ljust(width)
    spaces_needed = width - sum(len(word) for word in words)
    spaces_between_words = spaces_needed // (len(words) - 1)
    extra_spaces = spaces_needed % (len(words) - 1)
    justified_words = []
    for i in range(len(words) - 1):
        word = words[i]
        spaces_to_add = spaces_between_words + (1 if i < extra_spaces else 0)
        justified_words.append(word + ' ' * spaces_to_add)
    justified_words.append(words[-1])
    return ''.join(justified_words)


def text_wrapper(source_text, width, separator_chars=[" "], justify="left"):
    '''
    DESCRIPTION
        Wrap a text
    UPDATE
        10/04/23
    COMMENT
    '''    
    output = ""
    if type(source_text) != list:
        source_text = [source_text]
    if justify == "left":
        source_text = [s.rstrip() for s in source_text]
    if justify in ["middle", "justified"]:
        source_text = [s.strip() for s in source_text]
    if justify == "right":
        source_text = [s.lstrip() for s in source_text]
    for line in source_text:
        current_length = 0
        latest_separator = -1
        current_chunk_start = 0
        char_index = 0
        while char_index < len(line):
            if line[char_index] in separator_chars:
                latest_separator = char_index
            output += line[char_index]
            current_length += 1
            if current_length == width:
                if latest_separator > current_chunk_start and line[char_index + 1] not in [c for c in separator_chars if c == " "]:
                    cutting_length = char_index - latest_separator
                    if cutting_length:
                        output = output[:-cutting_length]
                    output += "\n"
                    current_chunk_start = latest_separator + 1
                    char_index = current_chunk_start
                else:
                    output += "\n"
                    current_chunk_start = char_index + 1
                    latest_separator = current_chunk_start - 1
                    char_index += 1
                if line[char_index] in " ":
                    char_index += 1
                current_length = 0
            else:
                char_index += 1
        output += "\n"
    output = [o.rstrip().rstrip("\n") for o in output.rstrip("\n").split("\n")]
    if justify == "middle":
        output = [f"{' ' * math.ceil((width - len(o)) / 2)}{o}" for o in output]
        output = [o.rstrip() for o in output]
    if justify == "right":
        output = [o.rjust(width) for o in output]
    if justify == "justified":
        output = [text_justify(o, width) for o in output]
        output = [o.rstrip() for o in output]
    return output


'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                            COLORS FUNCTIONS                                            
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

def random_hex_color(uppercase=False):
    '''
    DESCRIPTION
        Generate random hex color
    UPDATE
        10/04/23
    COMMENT
    '''    
    hex_parts = '0123456789abcdef'
    color = '#'
    for i in range(6):
        color += hex_parts[floor(random() * 16)]
    if uppercase is True:
        return color.upper()
    else:
        return color


def hex_to_RGB(hex):
    '''
    DESCRIPTION
        Convert hexadecimal to rgb color
    UPDATE
        10/04/23
    COMMENT
    '''    
    # return list
    return [int(hex[i:i+2], 16) for i in range(1, 6, 2)]


def RGB_to_hex(RGB):
    '''
    DESCRIPTION
        Convert rgb to hexadecimal color
    UPDATE
        10/04/23
    COMMENT
    '''    
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in RGB])


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    '''
    DESCRIPTION
        Create a hexadecimal color gradient between 2 colors
    UPDATE
        10/04/23
    COMMENT
    '''    
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    HEX_list = [start_hex]
    RBG_list = [s]
    for t in range(1, n):
        curr_vector = [
          int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
          for j in range(3)
        ]
        RBG_list.append(curr_vector)
        HEX_list.append(RGB_to_hex(curr_vector))
    return HEX_list, RBG_list


def requires_white_text(hex_color, threshold=382.5):
    '''
    DESCRIPTION
        Check if a hexadecimal color require a text with white foreground
    UPDATE
        10/04/23
    COMMENT
    '''    
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')
    # Convert hex color to RGB
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # Calculate sum of RGB values
    rgb_sum = sum(rgb)
    # Check if sum is below threshold (default threshold is 382.5)
    return rgb_sum < 382.5