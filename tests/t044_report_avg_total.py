#!/usr/bin/env python

from runtest import TestBase

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'sort', """
   Total avg   Total min   Total max  Function
  ==========  ==========  ==========  ====================
   11.378 ms   11.378 ms   11.378 ms  main
   10.537 ms   10.537 ms   10.537 ms  bar
   10.288 ms   10.288 ms   10.288 ms  usleep
  120.947 us  120.605 us  121.290 us  foo
   39.967 us   39.801 us   40.275 us  loop
    0.701 us    0.701 us    0.701 us  __monstartup
    0.270 us    0.270 us    0.270 us  __cxa_atexit
""")

    def prepare(self):
        self.subcmd = 'record'
        return self.runcmd()

    def setup(self):
        self.subcmd = 'report'
        self.option = '--avg-total'

    def sort(self, output):
        """ This function post-processes output of the test to be compared .
            It ignores blank and comment (#) lines and remaining functions.  """
        result = []
        for ln in output.split('\n'):
            if ln.strip() == '':
                continue
            line = ln.split()
            if line[1] == 'avg':
                continue
            if line[0].startswith('='):
                continue
            # A report line consists of following data
            # [0]        [1]   [2]        [3]   [4]        [5]   [6]
            # avg_total  unit  min_total  unit  max_total  unit  function
            if line[-1].startswith('__'):
                continue
            result.append(line[-1])

        return '\n'.join(result)
