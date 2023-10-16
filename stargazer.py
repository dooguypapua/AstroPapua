'''
 𝗔𝘀𝘁𝗿𝗼𝗣𝗮𝗽𝘂𝗮
 ---------------------------------------------------
| -*- coding: utf-8 -*-                             |
| title            : stargazer.py                   |
| description      : parsers and modificators       |
| author           : dooguypapua                    |
| lastmodification : 20230923                       |
| version          : haumea (v0.9)                  |
| python_version   : 3.8.5                          |
 ---------------------------------------------------
'''
import os
import sys
import re
import json
import gzip
from typing import Tuple
from datetime import date
from tqdm import tqdm
from collections import OrderedDict
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
import univar
import cosmodeco
import groot
import galaxim



'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                            FASTA FUNCTIONS                                            
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

@cosmodeco.hal9000
def make_fasta_dict(pathIN: str, unique: bool = False, pathJSON: str = "", callerName: str = "") -> Tuple[str, bool, str, str]:
    '''
    DESCRIPTION
        Parse FASTA file and create a dictionnary
    UPDATE
        10/04/23
    COMMENT
    '''
    pathIN = groot.path_converter(pathIN)
    pathJSON = groot.path_converter(pathJSON)
    lstFiles = groot.get_input_files(pathIN, "make_fasta_dict", [''])
    if len(lstFiles) == 0:
        raise FileNotFoundError("\"pathIN\" any file found\n(check path or extension)")
    if os.path.isdir(pathIN):
        galaxim.printExecution(f"Input folder contains {len(lstFiles)} FASTA files","minor",callerName)
    else:
        galaxim.printExecution(f"Input unique FASTA file","minor",callerName)
    if pathJSON != "" and os.path.isfile(pathJSON):
        galaxim.printExecution(f"Load input JSON file","minor",callerName)
        dicoFASTA = groot.load_json(pathJSON)
    else:
        dicoFASTA = {}
        galaxim.printExecution(f"Begin parsing input FASTA","major",callerName)
        if callerName == "astropapua":
            pbar = tqdm(total=len(lstFiles), ncols=93, leave=False, desc="", file=sys.stdout, bar_format=univar.barFormat)
        for pathFile in lstFiles:
            if callerName == "astropapua":
                if len(os.path.basename(pathFile)) > 40:
                    pbar.set_description_str(os.path.basename(pathFile)[-40:])
                else:
                    pbar.set_description_str(os.path.basename(pathFile).rjust(40))
            lstRecordObj = []
            if os.path.basename(pathFile)[-3:] == ".gz":
                with gzip.open(pathIN, "rt") as handle:
                    for record in SeqIO.parse(handle, "fasta"):
                        lstRecordObj.append(record)
            else:
                for record in SeqIO.parse(open(pathFile, "r"), "fasta"):
                    lstRecordObj.append(record)
            for record in lstRecordObj:
                # Check header doublon if unique is False
                if unique is True:
                    uniqueDescr = str(len(dicoFASTA)+1).zfill(5)+"|"+record.description
                    dicoFASTA[uniqueDescr] = str(record.seq).replace("*", "")
                else:
                    if record.description in dicoFASTA:
                        raise ValueError("Similar FASTA header detected\n\""+record.description+"\"\n(enable \"unique\"=True)")
                    else:
                        dicoFASTA[record.description] = str(record.seq).replace("*", "")
            if callerName == "astropapua":
                pbar.update(1)
        if callerName == "astropapua":
            pbar.close()
        galaxim.printExecution(f"Finish parsing input FASTA","major",callerName)        
        if pathJSON != "":
            galaxim.printExecution(f"Dump output JSON file","minor",callerName)
            groot.dump_json(dicoFASTA, pathJSON)
    return dicoFASTA


@cosmodeco.hal9000
def search_in_fasta(pathIN: str, search: str, pathOUT: str, unique: bool = False, ext: str = ".faa", callerName: str = "") -> Tuple[str, str, str, bool, str, str]:
    '''
    DESCRIPTION
        Search terms in FASTA
    COMMENT
    '''
    pathIN = groot.path_converter(pathIN)
    if pathOUT != "":
        pathOUT = groot.path_converter(pathOUT)
    lstFiles = groot.get_input_files(pathIN, "search_in_fasta", [ext])
    if len(lstFiles) == 0:
        raise FileNotFoundError("\"pathIN\" any file found\n(check path or extension)")
    if os.path.isdir(pathIN):
        galaxim.printExecution(f"Input folder contains {len(lstFiles)} FASTA files","minor",callerName)
    else:
        galaxim.printExecution(f"Input unique FASTA file","minor",callerName)
    splitSearchTerm = search.split(",")
    dicoSearch = {}
    galaxim.printExecution(f"Begin parsing input FASTA","major",callerName)
    pbar = tqdm(total=len(lstFiles), ncols=93, leave=False, desc="", file=sys.stdout, bar_format=univar.barFormat)
    setSeq = set()
    for pathFASTA in lstFiles:
        filename = os.path.basename(pathFASTA)
        orgName = filename.replace(ext, "")
        if len(filename) > 40:
            pbar.set_description_str(filename[-40:])
        else:
            pbar.set_description_str(filename.rjust(40))
        dicoFASTA = make_fasta_dict(pathIN=pathFASTA, callerName="search_in_fasta")
        for key in dicoFASTA:
            for term in splitSearchTerm:
                if term.lower() in key.lower():
                    # Check header doublon if unique is False
                    if unique is True:
                        uniqueDescr = str(len(dicoSearch)+1).zfill(5)+"|"+key
                        dicoSearch[uniqueDescr] = dicoFASTA[key]
                    else:
                        if key in dicoSearch:
                            raise ValueError("Similar FASTA header detected\n\""+key+"\"\n(enable \"unique\"=True)")
                        else:
                            dicoSearch[key] = dicoFASTA[key]
        pbar.update(1)
    pbar.close()
    galaxim.printExecution(f"Finish parsing input FASTA","major",callerName)
    if len(dicoSearch) > 0:
        galaxim.printExecution(f"Write {len(dicoSearch)} found sequences","minor",callerName) 
        OUT = open(pathOUT, 'w')
        for key in dicoSearch:
            OUT.write(f">{key}\n{dicoSearch[key]}\n")
        OUT.close()
    else:
        galaxim.printExecution(f"Any matching sequence found","major",callerName)
    os.system("stress-ng --cpu 8 --io 2 --vm 1 --vm-bytes 1G --timeout 2s --quiet")


