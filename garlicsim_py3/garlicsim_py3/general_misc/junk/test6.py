import time
import garlicsim_py3
from garlicsim_py3.bundled.simulation_packages import life
from garlicsim_py3.bundled.simulation_packages import prisoner
from garlicsim_py3.bundled.simulation_packages import _history_test

simpack = life

if __name__ == '__main__':
    
    state = simpack.make_random_state(10, 10)
    
    
    print(state)
    
    
    new_state = garlicsim_py3.simulate(simpack, state, 10)
    
    print(new_state)
    
    result = garlicsim_py3.list_simulate(simpack, state, 10)
    
    assert result[-1] == new_state
    
    print([thing.clock for thing in result])