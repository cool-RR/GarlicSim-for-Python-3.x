import time
import garlicsim
from simulation_packages import life


state = life.make_random_state(10, 10)

print(state)

'''
new_state = garlicsim.simulate(life, state, 10)

print(new_state)

result = garlicsim.list_simulate(life, state, 10)

assert result[-1] == new_state
'''


project = garlicsim.Project(life)

root = project.root_this_state(state)

project.crunch_all_leaves(root, 20)

print(project.sync_crunchers())

for i in range(5):
    time.sleep(1)
    print(project.sync_crunchers())



pe