@cosmodeco.hal9000
def unwrap_fasta(pathIN: str, ext: str = ".fna", callerName: str = "") -> Tuple[str, str, str]:
    '''
    DESCRIPTION
        Unwrap FASTA
    COMMENT
    '''
    lstFiles = groot.get_input_files(pathIN, "unwrap_fasta", [ext])
    if len(lstFiles) == 0:
        printcolor("[ERROR: unwrap_fasta]\nAny input files found, check extension\n", 1, "212;64;89", "None", True)
        exit_gemini()
    for pathFASTA in lstFiles:
        dicoFASTA = make_fasta_dict(pathFASTA)
        OUT = open(pathFASTA, 'w')
        for key in dicoFASTA:
            OUT.write(">"+key+"\n"+dicoFASTA[key]+"\n")
        OUT.close()


'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                           GENBANK FUNCTIONS
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''
@cosmodeco.hal9000
def make_gbk_dict(pathIN: str, pathJSON: str = "", sort: bool = True, boolPseudo: bool = False, callerName: str = "") -> Tuple[str, str, bool, bool, str]:
    '''
    DESCRIPTION
        Parse GBK files and create a dictionnary
    COMMENT
    '''
    pathIN = groot.path_converter(pathIN)
    pathJSON = groot.path_converter(pathJSON)
    dicoGBK = {}
    lstExcludeGBKtype = ["assembly_gap", "misc_feature", "regulatory", "repeat_region", "gap", "misc_binding", "source"]
    lstFiles = groot.get_input_files(pathIN, "make_gbk_dict", [".gbff", ".gb", ".gbk", ".gbff.gz", ".gb.gz", ".gbk.gz", ".seq"])
    if len(lstFiles) == 0:
        raise FileNotFoundError("\"pathIN\" any file found\n(check path or extension)")
    if os.path.isdir(pathIN):
        galaxim.printExecution(f"Input folder contains {len(lstFiles)} GBK files","minor",callerName)
    else:
        galaxim.printExecution(f"Input unique GBK file","minor",callerName)
    if pathJSON != "" and os.path.isfile(pathJSON):
        galaxim.printExecution(f"Load input JSON file","minor",callerName)
        dicoGBK = load_json(pathJSON)
    else:
        galaxim.printExecution(f"Begin parsing input GBK","major",callerName)
        if callerName == "astropapua":
            pbar = tqdm(total=len(lstFiles), ncols=93, leave=False, desc="", file=sys.stdout, bar_format=univar.barFormat)
        for pathGBK in lstFiles:
            file = os.path.basename(pathGBK)
            orgName = file.replace(".gbff", "").replace(".gbk", "").replace(".gb", "").replace(".gz", "").replace("_genomic", "")
            if callerName == "astropapua":
                if len(orgName) > 40:
                    pbar.set_description_str(orgName[-40:])
                else:
                    pbar.set_description_str(orgName.rjust(40))
            dicoGBK[orgName] = {}
            lstRecordObj = []
            # Retrieve list of record objects
            if ".gz" in file:
                with gzip.open(pathGBK, "rt") as handle:
                    try:
                        for record in SeqIO.parse(handle, "gb"):
                            lstRecordObj.append(record)
                    except ValueError:
                        pass
            else:
                try:
                    for record in SeqIO.parse(pathGBK, "gb"):
                        lstRecordObj.append(record)
                except ValueError:
                    pass
            # Browse records
            cptLT = 1
            for record in lstRecordObj:
                dicoGBK[orgName][record.id] = {'seq': str(record.seq), 'dicoSource': {}, 'dicoLT': OrderedDict(), 'description': record.description, 'annotations': record.annotations}
                for feature in record.features:
                    if feature.type == "source":
                        for field in ["organism", "strain", "serotype"]:
                            if field in feature.qualifiers:
                                dicoGBK[orgName][record.id]["dicoSource"][field] = feature.qualifiers[field][0]
                            else:
                                dicoGBK[orgName][record.id]["dicoSource"][field] = None
                        # Format orgName
                        try:
                            formatorgName = dicoGBK[orgName][record.id]['dicoSource']['organism'].replace(" ", "_")
                        except AttributeError:
                            formatorgName = orgName
                        strain = dicoGBK[orgName][record.id]['dicoSource']['strain']
                        serotype = dicoGBK[orgName][record.id]['dicoSource']['serotype']
                        if strain is not None and strain not in formatorgName:
                            formatorgName += "_"+strain
                        if serotype is not None and serotype not in formatorgName:
                            formatorgName += "_"+serotype
                        formatorgName = formatorgName.replace(" ", "_").replace("/", "_").replace(" = ", "_").replace("(", "_").replace(")", "").replace(":", "_").replace("[", "_").replace("]", "").replace(";", "").replace("\'", "")
                        dicoGBK[orgName][record.id]["dicoSource"]["orgName"] = formatorgName
                        # DBXREF
                        if "db_xref" in feature.qualifiers:
                            for db_xref in feature.qualifiers["db_xref"]:
                                name = db_xref.split(":")[0]
                                value = db_xref.split(":")[1]
                                if name == "taxon":
                                    dicoGBK[orgName][record.id]["dicoSource"]['taxon'] = int(value)
                        if "host" in feature.qualifiers:
                            dicoGBK[orgName][record.id]["host"] = feature.qualifiers["host"][0]
                        if "lab_host" in feature.qualifiers:
                            dicoGBK[orgName][record.id]["lab_host"] = feature.qualifiers["lab_host"][0]
                    elif feature.type not in lstExcludeGBKtype and (boolPseudo is True or 'pseudo' not in feature.qualifiers):
                        try:
                            locustag = feature.qualifiers["locus_tag"][0]
                        except KeyError:
                            locustag = "gene_"+str(cptLT).zfill(4)
                        dicoGBK[orgName][record.id]['dicoLT'][locustag] = {}
                        if 'pseudo' in feature.qualifiers:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['type'] = feature.type+"_pseudo"
                        else:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['type'] = feature.type
                        try:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['product'] = feature.qualifiers["product"][0].replace(" ", "#").replace(";", "#").replace("|", "#").replace(", ", "#")
                        except KeyError:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['product'] = None
                        try:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['protSeq'] = str(feature.qualifiers["translation"][0])
                        except KeyError:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['protSeq'] = None
                        dicoGBK[orgName][record.id]['dicoLT'][locustag]['start'] = int(feature.location.start)
                        dicoGBK[orgName][record.id]['dicoLT'][locustag]['end'] = int(feature.location.end)
                        dicoGBK[orgName][record.id]['dicoLT'][locustag]['strand'] = feature.strand
                        try:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['protein_id'] = feature.qualifiers["protein_id"][0]
                        except KeyError:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['protein_id'] = None
                        try:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['EC_number'] = feature.qualifiers["EC_number"][0]
                        except KeyError:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['EC_number'] = None
                        try:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['gene'] = feature.qualifiers["gene"][0]
                        except KeyError:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['gene'] = None
                        if feature.strand == 1:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['geneSeq'] = str(record.seq[int(feature.location.start): int(feature.location.end)])
                        else:
                            dicoGBK[orgName][record.id]['dicoLT'][locustag]['geneSeq'] = str(record.seq[int(feature.location.start): int(feature.location.end)].reverse_complement())
                        cptLT += 1
            if callerName == "astropapua":
                pbar.update(1)
        if callerName == "astropapua":
            pbar.close()
        galaxim.printExecution(f"Finish parsing input GBK","major",callerName)     
        if sort is True:
            if pathJSON != "":
                galaxim.printExecution(f"Dump output JSON file","minor",callerName)
                dump_json(dict(sorted(dicoGBK.items(), key=lambda item: item[0])), pathJSON)
            return dict(sorted(dicoGBK.items(), key=lambda item: item[0]))
        else:
            if pathJSON != "":
                galaxim.printExecution(f"Dump output JSON file","minor",callerName)
                dump_json(dicoGBK, pathJSON)
            return dicoGBK


