import garlicsim_py3
from garlicsim_py3.bundled.simulation_packages import queue

s = queue.make_plain_state()
l = garlicsim_py3.list_simulate(queue, s, 100)
