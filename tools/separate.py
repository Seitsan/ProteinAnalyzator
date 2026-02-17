from Bio import SeqIO

all_records = list(SeqIO.parse("../data/insulin.fasta", "fasta"))

oneh = all_records[0:100]
oneth = all_records[0:1000]
tenth = all_records[0:10000]

SeqIO.write(oneh, "../data/xxsmall.faa", "fasta")
SeqIO.write(oneth, "../data/xsmall.faa", "fasta")
SeqIO.write(tenth, "../data/small.faa", "fasta")