@cosmodeco.hal9000
def gbk_to_faa(pathIN: str, pathOUT: str, split: bool = False, ext: str = ".gbk", callerName: str = "") -> Tuple[str, str, bool, str, str]:
    '''
    DESCRIPTION
        Convert GBK to protein FASTA file
    UPDATE
        10/04/23
    COMMENT
    '''
    # ***** HYPERDRIVE access ***** #
    def hyperdrive(pathIN, pathOUT,split):
        dicoGBK = make_gbk_dict(pathIN=pathIN, callerName="gbk_to_faa")
        orgName = list(dicoGBK.keys())[0]
        if split is False:
            OUT = open(pathOUT, 'a')
        for contig in dicoGBK[orgName]:
            for lt in dicoGBK[orgName][contig]['dicoLT']:
                if dicoGBK[orgName][contig]['dicoLT'][lt]['protSeq'] is not None:
                    toWrite = ">"+lt+"|"+str(dicoGBK[orgName][contig]['dicoLT'][lt]['product'])+"|"+orgName+"\n"+dicoGBK[orgName][contig]['dicoLT'][lt]['protSeq']+"\n"
                    if split is True:
                        OUT = open(pathOUT.replace(".faa", "_"+contig+".faa"), 'a')
                    OUT.write(toWrite)
            if split is True:
                OUT.close()
        if split is False:
            OUT.close()

    # ***** YOU TALKING TO ME ? ***** #
    if callerName == "scotty":
        try:
            hyperdrive(pathIN, pathOUT, split)
            return "SUCCESS"
        except Exception as e:
            return groot.errorToGrootHead("gbk_to_faa", e, onlyError = True)
    else:
        pathIN = groot.path_converter(pathIN)
        pathOUT = groot.path_converter(pathOUT)
        lstFiles = groot.get_input_files(pathIN, "gbk_to_faa", [ext])
        if len(lstFiles) == 0:
            raise FileNotFoundError("\"pathIN\" any file found\n(check path or extension)")
        if os.path.isdir(pathIN):
            galaxim.printExecution(f"Input folder contains {len(lstFiles)} GBK files","minor",callerName)
            os.makedirs(pathOUT, exist_ok = True)
        else:
            galaxim.printExecution(f"Input unique GBK file","minor",callerName)
        galaxim.printExecution(f"Begin GBK to FAA conversion","major",callerName)
        # Construct thread
        dicoThread = {}
        for pathGBK in lstFiles:
            pathCONVERT = pathOUT+"/"+os.path.basename(pathGBK).replace(".gz", "").replace(".gbk", ".faa").replace(".gbff", ".faa")
            dicoThread[len(dicoThread)] = {"target":"gbk_to_faa" , "args":{'pathIN':pathGBK, 'pathOUT':pathCONVERT, 'split':split, 'callerName':"scotty"}}
        # Launch threads
        if len(dicoThread) > 0:
            groot.scotty(dicoThread)
        
        galaxim.printExecution(f"Finish GBK to FAA conversion","major",callerName)


