import os
import sys
import unittest2


here = os.path.dirname(__file__)
loader = unittest2.defaultTestLoader

def suite():
    suite = unittest2.TestSuite()
    for fn in os.listdir(here):
        if fn.startswith("test") and fn.endswith(".py"):
            modname = "unittest2.test." + fn[:-3]
            __import__(modname)
            module = sys.modules[modname]
            suite.addTest(loader.loadTestsFromModule(module))
    return suite


if __name__ == "__main__":
    unittest2.main(defaultTest="suite")
