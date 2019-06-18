import os
import random
import subprocess
import questTranslation
import adventuresawait
import math
import time

header = "(define (problem agent)\n(:domain vincentland)\n(:objects "

predicates = ["(location ?l)",
        "(item ?i)",
        "(character ?c)",
        "(has ?cl ?i)",
        "(at ?c ?l)",
        "(player ?p)",
        "(cooperative ?c)",
        "(wants ?c ?i)",
        "(dead ?c)",
        "(weapon ?w)",
        "(adjacent ?la ?lb)",
        "(captive ?captor ?captive)",
        "(damaged ?i)"]

objects = set(["Jafar", "Aladdin", "Jasmine", "Genie","Dragon", "mountain", "lamp", "castle", "you"])

facts = set([ "(character Jafar)",
          "(character Aladdin)",
          "(character Jasmine)",
          "(monster Dragon)",
          "(monster Genie)",
          "(location castle)",
          "(location mountain)",
          "(location lamp)",
          "(item lamp)",
          "(player you)",
          "(has Dragon lamp)",
          "(at Dragon mountain)",
          "(at Jafar castle)",
          "(at Jasmine castle)",
          "(at you castle)",
          "(at Genie lamp)",
          "(at Aladdin castle)",
          "(adjacent mountain lamp)",
          "(adjacent lamp mountain)",
          "(adjacent mountain castle)",
          "(adjacent castle mountain)",
          "(= (total-cost) 0)"])

preferences = dict()
preferences["Jafar"] = ["sedentary"]
preferences["Dragon"] = ["bloodthirsty"]

actionsCosts = dict()
actionsCosts["kill"] = ["(3 bloodthirsty)","(-3 peaceful)"]
actionsCosts["escort"] = ["(-3 sedentary)", "(3 traveller)"]

goals = []

def finished_thinking(calculating):
    total = len(calculating)
    target = total

    for agent in calculating:
        if agent.poll() == None:
            total += -1

    return (total == target)

def rate_plan(plan, preference):
    """ Scores a quest by adding the cost (according to an agent's preferences) 
    of each action """
    score = 0
    if plan == 'Cluster' or plan == []:
        return -1000
    filenames = os.listdir(data)
    solutions = sorted([filename for filename in filenames if filename[-5:] ==".soln"])
    with open(os.path.join(data,solutions[0])) as opened_file:
        everything = opened_file.readlines()
        for line in everything:
            if 'plan cost' in line:
                cost = line.split()[-1]
                return cost/len(plan)


def choose_goals(data,agents, goals_per_agent = 5):
    """ Chooses goals based on preferences, by creating goals stochastically and
    rating them according to action costs """
    
    data = "world"
    domain = "domain.pddl"
    

    for _ in range(goals_per_agent):
        random_goals(agents)

    all_plans = []

    while len(goals) > 0:
        
        agent = agents[0]
        create(data, [agent])
        print("Wait")
        time.sleep(2)
        
        calculating = [subprocess.Popen(["metricff//Metric-FF-v2.1//ff", '-o', os.path.join(data,domain), '-f', os.path.join(data,agent+".pddl"), '-s', '3', '>', os.path.join(data,agent+".soln")])]
        too_long = 10
        thinking_time = time.clock()

        while not finished_thinking(calculating):
            time.sleep(0.1)
            thinking_timelast = time.clock()
            if thinking_time + too_long < thinking_timelast:
                calculating[0].kill()
                break

        translation, quest = questTranslation.interpret(data)
        if quest == []:
            quest = ['Cluster']
        all_plans.append((goals[0], quest))
        goals.pop(0)
    
    for agent in agents:
        scores = []
        preference = preferences[agent]
        for plan in all_plans:
            scores.append((plan[0],rate_plan(plan[1][0],preference)))

        best = sorted(scores)[-1]
        goals.append(best[0])

