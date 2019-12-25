import numpy as np
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

        for count, tag in enumerate(tags):
            if tag == "<s>": continue

            if sentence[0] in self.corpus:
                emission = (self.emission_counts.get(tag).get(sentence[0], 0)) / \
                    (self.get_emission_tag_count(tag))

            # if the current word is not in the corpus which means
            # the word is unknown word, apply smoothing
            else:
                emission = (self.emission_counts[tag].get(sentence[0], 0) + alpha) / \
                    (self.get_emission_tag_count(tag) + 20)

            transition = self.transition_probs['<s>'].get(tag, 0)
            path[count, 0] = transition * emission
            backpointers[count, 0] = 0

        for t in range(1, self.sentence_size):
            for count, tag in enumerate(tags):
                if tag == "<s>": continue

                if sentence[t] in self.corpus:
                    emission = (self.emission_counts.get(tag).get(sentence[t], 0)) / \
                        (self.get_emission_tag_count(tag))

                # if the current word is not in the corpus which means
                # the word is unknown word, apply smoothing
                else:
                    emission = (self.emission_counts[tag].get(sentence[t], 0) + alpha) / \
                    (self.get_emission_tag_count(tag) + 20)


                # transition = self.get_smoothed_transition(qp, q)
                # transition = self.transition_probs[qp].get(q, 0)

                path[count, t] = np.max(
                    [path[countp, t - 1] * self.transition_probs[tagp].get(tag, 0) * emission for countp, tagp in enumerate(tags)]
                )

                backpointers[count, t] = np.argmax(
                    [path[countp, t - 1] * self.transition_probs[tagp].get(tag, 0) for countp, tagp in enumerate(tags)]
                )

        last_tag = np.argmax([path[tag, self.sentence_size - 1] for tag in range(len(tags))])

        self.last_tag = last_tag
        self.backpointers = backpointers
