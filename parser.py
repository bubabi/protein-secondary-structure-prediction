from collections import defaultdict
from typing import Optional

class InputParser(object):

    def __init__(self, path):
        self.path = path
        self.hydrogen_bonding_patterns = {'helix': ['G', 'H', 'I'],
                                          'sheet': ['B', 'E'],
                                          'turn': ['T', 'S', 'L']}
        self.data = list()

    def parse_data(self):
        with open(self.path) as f:
            lines = f.readlines()
            i = 0
            for i in range(0, len(lines)-2, 3):
                protein = lines[i:i+3]
                sequence_header = protein[0].strip()[1:]

                aa_seq = protein[1].strip().upper()
                secondary_structre = protein[2].strip()
                
                processed_seq = self.preprocessing_sequence(aa_seq, secondary_structre)

                self.data.append(processed_seq)

    def preprocessing_sequence(self, amino_acid_sequence, secondary_structre):
        preprocessed_sequence = ""
        for i in range(len(amino_acid_sequence)):
            if secondary_structre[i] == "_":
                continue
            else:
                if secondary_structre[i] in self.hydrogen_bonding_patterns['helix']:
                    preprocessed_sequence += amino_acid_sequence[i] + "/" + "H "
                elif secondary_structre[i] in self.hydrogen_bonding_patterns['sheet']:
                    preprocessed_sequence += amino_acid_sequence[i] + "/" + "B "
                else:
                    preprocessed_sequence += amino_acid_sequence[i] + "/" + "T "    
        
        return preprocessed_sequence[:-1]

    def get_transition_counts(self):
        transition_pairs = defaultdict(dict)
        start_token = "start/<s>"
        for line in self.data:
            words_with_tag = line.split()
            words_with_tag.insert(0, start_token)
            for i in range(len(words_with_tag)-1):
                pre_tag = words_with_tag[i].split("/")[1]
                post_tag = words_with_tag[i+1].split("/")[1]
                transition_pairs[pre_tag][post_tag] = transition_pairs.get(pre_tag, {}).get(post_tag, 0) + 1

        return transition_pairs

    def get_emission_counts(self):
        corpus = set()
        tags = list()
        emission_pairs = defaultdict(dict)
        for line in self.data:
            words_with_tag = line.split()
            for element in words_with_tag:
                pairs = element.split("/")
                word = pairs[0]
                corpus.add(word)
                tag = pairs[1]
                emission_pairs[tag][word] = emission_pairs.get(tag, {}).get(word, 0) + 1
        return emission_pairs, corpus
