import os

quests = []
#filenames = os.path.join("metricff\\Metric-FF-v2.1")
solutions = [os.path.join("metricff","Metric-FF-v2.1","lilpeen.soln")]
for solution in solutions:
	with open(solution) as opened_file:
		quest = opened_file.readlines()
		newQuest = []
		foundSteps = 0
		for lines in quest:
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
		quests.append(newQuest)
		
print (quests)
