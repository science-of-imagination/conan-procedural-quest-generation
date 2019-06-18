import os

def translate(action):
    """ Translates a quest from the PDDL format to English  """
    
    action = action.replace("\\n","")[1:-2].split()
    verb = action[0]
    sentence = ""
    if verb == "move":
        sentence = action[1]+" go to the "+action[2]+" from the "+action[3]
    elif verb == "getfromlocation":
        sentence = action[1]+" retrieve some "+action[2]+" from the "+action[3]
    elif verb == "giveto":
        sentence = action[1]+" offer some "+action[3]+" to the "+action[2]+" in the "+action[4]
    elif verb == "given":
        sentence = action[2]+" are given some "+action[3]+" by the "+action[1]+" in the "+action[4]
    elif verb == "kill":
        sentence = action[1]+" kill the "+action[2]+" with a "+action[5]+", who drops some "+action[3]+" in the "+action[4]
    elif verb == "escort":
        sentence = action[1]+" escort the "+action[2]+" to the "+action[4]+" from the "+action[3]
    elif verb == "drop":
        sentence = action[1]+" drop some "+action[3]+" at the "+action[2]

    return sentence

def communication_filter(quest, difficulty):
    """ Hides a number of steps in the quest equal to the difficulty setting
    2 would hide 50%, one every other step. 3 would hide two steps between each revealed step. """
    
    length = len(quest)

    revealed = list(range(0,length,difficulty)) # if it starts at 0: always gives the first step
    
    for i,step in enumerate(quest):
        if i not in revealed:
            quest[i] = "?"

    return quest

def interpret(data, difficulty=1): # Higher difficulty leads to several hidden steps 
    """ Reads a solution file and produces a quest """

    quests = []
    filenames = os.listdir(data)
    solutions = sorted([filename for filename in filenames if filename[-5:] ==".soln"])
    indicesToPop = []
    for solution in solutions:
        with open(os.path.join(data,solution)) as opened_file:
            quest = opened_file.readlines()
            opened_file.seek(0)
            newQuest = []
            #foundSteps = 0
            questFound = False
            if "Solution found!" in opened_file.read():

                for lines in quest:
                    if "Actual search time:" in lines:
                        questFound = True
                    if questFound:
                        if "Plan length:" in lines:

                            break

                        newQuest.append('('+" ".join(lines.split()[:-1])+')')
                    """
                if 'plan cost' in lines:
                    break
                if foundSteps == 0 and '0:' not in lines:
                    pass
                elif foundSteps == 1 or '0:' in lines:
                    if '0:' in lines:
                        newQuest.append('('+" ".join(lines.split()[2:])+')')
                        foundSteps = 1
                    else:
                        newQuest.append('('+" ".join(lines.split()[1:])+')')
                """
                quests.append(newQuest[1:])
            else:
                indicesToPop.append(solution)

    for indices in indicesToPop:
        solutions.remove(indices)

    translations = []
    for quest in quests:
        translation = []
        for action in quest:
            translation.append(translate(action))
        translations.append(communication_filter(translation,difficulty))

    return translations, quests, solutions