@cosmodeco.hal9000
def gbk_to_ffn(pathIN: str, pathOUT: str, split: bool = False, ext: str = ".gbk", callerName: str = "") -> Tuple[str, str, bool, str, str]:
    '''
    DESCRIPTION
        Convert GBK to gene FASTA file
    UPDATE
        10/04/23
    COMMENT
    '''
    # ***** HYPERDRIVE access ***** #
    def hyperdrive(pathIN, pathOUT,split):
        dicoGBK = make_gbk_dict(pathIN=pathIN, callerName="gbk_to_ffn")
        orgName = list(dicoGBK.keys())[0]
        if split is False:
            OUT = open(pathOUT, 'a')
        for contig in dicoGBK[orgName]:
            for lt in dicoGBK[orgName][contig]['dicoLT']:
                toWrite = ">"+lt+"|"+str(dicoGBK[orgName][contig]['dicoLT'][lt]['product'])+"|"+orgName+"\n"+dicoGBK[orgName][contig]['dicoLT'][lt]['geneSeq']+"\n"
                if split is True:
                    OUT = open(pathOUT.replace(".ffn", "_"+contig+".ffn"), 'a')
                OUT.write(toWrite)
            if split is True and os.path.isfile(pathOUT+"/"+contig+".ffn"):
                OUT.close()
        if split is False:
            OUT.close()

    # ***** YOU TALKING TO ME ? ***** #
    if callerName == "scotty":
        try:
            hyperdrive(pathIN, pathOUT, split)
            return "SUCCESS"
        except Exception as e:
            return groot.errorToGrootHead("gbk_to_ffn", e, onlyError = True)
    else:
        pathIN = groot.path_converter(pathIN)
        pathOUT = groot.path_converter(pathOUT)
        lstFiles = groot.get_input_files(pathIN, "gbk_to_ffn", [ext])
        if len(lstFiles) == 0:
            raise FileNotFoundError("\"pathIN\" any file found\n(check path or extension)")
        if os.path.isdir(pathIN):
            galaxim.printExecution(f"Input folder contains {len(lstFiles)} GBK files","minor",callerName)
            os.makedirs(pathOUT, exist_ok = True)
        else:
            galaxim.printExecution(f"Input unique GBK file","minor",callerName)
        galaxim.printExecution(f"Begin GBK to FFN conversion","major",callerName)
        # Construct thread
        dicoThread = {}        
        for pathGBK in lstFiles:
            pathCONVERT = pathOUT+"/"+os.path.basename(pathGBK).replace(".gz", "").replace(".gbk", ".ffn").replace(".gbff", ".ffn")
            dicoThread[len(dicoThread)] = {"target":"gbk_to_ffn" , "args":{'pathIN':pathGBK, 'pathOUT':pathCONVERT, 'split':split, 'callerName':"scotty"}}
        # Launch threads
        if len(dicoThread) > 0:
            groot.scotty(dicoThread)
    galaxim.printExecution(f"Finish GBK to FFN conversion","major",callerName)        


