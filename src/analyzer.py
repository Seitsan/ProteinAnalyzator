from Bio import SeqIO
from pathlib import Path
from collections import Counter


nonpolar = ["A", "V", "L", "I", "P", "M", "F", "W"]
uncharged_polar = ['Y', 'N', 'Q', 'G', 'S', 'T', 'C']
positive_polar = ['H', 'K', 'R']
negative_polar = ['D' ,'E']
aacids = nonpolar + uncharged_polar + positive_polar + negative_polar


class ProteinAnalyzer:

    def __init__(self, fasta:Path):
        self.fasta = fasta


    def parse(self):
        """
        Parse FASTA from file.fasta
        Args:
            fasta - path to file.fasta
        """

        for seq_record in SeqIO.parse(self.fasta, "fasta"):
            yield seq_record.seq


    def get_stats(self, seq):

        nonpolar_score = 0
        unch_pol_score = 0
        pos_pol_score = 0
        neg_pol_score = 0
        other = 0


        aa_score = Counter(seq)
        nonpolar_score += sum(aa_score[aa] for aa in nonpolar)
        unch_pol_score += sum(aa_score[aa] for aa in uncharged_polar)
        pos_pol_score += sum(aa_score[aa] for aa in positive_polar)
        neg_pol_score += sum(aa_score[aa] for  aa in negative_polar)
        other += sum(aa_score[aa] for aa in aa_score if aa not in aacids)
        return([
            {'type': 'Nonpolar', 'quantity': nonpolar_score},
            {'type': 'Uncharged_polar', 'quantity': unch_pol_score},
            {'type': 'Positively_polar', 'quantity': pos_pol_score},
            {'type': 'Negatively_polar', 'quantity': neg_pol_score},
            {'type': 'Other', 'quantity': other}
                ])
