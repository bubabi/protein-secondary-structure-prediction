
class TestHandler(object):

    def __init__(self, viterbi):
        self.viterbi = viterbi

    def test_individual_sequence(self, protein_sequence):
        sequence = list()
        for aa in protein_sequence:
            sequence.append(aa)
        
        self.viterbi.run(sequence)
        l = self.viterbi.backtracking()

        print(l)
    
    def parse(self):
        f = open('predicted_tags.csv', 'w')
        f.write("Id,Category\n")
        num_of_true = 0
        num_of_words = 0
        for line in self.test_set:
            sentence = list()
            only_tag_sequence = list()
            words_with_tag = line.split()
            for element in words_with_tag:
                pairs = element.split("/")
                word = pairs[0].lower()
                tag = pairs[1]
                sentence.append(word)
                only_tag_sequence.append(tag)

            self.viterbi.run(sentence)
            l = self.viterbi.backtracking()

            for i in range(len(sentence)):
                if only_tag_sequence[i] == l[i]:
                    num_of_true += 1
                    num_of_words += 1
                else:
                    num_of_words += 1
                f.write(str(num_of_words) + "," + l[i] + "\n")
        f.close()
        print("# of Correct Found Tags:", num_of_true, "\n# of Total Words", num_of_words)
        print("Accuracy:", (100*num_of_true) / num_of_words)