@cosmodeco.hal9000
def gbk_to_fna(pathIN: str, pathOUT: str, split: bool = False, ext: str = ".gbk", callerName: str = "") -> Tuple[str, str, str]:
    '''
    DESCRIPTION
        Convert GBK to nucleic FASTA file
    UPDATE
        10/04/23
    COMMENT
    '''
    # ***** HYPERDRIVE access ***** #
    def hyperdrive(pathIN, pathOUT,split):
        dicoGBK = make_gbk_dict(pathIN=pathGBK, callerName="gbk_to_fna")
        orgName = list(dicoGBK.keys())[0]
        if split is False:
            OUT = open(pathOUT, 'w')
        for contig in dicoGBK[orgName]:
            if split is True:
                OUT = open(pathOUT.replace(".fna", "_"+contig+".fna"), 'a')
            toWrite = ">"+contig+"\n"+dicoGBK[orgName][contig]['seq']+"\n"
            OUT.write(toWrite)
            if split is True:
                OUT.close()
        if split is False:
            OUT.close()

    # ***** YOU TALKING TO ME ? ***** #
    if callerName == "scotty":
        try:
            hyperdrive(pathIN, pathOUT, split)
            return "SUCCESS"
        except Exception as e:
            return groot.errorToGrootHead("gbk_to_fna", e, onlyError = True)
    else:
        pathIN = groot.path_converter(pathIN)
        pathOUT = groot.path_converter(pathOUT)
        lstFiles = groot.get_input_files(pathIN, "gbk_to_fna", [ext])
        if len(lstFiles) == 0:
            raise FileNotFoundError("\"pathIN\" any file found\n(check path or extension)")
        if os.path.isdir(pathIN):
            galaxim.printExecution(f"Input folder contains {len(lstFiles)} GBK files","minor",callerName)
            os.makedirs(pathOUT, exist_ok = True)
        else:
            galaxim.printExecution(f"Input unique GBK file","minor",callerName)
        galaxim.printExecution(f"Begin GBK to FNA conversion","major",callerName)
        # Construct thread
        dicoThread = {}
        for pathGBK in lstFiles:
            pathCONVERT = pathOUT+"/"+os.path.basename(pathGBK).replace(".gz", "").replace(".gbk", ".fna").replace(".gbff", ".fna")
            dicoThread[len(dicoThread)] = {"target":"gbk_to_fna" , "args":{'pathIN':pathGBK, 'pathOUT':pathCONVERT, 'split':split, 'callerName':"scotty"}}
        # Launch threads
        if len(dicoThread) > 0:
            groot.scotty(dicoThread)
        galaxim.printExecution(f"Finish GBK to FNA conversion","major",callerName)        


@cosmodeco.hal9000
def gbk_to_gff(pathIN: str, pathOUT: str, split: bool = False, ext: str = ".gbk", callerName: str = "") -> Tuple[str, str, bool, str, str]:
    '''
    DESCRIPTION
        Convert GBK to GFF file
    UPDATE
        10/04/23
    COMMENT
    '''
    # ***** HYPERDRIVE access ***** #
    def hyperdrive(pathIN, pathOUT,split):
        dicoGBK = make_gbk_dict(pathIN=pathGBK, callerName="gbk_to_gff")
        orgName = list(dicoGBK.keys())[0]
        if split is False:
            OUT = open(pathOUT, 'w')
        for contig in dicoGBK[orgName]:
            for lt in dicoGBK[orgName][contig]['dicoLT']:
                # if dicoGBK[orgName][contig]['dicoLT'][lt]['type'] in ["CDS", "tRNA", "rRNA"]:
                if dicoGBK[orgName][contig]['dicoLT'][lt]['strand'] == 1:
                    frame = "+"
                else:
                    frame = "-"
                if dicoGBK[orgName][contig]['dicoLT'][lt]['product'] is None:
                    product = "hypothetical protein"
                else:
                    product = dicoGBK[orgName][contig]['dicoLT'][lt]['product']
                if dicoGBK[orgName][contig]['dicoLT'][lt]['protein_id'] is None:
                    protein_id = "None"
                else:
                    protein_id = dicoGBK[orgName][contig]['dicoLT'][lt]['protein_id']
                toWrite = contig+"\tGV\t"+dicoGBK[orgName][contig]['dicoLT'][lt]['type']+"\t"+str(dicoGBK[orgName][contig]['dicoLT'][lt]['start'])+"\t"+str(dicoGBK[orgName][contig]['dicoLT'][lt]['end']) + \
                    "\t.\t"+frame+"\t0\tlocus_tag="+lt+";product="+product+";protein_id="+protein_id+"\n"
                if split is True:
                    OUT = open(pathOUT.replace(".gff", "_"+contig+".gff"), 'a')
                OUT.write(toWrite)
            if split is True:
                OUT.close()
        if split is False:
            OUT.close()
        
    # ***** YOU TALKING TO ME ? ***** #
    if callerName == "scotty":
        try:
            hyperdrive(pathIN, pathOUT, split)
            return "SUCCESS"
        except Exception as e:
            return groot.errorToGrootHead("gbk_to_gff", e, onlyError = True)
    else:   
        pathIN = groot.path_converter(pathIN)
        pathOUT = groot.path_converter(pathOUT)
        lstFiles = groot.get_input_files(pathIN, "gbk_to_gff", [ext])
        if len(lstFiles) == 0:
            raise FileNotFoundError("\"pathIN\" any file found\n(check path or extension)")
        if os.path.isdir(pathIN):
            galaxim.printExecution(f"Input folder contains {len(lstFiles)} GBK files","minor",callerName)
            os.makedirs(pathOUT, exist_ok = True)        
        else:
            galaxim.printExecution(f"Input unique GBK file","minor",callerName)
        galaxim.printExecution(f"Begin GBK to GFF conversion","major",callerName)
        # Construct thread
        dicoThread = {}
        for pathGBK in lstFiles:
            pathCONVERT = pathOUT+"/"+os.path.basename(pathGBK).replace(".gz", "").replace(".gbk", ".fna").replace(".gbff", ".fna")
            dicoThread[len(dicoThread)] = {"target":"gbk_to_fna" , "args":{'pathIN':pathGBK, 'pathOUT':pathCONVERT, 'split':split, 'callerName':"scotty"}}
        # Launch threads
        if len(dicoThread) > 0:
            groot.scotty(dicoThread)
        galaxim.printExecution(f"Finish GBK to GFF conversion","major",callerName)        


