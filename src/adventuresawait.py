import subprocess
import os
import sys
import time

import questTranslation
import questClassification
import worldManagement

def replace_action(currentDomain, action, increase):
    costEffect = "(increase (total-cost) "
    position = currentDomain.find(":action "+action)
    print(action)
    cutDomain = currentDomain[position:]
    costPosition = cutDomain.find(costEffect)+position

    number = int(currentDomain[costPosition+23])
    print(number)

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
    
    for agent in agents:
        currentDomain = template
        for preference in preferences[agent]:
            if preference[0] == "+":
                currentDomain = replace_action(currentDomain, preference[1:],increase=True)
            else:
                currentDomain = replace_action(currentDomain, preference[1:],increase=False)
        with open(os.path.join(data,"domain"+agent+".pddl"),"w") as newdomainfile:
            newdomainfile.write(currentDomain)

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

    agents = sorted(["baker", "king", "lumberjack", "blacksmith", "merchant", "guard", "daughter"])

    write_domains(data, domain, agents, worldManagement.preferences)
    
    worldManagement.create(data,agents,genesis=True)

    too_long = 10000

    run = True
    calculating = []
    opened_files = []
    while run:

        for agent in agents:
            opened_files.append(open(os.path.join(data,agent+".soln"),"w")) 
            calculating.append(subprocess.Popen([os.path.join("metricff","Metric-FF-v2.1","ff"), '-o', os.path.join(data,"domain"+agent+".pddl"), '-f', os.path.join(data,agent+".pddl"), '-s', '3'],stdout=opened_files[-1]))

        thinking_time = time.clock()
        print('Thinking')
        while not finished_thinking(calculating):
            time.sleep(0.5)
            print("..", end=".")
            thinking_time = time.clock()
            if thinking_time > too_long:
                break
        for opened_file in opened_files:
            opened_file.close()

        print("Done")
        translations, formalplans = questTranslation.interpret(data)

        print(formalplans)

        motivations = [questClassification.classify(formalplan) for formalplan in formalplans]

        for translation,motivation in zip(translations,motivations):
            print(translation,motivation)

        action = input()

        if action == "exit":
            run = False
        else:
            worldManagement.update(data, action, agents)


if __name__ == "__main__":
    main()