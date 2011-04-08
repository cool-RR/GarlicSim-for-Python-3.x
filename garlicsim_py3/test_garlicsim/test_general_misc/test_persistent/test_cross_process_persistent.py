# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Testing module for `garlicsim.general_misc.persistent.CrossProcessPersistent`.
'''

from __future__ import with_statement

import multiprocessing
import copy
import pickle
import abc

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import cute_testing
from garlicsim.general_misc import queue_tools

from garlicsim.general_misc import persistent
from garlicsim.general_misc.persistent import CrossProcessPersistent


class AbstractCrossProcessPersistent(CrossProcessPersistent):
    '''
    An abstract cross-process persistent.
    
    This is needed to test CPP's interaction with `__abstractmethods__`.
    '''
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def f(self):
        pass
    
class A(AbstractCrossProcessPersistent):
    def f(self):
        pass
    



def test():
    '''Test the basic workings of `CrossProcessPersistent`.'''
    checkers = [_check_deepcopying, _check_process_passing]
    cross_process_persistent_classes = [A, CrossProcessPersistent]
    
    iterator = cute_iter_tools.product(
        checkers,
        cross_process_persistent_classes,
    )
    
    for checker, cross_process_persistent_class in iterator:
        yield checker, cross_process_persistent_class
    
        
def _check_deepcopying(cross_process_persistent_class):
    '''Test that CPPs maintain their identities when faux-deepcopied.'''
    cross_process_persistent = cross_process_persistent_class()
    cross_process_persistent_deepcopy = copy.deepcopy(cross_process_persistent)
    assert cross_process_persistent_deepcopy is not cross_process_persistent
    
    cross_process_persistent_faux_deepcopy = copy.deepcopy(
        cross_process_persistent,
        persistent.DontCopyPersistent()
    )
    assert cross_process_persistent_faux_deepcopy is cross_process_persistent
    
    
class Process(multiprocessing.Process):
    '''Process used when testing to assert CPPs' identities.'''
    
    def __init__(self):
        multiprocessing.Process.__init__(self)
        
        self.work_queue = multiprocessing.Queue()
        '''Queue for receiving `(index, cpp)` pairs from main process.'''
        
        self.processed_items_queue = multiprocessing.Queue()
        '''Queue for giving back the main process the items it gives us.'''
        
        self.message_queue = multiprocessing.Queue()
        '''Queue for reporting to the main process about actions we do.'''
        
        self.library = {}
        '''Dict mapping from ints to CPPs.'''
        
    def run(self):
        for number, item in queue_tools.iterate(self.work_queue, block=True):
            if number in self.library:
                assert self.library[number] is item
                other_items = [value for (key, value) in self.library.items()
                               if key != number]
                for other_item in other_items:
                    assert other_item is not item
                self.processed_items_queue.put(item)
                self.message_queue.put('Asserted identity.')
            else: # number not in self.library
                self.library[number] = item
                self.processed_items_queue.put(item)
                self.message_queue.put('Stored object.')
        
    
def _check_process_passing(cross_process_persistent_class):
    '''
    Test that CPPs maintain their identities when passed between processes.
    '''
    
    cpp_1 = cross_process_persistent_class()
    cpp_2 = cross_process_persistent_class()
    cpp_3 = cross_process_persistent_class()
    
    process = Process()
    process.start()
    
    process.work_queue.put((1, cpp_1))
    assert process.message_queue.get(timeout=10) == 'Stored object.'
    assert process.processed_items_queue.get(timeout=10) is cpp_1
    
    process.work_queue.put((1, cpp_1))
    assert process.message_queue.get(timeout=10) == 'Asserted identity.'
    assert process.processed_items_queue.get(timeout=10) is cpp_1
    
    process.work_queue.put((2, cpp_2))
    assert process.message_queue.get(timeout=10) == 'Stored object.'
    assert process.processed_items_queue.get(timeout=10) is cpp_2
    
    process.work_queue.put((1, cpp_1))
    assert process.message_queue.get(timeout=10) == 'Asserted identity.'
    assert process.processed_items_queue.get(timeout=10) is cpp_1
    
    process.work_queue.put((2, cpp_2))
    assert process.message_queue.get(timeout=10) == 'Asserted identity.'
    assert process.processed_items_queue.get(timeout=10) is cpp_2
    
    process.work_queue.put((3, cpp_3))
    assert process.message_queue.get(timeout=10) == 'Stored object.'
    assert process.processed_items_queue.get(timeout=10) is cpp_3
    
    process.work_queue.put((3, cpp_3))
    assert process.message_queue.get(timeout=10) == 'Asserted identity.'
    assert process.processed_items_queue.get(timeout=10) is cpp_3
    
    process.work_queue.put((1, cpp_1))
    assert process.message_queue.get(timeout=10) == 'Asserted identity.'
    assert process.processed_items_queue.get(timeout=10) is cpp_1
    
    process.terminate()


def test_personality():
    '''Test that a `CrossProcessPersistent` has a `.personality`.'''
    a = A()
    cross_process_persistent = CrossProcessPersistent()
    assert isinstance(a.personality,
                      persistent.Personality)
    assert isinstance(cross_process_persistent.personality,
                      persistent.Personality)
    
    
def test_helpful_warnings_for_old_protocols():
    '''
    Test that helpful errors are given when trying to pickle with old protocol.
    '''
    pickle_modules = [pickle]
    cross_process_persistents = [A(), CrossProcessPersistent()]
    old_protocols = [0, 1]
    
    iterator = cute_iter_tools.product(
        pickle_modules,
        cross_process_persistents,
        old_protocols
    )
    
    for pickle_module, cross_process_persistent, old_protocol in iterator:
        yield (_check_helpful_warnings_for_old_protocols, 
               pickle_module,
               cross_process_persistent,
               old_protocol)
            
    
def _check_helpful_warnings_for_old_protocols(pickle_module,
                                              cross_process_persistent,
                                              old_protocol):
    '''
    Test that helpful errors are given when trying to pickle with old protocol.
    '''
    assert old_protocol < 2
    with cute_testing.RaiseAssertor(text=('protocol %s' % old_protocol)):
        pickle_module.dumps(cross_process_persistent,
                            protocol=old_protocol)