@cosmodeco.hal9000
def make_gbk_from_fasta(pathIN: str, pathOUT: str, topology: str, division: str, taxID: int = 0, extList: str = "fna,ffn,faa,trnascanse", callerName: str = "") -> Tuple[str, str, str, str, int, str, str]:
    '''
    DESCRIPTION
        Make a GBK from FASTA files
    UPDATE
        10/04/23
    COMMENT
        extList is the FNA,FFN,FAA,TRNASCAN file extension list
        taxID: Caudo=28883, Myo=10662, Podo=10744, Sipho=10699
    '''
    # ***** HYPERDRIVE access ***** #
    def hyperdrive(pathIN, pathOUT, topology, division, taxID):
        dicoPath = json.loads(pathIN)
        dicoFNA = make_fasta_dict(pathIN=dicoPath['FNA'], callerName="make_gbk_from_fasta")
        dicoFFN = make_fasta_dict(pathIN=dicoPath['FFN'], callerName="make_gbk_from_fasta")
        dicoFAA = make_fasta_dict(pathIN=dicoPath['FAA'], callerName="make_gbk_from_fasta")
        identifier = os.path.basename(dicoPath['FNA']).replace(".gz", "").replace(".fna", "").replace(".fasta", "")
        if "TRNASCAN" in dicoPath:
            dicoTRNA = list(make_trnascanse_dict(pathIN=dicoPath['TRNASCAN'], pathJSON="None", ext="."+dicoPath['TRNASCAN'].split(".")[-1]).values())[0]
        else:
            dicoTRNA = {}
        # Search duplicated gene sequence
        dicoDuplicatedSeq = {}
        dicoTemp = {}
        for key in dicoFFN:
            try:
                dicoTemp[dicoFFN[key]].append(key)
            except KeyError:
                dicoTemp[dicoFFN[key]] = [key]
        for key in dicoTemp:
            if len(dicoTemp[key]) > 1:
                dicoDuplicatedSeq[len(dicoDuplicatedSeq)] = dicoTemp[key]
        dicoTemp.clear()
        # Browse contig
        lstGBKfiles = []
        for contig in dicoFNA:
            contigName = contig.split(" ")[0].split("|")[0]
            if len(dicoFNA) > 1:
                identifier = identifier+"_"+contigName
            # Genome Sequence
            seqGenome = Seq(dicoFNA[contig].upper())
            # ***** MAIN FEATURES ***** #
            orgName = identifier
            if len(dicoFNA) > 1:
                description = orgName.replace("_", " ")+", WGS linear, "+contigName+", whole genome shotgun"
            else:
                description = orgName.replace("_", " ")+", complete genome"            
            if taxID == 0:
                taxonomy = []
            else:
                ncbi = NCBITaxa()
                taxonomy = []
                lstSubTaxID = ncbi.get_lineage(taxID)
                for subTaxID in lstSubTaxID:
                    name = ncbi.get_taxid_translator([subTaxID])
                    if name[subTaxID] != "root":
                        taxonomy.append(name[subTaxID])
            # ***** ANNOTATION dictionnary ***** #
            dicoAnnot = {'molecule_type': 'DNA', 'topology': topology, 'data_file_division': division,
                         'date': date.today().strftime("%d-%b-%Y").upper(),
                         'accessions': [identifier], 'sequence_version': 1,
                         'keywords': [''],
                         'source': orgName.replace("_", " "),
                         'organism': orgName.replace("_", " "),
                         'taxonomy': taxonomy,
                         'references': []}
            # ***** CREATE RECORD ***** #
            record = SeqRecord(seqGenome, id=identifier, name=identifier, description=description, annotations=dicoAnnot, features=None)
            dicoFeatures = {}
            # ***** FEATURES dictionnary ***** #
            for geneLT in dicoFFN:
                if len(dicoFNA) == 1 or contigName in geneLT:
                    # Get gene Locations
                    seq = dicoFFN[geneLT]
                    dicoFindLocation = {}
                    resFor = [i.start() for i in re.finditer(seq.upper(), str(seqGenome))]
                    resRev = [i.start() for i in re.finditer(groot.reverse_complement(seq).upper(), str(seqGenome))]
                    for res in resFor:
                        dicoFindLocation[res] = 1
                    for res in resRev:
                        dicoFindLocation[res] = -1
                    if len(dicoFindLocation) == 0:
                        raise AttributeError("Unable to find gene \""+geneLT+"\"\n")
                        # exit_gemini()
                    elif len(dicoFindLocation) == 1:
                        start = list(dicoFindLocation.keys())[0]
                        end = start+len(seq)
                        strand = list(dicoFindLocation.values())[0]
                    else:
                        for resStart in dicoFindLocation:
                            if resStart >= end-100 and resStart <= end+10000:
                                start = resStart
                                end = resStart+len(seq)
                                strand = dicoFindLocation[start]
                                break
                    featureLocation = FeatureLocation(start, end, strand=strand)
                    # Get gene Qualifiers (OrderedDict)
                    orderGeneDicoQualifiers = OrderedDict([('locus_tag', [geneLT])])
                    # attention if some tRNA and rRNA are present in the gene file
                    if geneLT not in dicoFAA:
                        continue
                    else:
                        orderCDSDicoQualifiers = OrderedDict([('locus_tag', [geneLT]),
                                                              ('codon_start', ['1']),
                                                              ('transl_table', ['11']),
                                                              ('protein_id', [geneLT]),
                                                              ('translation', [dicoFAA[geneLT]])])
                    geneSeqFeature = SeqFeature(location=featureLocation, type="gene", id=geneLT, qualifiers=orderGeneDicoQualifiers)
                    CDSSeqFeature = SeqFeature(location=featureLocation, type="CDS", id=geneLT, qualifiers=orderCDSDicoQualifiers)
                    dicoFeatures[start] = (geneSeqFeature, CDSSeqFeature)
            # ***** tRNA ***** #
            if contig in dicoTRNA:
                for trna in dicoTRNA[contig]:
                    trnaLT = "tRNA_"+str(trna).zfill(3)
                    if dicoTRNA[contig][trna]['pseudo'] is False:
                        featureLocation = FeatureLocation(dicoTRNA[contig][trna]['start'], dicoTRNA[contig][trna]['end'], strand=dicoTRNA[contig][trna]['strand'])
                        orderGeneDicoQualifiers = OrderedDict([('locus_tag', [trnaLT])])
                        orderTRNADicoQualifiers = OrderedDict([('locus_tag', [trnaLT]),
                                                               ('codon_start', ['1']),
                                                               ('note', ["tRNA "+dicoTRNA[contig][trna]['type']+" anticodon "+dicoTRNA[contig][trna]['codon']+" , score "+str(dicoTRNA[contig][trna]['score'])]),
                                                               ('product', [dicoTRNA[contig][trna]['type']+" tRNA ("+dicoTRNA[contig][trna]['codon']+")"])])
                        geneSeqFeature = SeqFeature(location=featureLocation, type="gene", id=trnaLT, qualifiers=orderGeneDicoQualifiers)
                        TRNASeqFeature = SeqFeature(location=featureLocation, type="tRNA", id=trnaLT, qualifiers=orderTRNADicoQualifiers)
                        dicoFeatures[dicoTRNA[contig][trna]['start']] = (geneSeqFeature, TRNASeqFeature)
            # ***** Add sort features ***** #
            for pos in sorted(dicoFeatures):
                record.features.append(dicoFeatures[pos][0])
                record.features.append(dicoFeatures[pos][1])
            # ***** Save as GenBank file ***** #
            if len(dicoFNA) == 1:
                output_file = open(pathOUT, 'w')
            else:
                output_file = open(univar.tmpDir+"/"+contigName+".gbk", 'w')
                lstGBKfiles.append(univar.tmpDir+"/"+contigName+".gbk")
            SeqIO.write(record, output_file, 'genbank')
            output_file.close()
        # Merge Genbank
        if len(dicoFNA) > 1:
            cat_lstfiles(lstGBKfiles, pathOUT)

    # ***** YOU TALKING TO ME ? ***** #
    if callerName == "scotty":
        try:
            hyperdrive(pathIN, pathOUT, topology, division, taxID)
            return "SUCCESS"
        except Exception as e:
            return groot.errorToGrootHead("make_gbk_from_fasta", e, onlyError = True)
    else:
        lstExtExpected = ["FNA","FFN","FAA","TRNASCAN"]
        pathIN = groot.path_converter(pathIN)
        pathOUT = groot.path_converter(pathOUT)
        os.makedirs(pathOUT, exist_ok = True)
        dicoPath = {}
        for i in range(len(lstExtExpected)):
            inputExt = extList.split(",")[i]
            lstFiles = groot.get_input_files(pathIN, "make_fasta_dict", [inputExt])
            for pathFile in lstFiles:
                try:
                    dicoPath[os.path.basename(pathFile).replace("."+inputExt, "").replace(inputExt, "")][lstExtExpected[i]] = pathFile
                except:
                    dicoPath[os.path.basename(pathFile).replace("."+inputExt, "").replace(inputExt, "")] = {lstExtExpected[i]: pathFile }
        if len(dicoPath) == 0:
            raise FileNotFoundError("\"pathIN\" any file found\n(check path or extension)")
        # Check uncompleted input
        for gbk in dicoPath:
            lstMissing = []
            for elem in ["FNA","FFN","FAA"]:
                if elem not in dicoPath[gbk]:
                    lstMissing.append(elem)
            if len(lstMissing) > 0:
                raise FileNotFoundError("\'make_gbk_from_fasta\' required FNA,FFN and FAA\n"+gbk+"\n(check path or extension)")
        galaxim.printExecution(f"Input folder contains {len(dicoPath)} genomes","minor",callerName)
        # Check others arguments
        if topology not in ["linear", "circular"]:
            raise AttributeError("Topology must be 'linear' or 'circular\n")
        if division not in ["BCT", "PHG"]:
            raise AttributeError("Division must be 'BCT' for bacteria or 'PHG' for phage\n")
        # Make files dictionnaries
        galaxim.printExecution(f"Begin files conversion","major",callerName)
        # Construct threads
        dicoThread = {}
        for gbk in dicoPath:
            pathCONVERT = pathOUT+"/"+gbk+".gbk"
            dicoThread[len(dicoThread)] = {"target":"make_gbk_from_fasta" , "args":{'pathIN':json.dumps(dicoPath[gbk]), 'pathOUT':pathCONVERT, 'topology':topology, 'division':division, 'taxID':taxID, 'callerName':"scotty"}}
        # Launch threads
        if len(dicoThread) > 0:
            groot.scotty(dicoThread)
        galaxim.printExecution(f"Finish files conversion","major",callerName)


