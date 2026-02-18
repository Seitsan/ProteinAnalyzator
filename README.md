# ProteinAnalyzator

A script for checking execution time of parsing and processing of FASTA
with singlethreading, multithreading and multiprocessing.

## Description

This script takes a path to FASTA, parsing and counting aminoacids by their properties.
It consist of:
* **main.py** - main working script. It can save results to csv
* **optimal_mtmp.py** - tool for founding optimal number of threads/processes
* **visualisation.ipynb** - visualisation of depending execution time by quantity of sequnce
and execution time by threads/processes quantity
* **src/analyzer.py** - ProteinAnalyzer class with methods: .parse() - parsing FASTA; 
get_stats() counting aminoacids by his physical and chemical properties to list of dictionaries
* **src/mtclasses.py** - Producer and Consumer classes for multithreading execution.
Producer parsing FASTA and putting a sequences to queue, Consumer takes a sequence 
from queue and processing it
* **tools/separate.py** - tool for splitting FASTA to some files by them sequence quantity

## Getting Started

### Dependencies

  - python=3.13
  - biopython
  - click
  - notebook
  - jupyter
  - pandas
  - numpy
  - matplotlib
  - seaborn

### Installing

**Copying from github**
```commandline
git clone https://github.com/Seitsan/ProteinAnalyzator.git
```

**Activating environment file**
```commandline
cd ProteinAnalyzator
conda env create -f environment.yml
```


### Executing program

Execute main.py with your_file.fasta and choose: print results to terminal or 
saving them to file.csv

```commandline
python main.py your_file.fasta [-m] [-o]
```
-m, --mode: 'st' for singlethreading, 'mt' for multithreading
and 'mp' for multiprocessing. default='st'

-o, --output: for saving results to file.csv. default=None

## Authors


Denis Kolodin ('Seitsan')

## License

This project is licensed under the MIT License - see the LICENSE file for details
