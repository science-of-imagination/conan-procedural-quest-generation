import os
import random

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
        "(weapon ?w)"]

actions = ["move","kill","giveto", "getfromlocation","given","escort","drop"]

objects = set(["baker", "blacksmith", "troll", "you", "hammer", "wheat",  "ore", "mine", "field", "bakery", "forge"])

facts = set([ "(character baker)",
          "(character blacksmith)",
          "(character troll)",
          "(location forge)",
          "(location bakery)",
          "(location mine)",
          "(location field)",
          "(item ore)",
          "(item wheat)",
          "(item hammer)",
          #"(item nothing)",
          "(weapon hammer)",
          "(has field wheat)",
          "(has mine ore)",
          "(has blacksmith ore)",
          "(has troll hammer)",
          #"(has troll nothing)",
          #"(has baker nothing)",
          #"(has blacksmith nothing)",
          "(at baker bakery)",
          "(at blacksmith forge)",
          "(at troll mine)",
          #"(wants troll wheat)",
          #"(wants baker wheat)",
          #"(wants blacksmith hammer)",
          "(cooperative blacksmith)"
          "(player you)",
          "(at you bakery)"])

allgoals = ["(and (dead troll) (dead blacksmith))","(at you forge)"]

goals = []

def choose_goals(agents):
    """ Chooses some goals out of a list.
    For the moment, it chooses all the goals. """

    for goal in allgoals:
        goals.append(goal)

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
        random_goals(agents)

    filenames = os.listdir(data)
    for filename in filenames:
        if filename[-5:] == ".soln" or filename[-5:] == ".pddl":
            if filename != "domain.pddl":
                os.remove(os.path.join(data,filename))

    for i,agent in enumerate(agents):
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