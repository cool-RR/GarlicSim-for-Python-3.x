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
    
    # project.crunching_manager.Cruncher = \
    #     garlicsim.asynchronous_crunching.crunchers.CruncherProcess
    
    root = project.root_this_state(state)
    
    meow = 100
    
    project.begin_crunching(root, meow)
    
    print(project.sync_crunchers())
    
    count = 0
    while True:
        time.sleep(0.05)
        j = project.sync_crunchers()
        print(j)
        count += j
        if count == meow: break
    
    
    print(root.get_all_leaves().popitem()[0].state)