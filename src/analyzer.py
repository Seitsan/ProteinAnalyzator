from Bio import SeqIO
from pathlib import Path
from collections import Counter


nonpolar = ["A", "V", "L", "I", "P", "M", "F", "W"]
uncharged_polar = ['Y', 'N', 'Q', 'G', 'S', 'T', 'C']
positive_polar = ['H', 'K', 'R']
negative_polar = ['D' ,'E']


class ProteinAnalyzer:

    def __init__(self, fasta:Path):
        self.fasta = fasta


    def parse(self):
        """
        Parse FASTA from file.fasta
        Args:
            fasta - path to file.fasta
        Return:
            SeqRecord
        """

        for seq_record in SeqIO.parse(self.fasta, "fasta"):
            print(seq_record.id)
            print(repr(seq_record.seq))
            print(len(seq_record))


    def get_stats(self):

        nonpolar_score = 0
        unch_pol_score = 0
        pos_pol_score = 0
        neg_pol_score = 0

        for seq_record in SeqIO.parse(self.fasta, 'fasta'):
            aa_score = Counter(seq_record)
            nonpolar_score += sum(aa_score[aa] for aa in nonpolar)
            unch_pol_score += sum(aa_score[aa] for aa in uncharged_polar)
            pos_pol_score += sum(aa_score[aa] for aa in positive_polar)
            neg_pol_score += sum(aa_score[aa] for  aa in negative_polar)
        return({
            'Nonpolar AA score': nonpolar_score,
            'Uncharged polar AA score': unch_pol_score,
            'Positively polar AA score': pos_pol_score,
            'Negatively polar AA score': neg_pol_score
                })

#         if output:
#             with open(output, "w") as f:
#                 f.write(f"""Nonpolar AA score: {nonpolar_score}
# Uncharged polar AA score: {unch_pol_score}
# Positively polar AA score: {pos_pol_score}
# Negatively polar AA score: {neg_pol_score}""")
#         else:
#             print(f"""Nonpolar AA score: {nonpolar_score}
# Uncharged polar AA score: {unch_pol_score}
# Positively polar AA score: {pos_pol_score}
# Negatively polar AA score: {neg_pol_score}""")