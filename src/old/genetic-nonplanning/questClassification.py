sequences = [["getfromlocation move giveto"],
["spy"],
["move listen move report"],
["getfromlocation move use move giveto"],

["getfromlocation move giveto"],
["move kill move report"],

["getfromlocation move giveto"],
["move kill move report"],
["move move report"],

["move kill"],
["getfromlocation move use move giveto"],
["getfromlocation move use capture move giveto"],
["move listen move report"],
["move given move giveto"],
["getfromlocation move giveto"],
["move kill escort move report"],

["move kill move report"],
["getfromlocation move use"],
["move repair"],
["getfromlocation move use"],
["move kill"],
["move repair"],
["move defend"],

["move kill"],
["move steal move giveto"],

["move getfromlocation"],
["move steal"],
["repair"],

["repair use"],
["getfromlocation use"],
["use"],
["kill"],
["use"],
["getfromlocation use"],
["getfromlocation experiment"],

["repair"],
["getfromlocation move giveto"],
["steal"],
["move giveto given"]]

divided = [sequences[0:4],sequences[4:6],sequences[6:9],sequences[9:16],sequences[16:23],sequences[23:25],sequences[25:28],sequences[28:35],sequences[35:39]]
numbers = [4,2,3,7,7,2,3,7,4] # Number of typical sequences per motivation
motivations = ["Knowledge","Comfort","Reputation","Serenity","Protection","Conquest","Wealth","Ability","Equipment"]

def classify_once(quest):
    """ Finds if a typical sequence for a motivation is found in the quest.
    The score for each motivation is the number of typical sequences found. """

    sequence = []
    for action in quest:
        sequence.append(action.split()[0][1:])

    sequence = [" ".join(sequence)]

    scores = [0]*9
    index = 0
    for motivation in divided:
        for sequencetype in motivation:
            if sequencetype[0] in sequence[0]:
                scores[index] += 1
        index += 1

    print(scores)
    value = max(scores)
    motivation = scores.index(value)

    return motivations[motivation]

def classify(quest):
    """ Finds how many times a typical sequence for a motivation is found in the quest.
    The score for each motivation is that number divided by the number of typical sequences. """

    sequence = []
    for action in quest:
        sequence.append(action.split()[0][1:])
    original = list(sequence)
    scores = [0]*9
    index = 0
    for motivation in divided:
        for sequencetype in motivation:
            sequence = list(original)
            sequencetype = sequencetype[0].split()
            length = len(sequencetype)
            length2 = len(sequence)
            while length <= length2:
                if sequence[0:length] == sequencetype:
                    scores[index] += 1.0/numbers[index] # Normalization
                sequence.pop(0)
                length2 = len(sequence)

        index += 1

    print(scores)
    value = max(scores)
    scorescopy = list(scores)
    indices = []
    if value == 0:
        indices = [0]
    else:
        while value in scorescopy:
            indices.append(scorescopy.index(value))
            scorescopy[indices[-1]] = 0

    return [motivations[index] for index in indices]