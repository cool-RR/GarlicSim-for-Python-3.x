import time
import garlicsim
from garlicsim_wx.simulation_packages import life

state = life.make_random_state(40, 15)
new_state = garlicsim.simulate(life, state)

p = garlicsim.Project(life)
n = p.root_this_state(s)
p.crunch_all_leaves(n, 100)
p.sync_crunchers()
time.sleep(10)
p.sync_crunchers()
    