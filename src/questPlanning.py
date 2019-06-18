import os
import subprocess

heuristic = "astar(ipdb())"
def plan_quest(agent):

    os.chdir(os.path.join("world",agent))
    with open("garbage","w") as garbage:
        subprocess.call(["C:\cygwin\\bin\python2.7.exe","C:\cygwin\home\Vincent\Fast-Downward-134116d39300\src\\translate\\translate.py","domain"+agent+".pddl", agent+".pddl"], stdout=garbage)
    with open("output.sas","r") as outputsas:
        with open("garbage2","w") as garbage2:
            subprocess.call(["C:\cygwin\home\Vincent\Fast-Downward-134116d39300\src\preprocess\preprocess"], stdin=outputsas, stdout=garbage2)
    with open("output","r") as output:
        with open(os.path.join("..",agent+".soln"),"w") as solution:
            calc = subprocess.Popen(['C:\cygwin\home\Vincent\Fast-Downward-134116d39300\src\search\downward-release.exe', '--search', heuristic], stdin=output, stdout=solution)
    os.chdir("..")
    os.chdir("..")
    return calc