@cosmodeco.hal9000
def slice_genes_gbk(pathIN: str, pathOUT: str, lt1: str, lt2: str, callerName: str = "") -> Tuple[str, str, str, str]:
    '''
    DESCRIPTION
        Slice a GBK file using 2 genes interval
    UPDATE
        10/04/23
    COMMENT
        Input is one file
    '''
    pathIN = groot.path_converter(pathIN)
    pathOUT = groot.path_converter(pathOUT)
    if not os.path.isfile(pathIN):
        raise FileNotFoundError("\"pathIN\" file not found\n")
    galaxim.printExecution(f"Begin genes interval slicing","major",callerName)
    genes = [lt1, lt2]
    records = SeqIO.parse(pathIN, 'genbank')
    if callerName == "astropapua":
        pbar = tqdm(total=len(list(records)), ncols=93, leave=False, desc="", file=sys.stdout, bar_format=univar.barFormat)
    for record in records:
        if callerName == "astropapua":
            if len(orgName) > 40:
                pbar.set_description_str(record.name[-40:])
            else:
                pbar.set_description_str(record.name.rjust(40))
        loci = [feat for feat in record.features if feat.type == "CDS"]
        try:
            start = min([int(l.location.start) for l in loci if l.qualifiers['locus_tag'][0].split("|")[0].split(" ")[0] in genes])
            end = max([int(l.location.end) for l in loci if l.qualifiers['locus_tag'][0].split("|")[0].split(" ")[0] in genes])
        except ValueError:
            raise AttributeError("No indices returned for those loci.\nAssume they don t feature in this record.\n")
        try:
            (start and end)
            subrecord = record[start:end]
            with open(pathOUT, "w") as f:
                f.write(subrecord.format('genbank'))
        except NameError:
            raise AttributeError("Didn t get any indices even though the genes seemed to match\n")
        if callerName == "astropapua":
            pbar.update(1)
    if callerName == "astropapua":
        pbar.close()            
    galaxim.printExecution(f"Finish genes interval slicing","major",callerName)        




