import os
import random
import subprocess
import questTranslation
#import adventuresawait
import math
import time
import questPlanning

header = "(define (problem agent)\n(:domain vincentland)\n(:objects "

""" Deprecated
predicates = ["(location ?l)",
        "(item ?i)",
        "(info ?info)",
        "(character ?c)",
        "(has ?cl ?i)",
        "(at ?c ?l)",
        "(player ?p)",
        "(cooperative ?c)",
        "(wants ?c ?i)",
        "(cooperative ?c)",
        "(weapon ?w)",
        "(captive ?p ?c)",
        "(damaged ?i)",
        "(defended ?c)",
        "(sneaky ?p)",
        "(dead ?m)",
        "(experimented ?i)",
        "(explored ?l)",
        "(used ?i)"]
"""
predicates_as_goals = [
        "(has ?cl ?i)",
        "(has ?p ?o)",
        "(has ?c ?o)",
        "(cooperative ?c)",
        "(at ?c ?l)",
        "(character ?c)",
        "(captive ?p ?c)",
        "(damaged ?i)",
        "(defended ?c)",
        "(defended ?i)",
        "(sneaky ?p)",
        "(dead ?m)",
        "(experimented ?i)",
        "(explored ?l)",
        "(used ?i)"]

objects = set(["Jafar", "Aladdin", "Jasmine", "Genie","Dragon", "mountain", "lamp", "castle", "you", "secret"])

