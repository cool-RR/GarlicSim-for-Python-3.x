import time
import garlicsim
from garlicsim.bundled.simulation_packages import life

if __name__ == '__main__':
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
    
    project.begin_crunching(root, 100)
    
    print(project.sync_crunchers())
    
    while True:
        time.sleep(0.5)
        j = project.sync_crunchers()
        print(j)
        if j == 0: break
    
    
    