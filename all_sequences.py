from processes_per_sequance import *
import json
from itertools import groupby
from configs import *

def key_func(k):
    return k['SequenceUUID']


class AllSequence:

    def __init__(self, descs):
        self.information = list(descs).pop()
        descs = list(descs)[:-1]
        self.descs = [desc for desc in descs if ("error" not in desc) and ("Heading" in desc)]
        self.sequences = []
        self.information['Information']['anomaly_sequences'] = []

    def create_json(self):
        results = []

        for _, val in groupby(self.descs, key_func):
            self.sequences.append(list(val))
        limits= LimitValues()
        for sequence in self.sequences:
            process = ProcessSeq(sequence)
            if len(sequence) > limits.sequence_limit:
                result, failure_sequence = process.add_column()
                if failure_sequence == True:
                    self.information['Information']['anomaly_sequences'].append(sequence[0]['SequenceUUID'])
            else:
                result = process.lower_sequence()
                self.information['Information']['anomaly_sequences'].append(sequence[0]['SequenceUUID'])
            results.append(result)
            results.append(self.information)
        return results


with open('/home/izzet/Downloads/3_1_2022_pendik.json') as fp:
    descs = json.load(fp)

all = AllSequence(descs)
final = all.create_json()
print(final)