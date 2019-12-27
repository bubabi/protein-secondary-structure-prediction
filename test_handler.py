from collections import defaultdict, Counter

class TestHandler(object):

    def __init__(self, viterbi):
        self.viterbi = viterbi

    def test_kmer_sequence(self, protein_sequence):
        sequence = list()
        for aa in protein_sequence:
            sequence.append(aa)
        
        self.viterbi.run(sequence)
        best_path = self.viterbi.backtracking()

        return best_path
    
    def kmer(self, protein_sequence):
        votes = defaultdict(list)
        for idx, aa in enumerate(protein_sequence):
            kmer_seq = protein_sequence[idx:idx+5]
            path = self.test_kmer_sequence(kmer_seq)

            for kmer_idx in range(len(path)):
                votes[kmer_idx + idx].append(path[kmer_idx])

        prediction = ""
        for aa in votes:
            most_common,num_most_common = Counter(votes[aa]).most_common(1)[0]
            prediction += most_common

        self.calc_accuracy(prediction)
        print(prediction)
        
    def calc_accuracy(self, prediction):
        num_of_true = 0
        num_of_aa = 0

        alpha_helix = [[3,6], [19,23], [30,32], [36,38], [41,44], [47,55], [166,168], [177,180], [240,242],
                        [278, 287], [288, 290], [322, 324], [335, 354], [335, 354]]
        beta_sheet = [[27, 29], [33, 35], [110, 112], [118, 120], [124, 127], [132, 135], [141, 146],
                        [148, 150], [156, 165], [181, 183], [187, 189], [194, 199], [204, 207], [214, 219], [228, 236],
                        [251, 258], [260, 262], [264, 274], [327, 334]]
        turn = [[8, 10], [105, 108], [121, 123], [128, 131], [209, 211], [225, 227], [243, 248]]

        structures = [alpha_helix, beta_sheet, turn]

        for i in range(len(structures)):
            for interval in structures[i]:
                for idx in range(interval[0]-1, interval[1]-1):
                    if i == 0:
                        if prediction[idx] == "H":
                            num_of_true += 1
                    elif i == 1:
                        if prediction[idx] == "B":
                            num_of_true += 1
                    else:
                        if prediction[idx] == "T":
                            num_of_true += 1
                    
                    num_of_aa += 1
        
        print("Accuracy:", (100*num_of_true) / num_of_aa)
