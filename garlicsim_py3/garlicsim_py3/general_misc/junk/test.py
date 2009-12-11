import time

import garlicsim_py3
from garlicsim_py3_wx.simulation_packages import life

if __name__ == "__main__":
        
    state = life.make_random_state()
    
    project = garlicsim_py3.Project(life)
    
    node = project.root_this_state(state)
    
    project.ensure_buffer(node, 100)
    
    print((project.sync_crunchers()))
    
    time.sleep(5)
    
    print((project.sync_crunchers()))