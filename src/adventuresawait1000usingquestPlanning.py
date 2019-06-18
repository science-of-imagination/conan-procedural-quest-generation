import subprocess
import os
import sys
import time

import questTranslation
import questClassification
import worldManagement
import questPlanning

class Actions:

    def __init__(self, name, parameters, effects):
        self.name = name
        self.parameters = parameters
        self.effect = effects

def replace_action(currentDomain, action, increase):
    costEffect = "(increase (total-cost) "
    position = currentDomain.find(":action "+action)
    #print(action)
    cutDomain = currentDomain[position:]
    costPosition = cutDomain.find(costEffect)+position

    number = int(currentDomain[costPosition+23])
    #print(number)

    if increase:
        number += 1
        changedDomain = currentDomain[0:costPosition]+costEffect+str(number)+")"+currentDomain[costPosition+(len(costEffect)+2):]
    else:
        number -= 1
        changedDomain = currentDomain[0:costPosition]+costEffect+str(number)+")"+currentDomain[costPosition+(len(costEffect)+2):]
    
    return changedDomain     

def write_domains(data, domain, agents, preferences):
    template = ""
    with open(os.path.join(data,domain),"r") as templatefile:
        template = templatefile.read()
    with open(os.path.join(data,domain),"r") as templatefile:
        template2 = templatefile.readlines()
    listOfActions = []
    actionFound = False
    name = []
    parameters = []
    effect = []
    for lines in template2:
        if 'action ' in lines:
            name.append(lines.split()[1])
        if 'parameters' in lines:
            parameters.append(lines[19:-1].replace(")","").replace("(","").split())
        if 'effect' in lines:
            effect.append(lines[21:-29].split(") "))
            for i,eff in enumerate(effect[0]):
                if i == len(effect[0])-1:
                    break
                effect[0][i] = eff+")"

        if len(name) and len(parameters) and len(effect) > 0:
            actionNamePlaceholder = Actions(name,parameters,effect)
            listOfActions.append(actionNamePlaceholder)
            name = []
            parameters = []
            effect = []


    for agent in agents:
        currentDomain = template
        #Remove that if when not testing a bunch of processes
        #if agent[-1] not in "1 2 3 4 5":
        for preference in preferences[agent]:
            if preference[0] == "+":
                currentDomain = replace_action(currentDomain, preference[1:],increase=True)
            else:
                currentDomain = replace_action(currentDomain, preference[1:],increase=False)
        with open(os.path.join(data,agent,"domain"+agent+".pddl"),"w") as newdomainfile:
            newdomainfile.write(currentDomain)

    return listOfActions

def finished_thinking(calculating):
    total = len(calculating)
    target = total

    for agent in calculating:
        if agent.poll() == None:
            total += -1

    return (total == target)


def main():
    data = "world"

    domain = "domain.pddl"

    #agents = sorted(["baker", "king", "lumberjack", "blacksmith", "merchant", "guard", "daughter"])
    agents = sorted(["baker", "king", "lumberjack", "blacksmith", "merchant", "guard", "daughter"])

    motivation_count = dict()
    motivations = ["Knowledge","Comfort","Reputation","Serenity","Protection","Conquest","Wealth","Ability","Equipment"]
    for motiv in motivations:
        motivation_count[motiv] = 0
    motivation_count["Not found"] = 0

    print(motivation_count)

    emptyOrComplete = 0

    quest_log = open("quest_log.txt","w")

    too_long = 600 # 10 minutes
    run = True

    #Creates all the domains and populates a list of action objects
    listOfActions = write_domains(data, domain, agents, worldManagement.preferences)

    #makes all the goals
    worldManagement.create(data,agents, attempts_per_agent=4, genesis=True, verbose=False)

    while run:


    
        calculating = []
        opened_files = []

        for agent in agents:
            calculating.append(questPlanning.plan_quest(agent))
            #opened_files.append(open(os.path.join(data,agent+".soln"),"w"))
            #calculating.append(subprocess.Popen([os.path.join("metricff","Metric-FF-v2.1","ff"), '-o', os.path.join(data,"domain"+agent+".pddl"), '-f', os.path.join(data,agent+".pddl"), '-s', '3'],stdout=opened_files[-1]))

        thinking_time = time.clock()
        thinking_timelast = thinking_time
        print('Thinking')
        while not finished_thinking(calculating):
            time.sleep(0.5)
            print(".", end=".")
            sys.stdout.flush()
            thinking_timelast += 0.5
            #print(thinking_timelast)
            if thinking_time + too_long < thinking_timelast:
                print(thinking_time)
                print("Took too long!")
                for stillcalculating in calculating:
                    if stillcalculating.poll() == None:
                        stillcalculating.kill()
                break
        
        for opened_file in opened_files:
            opened_file.close()

        print("Done")
        translations, formalplans, NPCNames = questTranslation.interpret(data)

        #print(formalplans)

        motivations = [questClassification.classify_fuzzy(formalplan) for formalplan in formalplans]
        for formalplan,motivation,npcname,translation in zip(formalplans,motivations,NPCNames,translations):

            #prints the quest
            print(npcname)
            print(translation,motivation)
            if len(formalplan) < 1:
                emptyOrComplete += 1
            else:
                print(" ".join(formalplan)+" "+motivation[0])
                quest_log.write(" ".join(formalplan))
                quest_log.write(" m:"+motivation[0])
                quest_log.write("\n\n")
            motivation_count[motivation[0]] += 1
        """
        for formalplan in formalplans:
            #print(formalplan)
            if len(formalplan) < 1:
                emptyOrComplete += 1
            else:
                print(" ".join(formalplan))
                quest_log.write(" ".join(formalplan))
                quest_log.write("\n\n")
        """
        #Prints the motivations
        #print(motivation_count)
        #print(emptyOrComplete)

        action = input()

        if action == "exit":
            run = False
        else:
            worldManagement.update(data, action, agents, listOfActions)



        #run -= 1
        #print ('This is iteration number '+ str(run))
    quest_log.close()

if __name__ == "__main__":
    main()