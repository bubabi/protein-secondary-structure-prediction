import operator
import numpy as np
from hmm_builder import HMMBuilder
from parser import InputParser
from viterbi import Viterbi
from test_handler import TestHandler
import random

input_path = "./TrainingDataset.txt"


if __name__ == '__main__':

    parser = InputParser(input_path)
    parser.parse_data()

    transition_counts = parser.get_transition_counts()


    emission_counts, corpus = parser.get_emission_counts()

    print("Transition_counts:", transition_counts)
    print("\nEmission_counts:", emission_counts)

    print("\nCorpus:", corpus)


    hmm_builder = HMMBuilder(transition_counts, emission_counts)
    transition_probability = hmm_builder.build_transition_probability()

    transition_probability = hmm_builder.normalize(transition_probability)
    
    print(transition_probability)
    # emission probabilities were calculated by smoothing manually in the Viterbi class.

    # total number of tags
    state_size = len(transition_probability.keys())
    # only tag labels for backtracking
    tag_labels = list(transition_probability.keys())
    # called k or alpha which will be used in add-k smoothing
    alpha = 1

    viterbi = Viterbi(state_size, transition_probability, transition_counts,
                        emission_counts, tag_labels, corpus, alpha)


    # test_seq = "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGPDEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQKTYQGSYGFRLGFLHSGTAKSVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHERCSDSDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCNSSCMGGMNRRPILTIITLEDSSGNLLGRNSFEVRVCACPGRDRRTEEENLRKKGEPHHELPPGSTKRALPNNTSSSPQPKKKPLDGEYFTLQIRGRERFEMFRELNEALELKDAQAGKEPGGSRAHSSHLKSKKGQSTSRHKKLMFKTEGPDSD"

    test_handler = TestHandler(viterbi)
    test_handler.kmer("MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGPDEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQKTYQGSYGFRLGFLHSGTAKSVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHERCSDSDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCNSSCMGGMNRRPILTIITLEDSSGNLLGRNSFEVRVCACPGRDRRTEEENLRKKGEPHHELPPGSTKRALPNNTSSSPQPKKKPLDGEYFTLQIRGRERFEMFRELNEALELKDAQAGKEPGGSRAHSSHLKSKKGQSTSRHKKLMFKTEGPDSD")
        
    # test_handler.kmer("MEEPQSD")
