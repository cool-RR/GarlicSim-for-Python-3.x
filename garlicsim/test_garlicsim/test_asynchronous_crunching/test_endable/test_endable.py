# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


from __future__ import division

import os
import types
import time
import itertools
import cPickle, pickle

import nose

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import math_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc.infinity import Infinity

import garlicsim

import test_garlicsim

from ..shared import MustachedThreadCruncher


def test_endable():
    
    from . import sample_endable_simpacks
    
    # Collecting all the test simpacks:
    simpacks = import_tools.import_all(sample_endable_simpacks).values()
    
    # Making sure that we didn't miss any simpack by counting the number of
    # sub-folders in the `sample_endable_simpacks` folders:
    sample_endable_simpacks_dir = \
        os.path.dirname(sample_endable_simpacks.__file__)
    assert len(path_tools.list_sub_folders(sample_endable_simpacks_dir)) == \
           len(simpacks)
    
    cruncher_types = [
        garlicsim.asynchronous_crunching.crunchers.ThreadCruncher,
        
        # Until multiprocessing shit is solved, this is commented-out:
        #garlicsim.asynchronous_crunching.crunchers.ProcessCruncher
    ]
    
    
    for simpack, cruncher_type in \
        cute_iter_tools.product(simpacks, cruncher_types):
        
        # Making `_settings_for_testing` available:
        import_tools.import_all(simpack)
        
        test_garlicsim.verify_sample_simpack_settings(simpack)
        
        yield check, simpack, cruncher_type

        
def check(simpack, cruncher_type):
    
    # tododoc: note somewhere visible: all simpacks end when they see a
    # world-state with clock reading of 4 or more.
    
    assert simpack._settings_for_testing.ENDABLE is True
    assert simpack._settings_for_testing.CONSTANT_CLOCK_INTERVAL == 1
    
    my_simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    
    assert my_simpack_grokker is garlicsim.misc.SimpackGrokker(simpack)
    # Ensuring caching works.
    
    assert garlicsim.misc.simpack_grokker.get_step_type(
        my_simpack_grokker.default_step_function
    ) == simpack._settings_for_testing.DEFAULT_STEP_FUNCTION_TYPE
    
    step_profile = my_simpack_grokker.build_step_profile()
    deterministic = \
        my_simpack_grokker.settings.DETERMINISM_FUNCTION(step_profile)
    
    state = simpack.State.create_root()
    
    ### Running for short periods synchronically so it doesn't end: ###########
    #                                                                         #
    
    # Whether we run the simulation for one, two, three, or four iterations, the
    # simulation doesn't end.
    prev_state = state
    for i in [1, 2, 3, 4]:
        new_state = garlicsim.simulate(state, i)
        assert new_state.clock >= getattr(prev_state, 'clock', 0)
        prev_state = new_state
    
    result = garlicsim.list_simulate(state, 4)
    for item in result:
        assert isinstance(item, garlicsim.data_structures.State)
        assert isinstance(item, simpack.State)
    
    assert isinstance(result, list)
    assert len(result) == 5
        
    
    iter_result = garlicsim.iter_simulate(state, 4)
        
    assert not hasattr(iter_result, '__getitem__')
    assert hasattr(iter_result, '__iter__')
    iter_result_in_list = list(iter_result)
    del iter_result
    assert len(iter_result_in_list) == len(result) == 5
    
    #                                                                         #
    ### Done running for short periods synchronically so it doesn't end. ######
    
    ### Now, let's run it for longer periods synchronically to make it end: ###
    #                                                                         #
    
    for i in [5, 6, 7]:
        new_state = garlicsim.simulate(state, i)
        assert new_state.clock == 4
    
    result = garlicsim.list_simulate(state, 7)
    
    assert isinstance(result, list)
    assert len(result) == 5
        
    
    iter_result = garlicsim.iter_simulate(state, 7)
        
    assert not hasattr(iter_result, '__getitem__')
    assert hasattr(iter_result, '__iter__')
    iter_result_in_list = list(iter_result)
    del iter_result
    assert len(iter_result_in_list) == len(result) == 5
        
    #                                                                         #
    ### Done running for longer periods synchronically to make it end. ########
    
    ### Setting up a project to run asynchronous tests:
    
    project = garlicsim.Project(simpack)
        
    project.crunching_manager.cruncher_type = cruncher_type
    
    assert project.tree.lock._ReadWriteLock__writer is None
    
    root = project.root_this_state(state)
    
    ### Running for short periods asynchronically so it doesn't end: ##########
    #                                                                         #
    
    project.begin_crunching(root, 4)

    total_nodes_added = 0    
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
        
    assert total_nodes_added == 4
    
    assert len(project.tree.nodes) == 5
    assert len(project.tree.roots) == 1
    
    paths = project.tree.all_possible_paths()
    
    assert len(paths) == 1
    
    (my_path,) = paths
        
    assert len(my_path) == 5
    
    node_1 = my_path[1]
    assert node_1.state.clock == 1
    
    node_2 = project.simulate(node_1, 3)
    
    assert len(project.tree.nodes) == 8
    assert len(project.tree.roots) == 1
    
    assert len(project.tree.all_possible_paths()) == 2
    
    node_3 = my_path.next_node(node_1)
    
    #                                                                         #
    ### Done running for short periods asynchronically so it doesn't end. #####
    
    ### Now, let's run it for longer periods asynchronically to make it end: ##
    #                                                                         #
    
    assert node_3.state.clock == 2
    project.begin_crunching(node_3, 3)
    
    total_nodes_added = 0
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
    assert total_nodes_added == 2 # Would have been 3 without the end!
    
    # So now `node_3`'s path has an end:
    ended_path = node_3.all_possible_paths()[1]
    isinstance(ended_path, garlicsim.data_structures.Path)
    (end,) = ended_path.get_ends_of_last_node() # (Asserting there's one end.)
    assert isinstance(end, garlicsim.data_structures.End)
    
    assert len(project.tree.nodes) == 10
    
    paths = project.tree.all_possible_paths()
    assert len(paths) == 3
    
    assert [len(p) for p in paths] == [5, 5, 5]
    
    
    # Ensuring buffer from `node_3` won't add a single node since we have a path
    # to an end:
    project.ensure_buffer(node_3, 10)
    project.ensure_buffer(node_3, 1000)
    project.ensure_buffer(node_3, Infinity)
    total_nodes_added = 0    
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
    assert len(project.tree.nodes) == 10
    
    
    
    plain_root = project.create_root()
    
    assert len(project.tree.roots) == 2
    assert len(project.tree.all_possible_paths()) == 4
    assert len(project.tree.nodes) == 11
    
    iterator = project.iter_simulate(node_1, 10)
    new_node = iterator.next()
    assert new_node is node_1
    assert len(project.tree.nodes) == 11
    
    assert project.tree.lock._ReadWriteLock__writer is None
    
    new_node = iterator.next()
    assert new_node is not node_1
    assert new_node.parent is node_1
    assert len(project.tree.nodes) == 12
    
    bunch_of_new_nodes = tuple(iterator)
    consecutive_pairs = cute_iter_tools.consecutive_pairs(bunch_of_new_nodes)
    for parent_node, kid_node in consecutive_pairs:
        assert project.tree.lock._ReadWriteLock__writer is None
        assert isinstance(parent_node, garlicsim.data_structures.Node)
        assert isinstance(kid_node, garlicsim.data_structures.Node)
        assert parent_node.children == [kid_node]
        assert kid_node.parent is parent_node
        
    assert len(project.tree.nodes) == 14

        
        
    
    
        
    
    
    