<img src="conf/AstroPapua_banner.png" height="200">

```console
python astropapua --help
```

```python
╭───────────────────────────────────────────────────────────────────────────────────────────╮
|     \           |                     _ \                                       ▄▄        |
|    _ \     __|  __|   __|  _ \       |   |  _` |  __ \   |   |   _` |        ▄▄████▄▄     |
|   ___ \  \__ \  |    |    (   |      ___/  (   |  |   |  |   |  (   |      ▄██████████▄   |
| _/    _\ ____/ \__| _|   \___/      _|    \__,_|  .__/  \__,_| \__,_|    ▄██▄██▄██▄██▄██▄ |
|                                                  _|                        ▀█▀  ▀▀  ▀█▀   |
╰─────────────────────────────────────────────────────────────────────────── haumea (v0.9) ─╯
╭───────────────────────────────────────────────────────────────────────────────────────────╮
| HUBBLE                                                                                    |
|-------------------------------------------------------------------------------------------|
╰───────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────────╮
| STARGAZER                                                                                 |
|-------------------------------------------------------------------------------------------|
| ''' Convert GBK to protein FASTA file '''                                      ▄██▄       |
| def gbk_to_faa(                                                              ▄██████▄     |
|     pathIN: str, pathOUT: str, split: bool = False, ext: str = .gbk)        ███▄██▄███    |
| ''' Convert GBK to gene FASTA file '''                                        ▄▀▄▄▀▄      |
| def gbk_to_ffn(                                                              ▀ ▀  ▀ ▀     |
|     pathIN: str, pathOUT: str, split: bool = False, ext: str = .gbk)                      |
| ''' Convert GBK to nucleic FASTA file '''                                      ▄██▄       |
| def gbk_to_fna(                                                              ▄██████▄     |
|     pathIN: str, pathOUT: str, split: bool = False, ext: str = .gbk)        ███▄██▄███    |
| ''' Convert GBK to GFF file '''                                               ▄▀▄▄▀▄      |
| def gbk_to_gff(                                                              ▀ ▀  ▀ ▀     |
|     pathIN: str, pathOUT: str, split: bool = False, ext: str = .gbk)                      |
| ''' Parse FASTA file and create a dictionnary '''                              ▄██▄       |
| def make_fasta_dict(                                                         ▄██████▄     |
|     pathIN: str, unique: bool = False, pathJSON: str = )                    ███▄██▄███    |
| ''' Parse GBK files and create a dictionnary '''                              ▄▀▄▄▀▄      |
| def make_gbk_dict(                                                           ▀ ▀  ▀ ▀     |
|     pathIN: str, pathJSON: str = , sort: bool = True,                                     |
|     boolPseudo: bool = False)                                                ▄▄████▄▄     |
| ''' Make a GBK from FASTA files '''                                         ██████████    |
| def make_gbk_from_fasta(                                                    ██▄▄██▄▄██    |
|     pathIN: str, pathOUT: str, topology: str, division: str,                 ▄▀▄▀▀▄▀▄     |
|     taxID: int = 0, extList: str = fna,ffn,faa,trnascanse)                  ▀        ▀    |
| ''' Parse GFF file and create a dictionnary '''                                           |
| def make_gff_dict(                                                            ▀▄   ▄▀     |
|     pathIN: str, pathJSON: str = , ext: str = .gff)                          ▄█▀███▀█▄    |
| ''' Search terms in FASTA '''                                               █▀███████▀█   |
| def search_in_fasta(                                                        █ █▀▀▀▀▀█ █   |
|     pathIN: str, search: str, pathOUT: str, unique: bool = False,              ▀▀ ▀▀      |
|     ext: str = .faa)                                                                      |
| ''' Slice a GBK file using 2 genes interval '''                                ▄██▄       |
| def slice_genes_gbk(                                                         ▄██████▄     |
|     pathIN: str, pathOUT: str, lt1: str, lt2: str)                          ███▄██▄███    |
| ''' Unwrap FASTA '''                                                          ▄▀▄▄▀▄      |
| def unwrap_fasta(                                                            ▀ ▀  ▀ ▀     |
|     pathIN: str, ext: str = .fna)                                                         |
╰───────────────────────────────────────────────────────────────────────────────────────────╯
```

---------------------------------------

#### Configuration