def random_goals(agents,subgoals=3):
    """ Chooses predicates and objects randomly to create goals.
    Assures the objects are compatible with the chosen predicates. """

    possible_goals = predicates[2:5]+predicates[6:7]+predicates[8:9]
    possible_objects = list(objects)

    for agent in agents:
        agent_goals = []
        for _ in range(random.randint(1,subgoals)):
            agent_goals.append(random.choice(possible_goals))
        print(agent_goals)
        for j,agent_goal in enumerate(agent_goals):
            goal = agent_goal.split()
            new_goal = ""
            for i,part in enumerate(goal):
                if "?" in part:
                    if "cl" in part:
                        chosen = "none"
                        while ("(location "+chosen+")" not in facts) and ("(character "+chosen+")" not in facts):
                            chosen = random.choice(possible_objects)
                        part = part.replace("?cl",chosen)
                    elif "c" in part:
                        chosen = "none"
                        while "(character "+chosen+")" not in facts:
                            chosen = random.choice(possible_objects)
                        part = part.replace("?c",chosen)
                    elif "l" in part:
                        chosen = "none"
                        while "(location "+chosen+")" not in facts:
                            chosen = random.choice(possible_objects)
                        part = part.replace("?l",chosen)
                    elif "i" in part:
                        chosen = "none"
                        while "(item "+chosen+")" not in facts:
                            chosen = random.choice(possible_objects)
                        part = part.replace("?i",chosen)

                new_goal += " "+part
            agent_goals[j] = new_goal
        if len(agent_goals) > 1:
            goals.append("(and"+"".join(agent_goals)+")")
        else:
            goals.append(agent_goals[0])
    print(goals)


def create(data,agents,genesis=False):
    """ Creates task files for the planner """

    if genesis: # Should run only once
        #random_goals(agents)
        choose_goals(data,agents)

    filenames = os.listdir(data)
    for filename in filenames:
        if filename[-5:] == ".soln" or filename[-5:] == ".pddl":
            if filename != "domain.pddl":
                os.remove(os.path.join(data,filename))

    for i,agent in enumerate(agents):
        print(agent)
        #time.sleep(1)
        with open(os.path.join(data,agent+".pddl"),"w") as opened_file:
            personal_header = header.replace("agent",agent)
            opened_file.write(personal_header)
            for obj in objects:
                opened_file.write(obj+" ")
            opened_file.write(")\n(:init ")
            for fact in facts:
                opened_file.write(fact+"\n")
            opened_file.write(")\n")

            opened_file.write("(:goal ")

            opened_file.write(goals[i]+"))")

def update(data,action,agents):
    """ Updates the world facts and rewrites task files """

    action = action.split()

    if action[0] == "move":
        facts.remove("(at "+action[1]+" "+action[3]+")")
        facts.add("(at "+action[1]+" "+action[2]+")")

    elif action[0] == "getfromlocation":
        facts.add("(has "+action[1]+" "+action[2]+")")

    elif action[0] == "giveto":
        facts.remove("(has "+action[1]+" "+action[3]+")")
        facts.add("(has "+action[2]+" "+action[3]+")")
        facts.add("(cooperative "+action[2]+")")

    elif action[0] == "given":
        facts.remove("(has "+action[1]+" "+action[3]+")")
        facts.add("(has "+action[2]+" "+action[3]+")")

    elif action[0] == "kill":
        facts.remove("(character "+action[2]+")")
        #facts.remove("(at "+action[2]+" "+action[4]+")")
        facts.add("(has "+action[4]+" "+action[3]+")")
        facts.add("(dead "+action[2]+")")
        facts.add("(item "+action[2]+")")

    elif action[0] == "escort":
        facts.remove("(at "+action[1]+" "+action[3]+")")
        facts.remove("(at "+action[2]+" "+action[3]+")")
        facts.add("(at "+action[1]+" "+action[4]+")")
        facts.add("(at "+action[2]+" "+action[4]+")")

    create(data,agents)