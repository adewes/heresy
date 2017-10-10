import libraries
import sys
from test_cases import test_cases
import time

libraries_to_test = ['jinja2','heresy','django']


if __name__ == '__main__':

    test_runners = {}

    for library_name in libraries_to_test:
        try:
            library = __import__('libraries.%s_runner' % library_name,fromlist = ['test'])
            test_runners[library_name] = library.test
        except ImportError:
            print "Skipping %s" % library_name

    for test_case_name,test_case_module in test_cases.items():
        print test_case_name
        times = {}
        for library,test_runner in test_runners.items():
            if hasattr(test_case_module,'%s' % library):
                repetitions = test_case_module.repetitions
                params = getattr(test_case_module,'%s' % library)
                test_function = test_runner(params['template_name'],params['context'],params['templates'])
                start = time.time()
                for i in range(0,repetitions):
                    result = test_function()
                end = time.time()
                print library,":",end-start
