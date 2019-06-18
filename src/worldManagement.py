import os
import random
import subprocess
import questTranslation
import questPlanning
#import adventuresawait
import math
import time

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

objects = set(["baker", "king", "lumberjack", "blacksmith", "merchant", "guard", "daughter", "troll", "wolf", "slime", "you", "hammer", "wheat", "sword", "spellbook", "ore", "castle", "village", "cave", "field", "bakery", "forge", "forest", "shop", "fireball", "gel", "pelt", "secret"])

facts = set([ "(character baker)",
          "(character blacksmith)",
          "(character king)",
          "(character lumberjack)",
          "(character merchant)",
          "(character guard)",
          "(character daughter)",
          "(monster troll)",
          "(monster wolf)",
          "(monster slime)",
          "(item pelt)",
          "(item gel)",
          "(has wolf pelt)",
          "(has slime gel)",
          "(location forge)",
          "(location bakery)",
          "(location cave)",
          "(location field)",
          "(location castle)",
          "(location village)",
          "(location forest)",
          "(location shop)",
          "(item ore)",
          "(item wheat)",
          "(item hammer)",
          "(item sword)",
          "(item spellbook)",
          "(information fireball)",
          "(has spellbook fireball)",
          "(information secret)",
          "(has king secret)",
          "(weapon sword)",
          "(weapon hammer)",
          "(has field wheat)",
          "(has cave ore)",
          "(has blacksmith hammer)",
          "(has troll hammer)",
          "(has you sword)",
          "(at baker bakery)",
          "(at blacksmith forge)",
          "(at troll village)",
          "(at lumberjack village)",
          "(at you bakery)",
          "(at king field)",
          "(at merchant shop)",
          "(at guard shop)",
          "(at daughter cave)",
          "(at wolf village)",
          "(at slime village)",
          "(has castle spellbook)",
          "(cooperative baker)",
          "(player you)",
          "(captive troll daughter)",
          "(adjacent castle village)",
          "(adjacent village field)",
          "(adjacent village bakery)",
          "(adjacent village forge)",
          "(adjacent village forest)",
          "(adjacent village shop)",
          "(adjacent field cave)",
          "(= (total-cost) 0)"])

#allgoals = ["(and (dead troll) (dead blacksmith))","(at you forge)"]

goals = []

preferences = dict()
preferences["baker"] = ["+kill","-exchange","-use","+escort"]
preferences["guard"] = ["-damage","-take","-report","+escort","-defend"]
preferences["king"] = ["-kill","-spy","-read","-move"]
preferences["lumberjack"] = ["-getfromlocation","-escort","-giveto","+move", "-kill"]
preferences["blacksmith"] = ["+escort", "-getfromlocation", "-move"]
preferences["merchant"] = ["-exchange", "-take", "+explore", "+spy"]
preferences["daughter"] = ["-kill", "-spy", "-take", "-stealth","-move"]

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
            if 'Plan cost: ' in line:
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

    scores = []

    for agent in agents:
        
        all_plans = []

        while len(all_plans) < attempts_per_agent:
            #print(goals[0])
            #agent = agents[0]
            create(data, [agent])
            if verbose:
              print("Wait")
            time.sleep(2)
            
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


            translation, quest, NPCNames = questTranslation.interpret(data)
            if quest == []:
                quest = ['Cluster']
            score = rate_plan(quest)
            if verbose:
              print(quest)
              print(score)
            all_plans.append((score, goals[0], quest))
            goals.pop(0)
            # Maybe make it choose the longest quest in case of equal scores?
            if len(all_plans) == attempts_per_agent:
                all_plans = sorted(all_plans)
                good_goals.append(all_plans[0][1])
                scores.append(all_plans[0][0])
                if verbose:
                  print(good_goals[-1],all_plans[0][0])
    
    if verbose:
      print("Should be empty now:")
      print(goals)
    goals.extend(good_goals)
    if verbose:
      print(goals)
      print(scores)


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


def create(data,agents, quest_per_agent = 1, attempts_per_agent = 4, genesis=False, verbose=True):
    """ Creates task files for the planner """

    if genesis: # Should run only once. change the attempt per agent.
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
            print(goals[i])

def update(data,action,agents,listOfActions):
    """ Updates the world facts and rewrites task files """
    # (move you bakery village)
    action = action.split()
    actionName = action[0] #this would be move

    for actions in listOfActions:
        if actions.name[0] == actionName:
            chosenAction = actions #chosenAction is therefore the object corresponding to the action



    parameterCorrespondence = {}
    for i,parameter in enumerate(chosenAction.parameters[0]):
        parameterCorrespondence[parameter] = action[i+1].replace(")","") #{(?p, you), (?to, village), (blalba)}




    for effects in chosenAction.effect[0]:
        effects = effects.replace(")","")
        effects = effects.replace("(","")

        toRemoveFlag = False
        #effects = '(has ?loc ?i)'
        currentEffect = effects.split()
        predicate = currentEffect[0]
        if predicate == "not":
            toRemoveFlag = True
            predicate = currentEffect[1]

        finalEffect = []
        for word in currentEffect:
            if word in parameterCorrespondence.keys():
                finalEffect.append(parameterCorrespondence[word])

        toAddorRemove = "("+predicate+" "+" ".join(finalEffect)+")"
        if toRemoveFlag:
            facts.remove(toAddorRemove)
        else:
            facts.add(toAddorRemove)

        print(toAddorRemove)



    '''
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
'''
    create(data,agents)