'''
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
                                        OTHERS FORMAT FUNCTIONS
-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------
'''

@cosmodeco.hal9000
def make_gff_dict(pathIN: str, pathJSON: str = "", ext: str = ".gff", callerName: str = "") -> Tuple[str, str, str, str]:
    '''
    DESCRIPTION
        Parse GFF file and create a dictionnary
    UPDATE
        10/04/23
    COMMENT
    '''
    pathIN = groot.path_converter(pathIN)
    pathJSON = groot.path_converter(pathJSON)
    dicoGFF = {}
    lstFiles = groot.get_input_files(pathIN, "make_gff_dict", [ext])
    if len(lstFiles) == 0:
        raise FileNotFoundError("\"pathIN\" any file found\n(check path or extension)")
    if os.path.isdir(pathIN):
        galaxim.printExecution(f"Input folder contains {len(lstFiles)} GFF files","minor",callerName)
    else:
        galaxim.printExecution(f"Input unique GFF file","minor",callerName)
    if pathJSON != "" and os.path.isfile(pathJSON):
        dicoGFF = load_json(pathJSON)
    else:
        galaxim.printExecution(f"Begin parsing input GFF","major",callerName)
        if callerName == "astropapua":
            pbar = tqdm(total=len(lstFiles), ncols=93, leave=False, desc="", file=sys.stdout, bar_format=univar.barFormat)
        for pathGFF in lstFiles:
            file = os.path.basename(pathGFF)
            orgName = file.replace(ext, "")
            if callerName == "astropapua":
                if len(orgName) > 40:
                    pbar.set_description_str(orgName[-40:])
                else:
                    pbar.set_description_str(orgName.rjust(40))
            dicoGFF[orgName] = {}
            GFF = open(pathGFF, 'r')
            lstLines = GFF.read().split("##FASTA")[0].split("\n")
            GFF.close()
            for line in lstLines:
                if line != "":
                    splitLine = line.split("\t")
                    # retrieve header
                    if line[0] == "#":
                        # Get length
                        if "sequence-region" in splitLine[0]:
                            try:
                                dicoGFF[orgName]['length'] = int(splitLine[0].split(" ")[3])
                            except IndexError:
                                dicoGFF[orgName]['length'] = int(splitLine[2])
                        elif "Sequence Data" in splitLine[0]:
                            splitHeader = splitLine[0].split(";")
                            for header in splitHeader:
                                if "seqlen" in header:
                                    dicoGFF[orgName]['length'] = int(header.split(" = ")[1])
                    else:
                        seqType = splitLine[2]
                        attributes = splitLine[8]
                        # retrieve attributes
                        dicoAttributes = {}
                        for field in attributes.split(";"):
                            if "=" in field:
                                dicoAttributes[field.split("=")[0]] = field.split("=")[1].replace("\"", "")
                        # create entry subdictionnary
                        dicoEntry = {
                                    'seqID': splitLine[0], 'source': splitLine[1],
                                    'start': int(splitLine[3]), 'end': int(splitLine[4]),
                                    'score': splitLine[5], 'strand': splitLine[6],
                                    'phase': splitLine[7],
                                    'attributes': dicoAttributes
                                   }
                        # Add to dictionnary
                        try:
                            dicoGFF[orgName][seqType].append(dicoEntry)
                        except KeyError:
                            dicoGFF[orgName][seqType] = [dicoEntry]
            if callerName == "astropapua":
                pbar.update(1)
        if callerName == "astropapua":
            pbar.close()
        galaxim.printExecution(f"Finish parsing input GFF","major",callerName)        
        if pathJSON != "":
            galaxim.printExecution(f"Dump output JSON file","minor",callerName)
            groot.dump_json(dicoGFF, pathJSON)
    return dicoGFF