facts = set([ "(character Jafar)",
          "(character Aladdin)",
          "(character Jasmine)",

          "(monster Dragon)",
          "(monster Genie)",

          "(location castle)",
          "(location mountain)",
          "(location lamp)",

          "(item lamp)",

          "(information secret)",

          "(player you)",

          "(has Dragon lamp)",
          "(has Jafar secret)",

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

goals = []

preferences = dict()
preferences["Jafar"] = ["-kill", "-spy", "-take", "-stealth","-move"]
preferences["Dragon"] = ["-damage","-take","-report","+escort","-defend"]
preferences["Aladdin"] = ["+kill","-exchange","-use","+escort"]
preferences["Jasmine"] = ['+kill', '-spy', '-take', '-stealth']
preferences["Genie"] = ["-kill", "-exchange", "-defend", "-read"]


def finished_thinking(calculating):
    total = len(calculating)
    target = total

    for agent in calculating:
        if agent.poll() == None:
            total += -1

    return (total == target)

def rate_plan(plan):
    """ Scores a quest by adding the cost (according to an agent's preferences)
    of each action """

    data = "world"

    if plan == 'Cluster' or plan == [] or len(plan[0]) == 0:
        return 1000 # Probably also when the goal is already achieved
    filenames = os.listdir(data)
    solutions = sorted([filename for filename in filenames if filename[-5:] ==".soln"])
    with open(os.path.join(data,solutions[0])) as opened_file:
        everything = opened_file.readlines()
        for line in everything:
            if 'plan cost' in line:
                cost = line.split()[-1]
                score = int(float(cost))/len(plan[0])
                if score == 0:
                    return 1000 # Goal already achieved
                else:
                    return score
    return 2000 # Impossible goal



def choose_goals(data,agents, quests_per_agent = 1, attempts_per_agent = 4, verbose = True):
    """ Chooses goals based on preferences, by creating goals stochastically and
    rating them according to action costs """

    data = "world"
    domain = "domain.pddl"


    for _ in range(attempts_per_agent):
        if attempts_per_agent < 2:
            goals[:] = []
        random_goals(agents)
    if attempts_per_agent < 2:
        return

    good_goals = []

    for agent in agents:

        all_plans = []

        while len(all_plans) < attempts_per_agent:
            #print(goals[0])
            #agent = agents[0]
            create(data, [agent])
            if verbose:
              print("Wait")
            #time.sleep(2)
            calculating = [questPlanning.plan_quest(agent)]
            too_long = 300 # 5 minutes
            thinking_time = time.clock()
            thinking_timelast = thinking_time
            while not finished_thinking(calculating):
                time.sleep(0.5)
                thinking_timelast += 0.5
                if thinking_time + too_long < thinking_timelast:
                    calculating[0].kill()
                    print("Took too long!")
                    break


            translation, quest = questTranslation.interpret(data)
            if quest == []:
                quest = ['Cluster']
            score = rate_plan(quest)
            if verbose:
              print(quest)
              print(score)
            all_plans.append((score, goals[0], quest))
            goals.pop(0)

            if len(all_plans) == attempts_per_agent:
                all_plans = sorted(all_plans)
                good_goals.append(all_plans[0][1])
                if verbose:
                  print(good_goals[-1],all_plans[0][0])

    if verbose:
      print("Should be empty now:")
      print(goals)
    goals.extend(good_goals)
    if verbose:
      print(goals)

def random_goals(agents,subgoals=3):
    """ Chooses predicates and objects randomly to create goals.
    Assures the objects are compatible with the chosen predicates. """

    #possible_goals = predicates[2:5]+predicates[6:7]+predicates[8:9]+predicates[10:]
    possible_goals = list(predicates_as_goals)
    possible_objects = list(objects)

    for agent in agents:
        agent_goals = []
        for _ in range(random.randint(1,subgoals)):
            agent_goals.append(random.choice(possible_goals))
        #print(agent_goals)
        for j,agent_goal in enumerate(agent_goals):
            goal = agent_goal.split()
            new_goal = ""
            for i,part in enumerate(goal):
                if "?" in part:
                    if "p" in part:
                        part = part.replace("?p", "you")
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
                    elif "m" in part:
                        chosen = "none"
                        while "(monster "+chosen+")" not in facts:
                            chosen = random.choice(possible_objects)
                        part = part.replace("?m",chosen)
                    elif "o" in part:
                        chosen = "none"
                        while "(information "+chosen+")" not in facts:
                            chosen = random.choice(possible_objects)
                        part = part.replace("?o",chosen)

                new_goal += " "+part
            agent_goals[j] = new_goal

        # Makes sure no agent wants the same character dead and alive / doesn't work perfectly yet for 3+ goals
        #print(agent)
        #print(agent_goals)
        contradictionCharacter = ""
        toChange = ""
        for agent_goal in agent_goals:
          #print(agent_goal.split(" "))
          if agent_goal.split(" ")[1] == "(dead" or agent_goal.split(" ")[1] == "(character":
            if contradictionCharacter == "":
              contradictionCharacter = [agent_goal.split(" ")[2],agent_goal.split(" ")[1]]
            else:
              if agent_goal.split(" ")[1] != contradictionCharacter[1] and agent_goal.split(" ")[2] == contradictionCharacter[0]:
                toChange = agent_goal
        if toChange != "":
          agent_goals.remove(toChange)
        #print(agent_goals)
        # End of check

        if len(agent_goals) > 1:
            goals.append("(and"+"".join(agent_goals)+")")
        else:
            goals.append(agent_goals[0])
    #print(goals)


def create(data,agents, quest_per_agent = 1, attempts_per_agent = 4, genesis=False, verbose = False):
    """ Creates task files for the planner """

    if genesis: # Should run only once
        #random_goals(agents)
        choose_goals(data,agents, quest_per_agent, attempts_per_agent, verbose)

    filenames = os.listdir(data)
    for filename in filenames:
        if filename[-5:] == ".soln" or filename[-5:] == ".pddl":
            #if filename != "domain.pddl":
            if "domain" not in filename:
                os.remove(os.path.join(data,filename))

    for i,agent in enumerate(agents):
        if verbose:
          print(agent)
        #time.sleep(1)
        with open(os.path.join(data,agent,agent+".pddl"),"w") as opened_file:
            personal_header = header.replace("agent",agent)
            opened_file.write(personal_header)
            for obj in objects:
                opened_file.write(obj+" ")
            opened_file.write(")\n(:init ")
            for fact in facts:
                opened_file.write(fact+"\n")
            opened_file.write(")\n")

            opened_file.write("(:goal ")

            opened_file.write(goals[i]+")\n")
            opened_file.write("(:metric minimize (total-cost)))")
            #print(goals[i])

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