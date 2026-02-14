from src.analyzer import ProteinAnalyzer
from pathlib import Path


fasta_file = Path("insulin.fasta")
output_file = Path("stats.txt")
protan = ProteinAnalyzer(fasta=fasta_file, output=output_file)
# protan.parse(fasta_file)
protan.get_stats(fasta_file, output_file)