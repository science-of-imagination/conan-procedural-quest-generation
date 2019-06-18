import subprocess
import os
import sys
import time

import questTranslation
import questClassification
import worldManagement
'''
TODO: Add all actions from the paper
TODO: Fix the escort when it should goto. Maybe precondition is dangerous place or person is movable
TODO: Motivation and preferences

'''
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

    agents = ["Jafar","Aladdin","Jasmine","Genie","Dragon"]

    worldManagement.create(data,agents,genesis=True)

    too_long = 20

    run = True
    while run:
        calculating = [subprocess.Popen(["metricff//Metric-FF-v2.1//ff", '-o', os.path.join(data,domain), '-f', os.path.join(data,agent+".pddl"), '-s', '3', '>', os.path.join(data,agent+".soln")]) for agent in agents]

        thinking_time = time.clock()

        while not finished_thinking(calculating):
            time.sleep(0.1)
            thinking_time = time.clock()
            if thinking_time > too_long:
                break
        translations, formalplans = questTranslation.interpret(data)

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