""" original:
sequences = [["get goto give"],
["spy"],
["goto listen­ goto report"],
["get goto use goto give"],

["get goto give"],
["goto damage goto report"],

["get goto give"],
["goto kill goto report"],
["goto goto report"],

["goto damage"],
["get goto use goto give"],
["get goto use capture goto give"],
["goto listen goto report"],
["goto take goto give"],
["get goto give"],
["goto damage escort goto report"],

["goto damage goto report"],
["get goto use"],
["goto repair"],
["get goto use"],
["goto damage"],
["goto repair"],
["goto defend"],

["goto damage"],
["goto steal goto give"],

["goto get"],
["goto steal"],
["repair"],

["repair use"],
["get use"],
["use"],
["damage"],
["use"],
["get use"],
["get experiment"],

["repair"],
["get goto give"],
["steal"],
["goto exchange"]]
"""
""" version two:
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
"""

# version three (only replaced goto->move and get->getfromlocation and give->giveto)
sequences = [["getfromlocation move giveto"],
["spy"],
["move listen move report"],
["getfromlocation move use move giveto"],

["getfromlocation move giveto"],
["move damage move report"],

["getfromlocation move giveto"],
["move kill move report"],
["move move report"],

["move damage"],
["getfromlocation move use move giveto"],
["getfromlocation move use capture move giveto"],
["move listen move report"],
["move take move giveto"],
["getfromlocation move giveto"],
["move damage escort move report"],

["move damage move report"],
["getfromlocation move use"],
["move repair"],
["getfromlocation move use"],
["move damage"],
["move repair"],
["move defend"],

["move damage"],
["move steal move giveto"],

["move getfromlocation"],
["move steal"],
["repair"],

["repair use"],
["getfromlocation use"],
["use"],
["damage"],
["use"],
["getfromlocation use"],
["getfromlocation experiment"],

["repair"],
["getfromlocation move giveto"],
["steal"],
["move exchange"]]



divided = [sequences[0:4],sequences[4:6],sequences[6:9],sequences[9:16],sequences[16:23],sequences[23:25],sequences[25:28],sequences[28:35],sequences[35:39]]
numbers = [4,2,3,7,7,2,3,7,4] # Number of typical sequences per motivation
motivations = ["Knowledge","Comfort","Reputation","Serenity","Protection","Conquest","Wealth","Ability","Equipment"]

#Sert a rien
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
    The score for each motivation is that number divided by the number of typical sequences.

    Copies the quest and removes one action at a time, comparing the next few actions to each typical sequence
    Scores 1 point for a typical sequence found """

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
        return ["Not found"]
    else:
        while value in scorescopy:
            indices.append(scorescopy.index(value))
            scorescopy[indices[-1]] = 0

    return [motivations[index] for index in indices]

def classify_fuzzy(quest):
    """ Finds how many times a typical sequence for a motivation is found in the quest.
    The score for each motivation is that number divided by the number of typical sequences.

    Copies the quest and removes one action at a time, comparing the next few actions to each typical sequence
    Scores a normalized fuzzy membership value for a piece of a typical sequence found """

    sequence = []
    for action in quest:
        sequence.append(action.split()[0][1:])
    original = list(sequence)
    scores = [0]*9
    index = 0
    for motivation in divided:
        for sequencetype in motivation:
            sequencetype = sequencetype[0].split()
            if len(sequencetype) == 1:
                membership_value = 1.0
                pairs = [list(sequencetype)]
            else:
                membership_value = 1.0/(len(sequencetype)-1)
                pairs = []
                for i in range(len(sequencetype)-1):
                    pairs.append([sequencetype[i], sequencetype[i+1]])

            for pair in pairs:
                sequence = list(original)
                length = len(pair)
                length2 = len(sequence)
                while length <= length2:
                    if sequence[0:length] == pair:
                        scores[index] += membership_value/numbers[index] # Normalization
                    sequence.pop(0)
                    length2 = len(sequence)

        index += 1

    print(scores)
    value = max(scores)
    scorescopy = list(scores)
    indices = []
    if value == 0:
        return ["Not found"]
    else:
        while value in scorescopy:
            indices.append(scorescopy.index(value))
            scorescopy[indices[-1]] = 0

    return ([motivations[index] for index in indices])

#classify_fuzzy(['(explore you bakery village)', '(take you guard sword village)', '(move you castle village)', '(giveto you king sword castle)', '(escort you king castle field)', '(take you king sword field)', '(report you king sword field)', '(kill you king sword field sword)'])