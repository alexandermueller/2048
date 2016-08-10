import os.path

def setAssignments(filename, assignments):
    assignmentsFile = open(filename, 'w')
    assignmentsList = []

    for assignment in assignments.keys():
        assignmentsList.append('%s:%s' % (assignment, assignments[assignment]))

    assignmentsFile.write('\n'.join(assignmentsList))
    assignmentsFile.close()

def getAssignments(filename, defaults):
    assignments = defaults
    
    if os.path.isfile(filename):
        assignmentsFile = open(filename, 'r')

        for line in assignmentsFile.read().split('\n'):
            assignment = line.split(':')
            if len(assignment) == 2: 
                assignments[assignment[0]] = str(assignment[1])
    
        assignmentsFile.close()
    
    return assignments

def setStats(stats):
    setAssignments('Stats.txt', stats)

def getStats(lowest):    
    stats = getAssignments('Stats.txt', lowest)
    
    for stat in stats.keys():
        stats[stat] = int(stats[stat])

    return stats

def setSettings(settings):
    setAssignments('GameSettings.txt', settings)

def getSettings(defaults):    
    return getAssignments('GameSettings.txt', defaults)

def setHashTable(table):
    setAssignments('GameStateHashTable.txt', table)

def getHashTable(defaultTable):
    return getAssignments('GameStateHashTable.txt', defaultTable)