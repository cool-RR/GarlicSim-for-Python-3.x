import time
import garlicsim_py3
from garlicsim_py3.bundled.simulation_packages import life

state = life.make_random_state(40, 15)
print(state)
new_state = garlicsim_py3.simulate(life, state)

p = garlicsim_py3.Project(life)
n = p.root_this_state(state)
p.ensure_buffer(n, 100)
print(p.sync_crunchers())
time.sleep(10)
print(p.sync_crunchers())
    