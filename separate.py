from Bio import SeqIO

targets = [100, 1000, 10000]
result_seqs = []
for target in targets:
    min_diff = float('inf')
    for seq_record in SeqIO.parse("insulin.fasta", "fasta"):
        curr_dif = abs(len(seq_record) - target)
        if curr_dif < min_diff:
            min_diff = curr_dif
            closest_seq = seq_record
    result_seqs.append(closest_seq)

SeqIO.write(result_seqs[0], "xxsmall.faa", "fasta")
SeqIO.write(result_seqs[1], "xsmall.faa", "fasta")
SeqIO.write(result_seqs[2], "small.faa", "fasta")