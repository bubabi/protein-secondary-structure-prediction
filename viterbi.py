import numpy as np
import math
import string

class Viterbi(object):
    def __init__(self, state_size, transition_probs, transition_counts,
                    emission_counts, tag_labels, corpus, alpha):
        self.state_size = state_size
        self.transition_probs = transition_probs
        self.transition_counts = transition_counts
        self.emission_counts = emission_counts
        self.tag_labels = tag_labels
        self.backpointers = None
        self.last_tag = None
        self.sentence_size = 0
        self.corpus = corpus
        self.alpha = alpha

    def get_emission_tag_count(self, tag):
        return sum(self.emission_counts[tag].values())

    def get_transition_tag_count(self, tag):
        return sum(self.transition_counts[tag].values())

    def backtracking(self):
        pre_tag = self.last_tag
        tag_list = [pre_tag]

        for m in range(self.sentence_size - 1, -1, -1):
            pre_tag = self.backpointers[pre_tag, m]
            tag_list.append(pre_tag)

        tag_list.reverse()

        return [self.tag_labels[tag] for tag in tag_list[1:]]

    def run(self, sentence):
        tag_indexes = list(range(self.state_size))
        self.sentence_size = len(sentence)
        path = np.zeros(shape=(len(tag_indexes), self.sentence_size + 1))
        backpointers = np.zeros(shape=(len(tag_indexes), self.sentence_size + 1), dtype=np.int)
        tags = self.transition_probs.keys()
        alpha = self.alpha

        print(sentence)

        for count, tag in enumerate(tags):
            if tag == "<s>": continue

            emission = (self.emission_counts[tag].get(sentence[0], 0) + alpha) / \
                    (self.get_emission_tag_count(tag) + 20)

            transition = self.transition_probs['<s>'].get(tag, 0)
            path[count, 0] = math.log10(transition) + math.log10(emission)
            backpointers[count, 0] = 0

        for t in range(1, self.sentence_size):
            for count, tag in enumerate(tags):
                if tag == "<s>": continue

                emission = (self.emission_counts[tag].get(sentence[t], 0) + alpha) / \
                    (self.get_emission_tag_count(tag) + 20)

                path[count, t] = np.min(
                    [path[countp, t - 1] + math.log10(self.transition_probs[tagp].get(tag, 0)) + math.log10(emission) for countp, tagp in enumerate(tags)]
                )

                backpointers[count, t] = np.argmin(
                    [path[countp, t - 1] + math.log10(self.transition_probs[tagp].get(tag, 0)) for countp, tagp in enumerate(tags)]
                )

                print(path[count, t])
        
        last_tag = np.argmin([path[tag, self.sentence_size - 1] for tag in range(len(tags))])

        print(path)
        print(backpointers)
        self.last_tag = last_tag
        self.backpointers = backpointers
