import time
import sys
from random import random

NUM_RUN=5

class TimeThisDecorator():
   def __init__(self, num_runs):
      self.num_runs = num_runs

   def __call__(self, func, *args, **kwargs):
      def warper(*argv, **vargv):
         # 'ret' contains return value of 'func'
         ret = None
         with self:
            # call 'func' self.num_runs + 1 times and collect time of work
            for n in range(self.num_runs):
               print(" Run {}".format(n))
               t = time.time()
               ret = func(*argv, **vargv)
               delta = time.time() - t
               print(" End {n} after {d:.5f} sec\n".format(d=delta, n=n))
               self.avg_time += delta
         return ret
      return warper

   # return statistic for print
   def __str__(self):
      return "Execution took {a:.5f} sec average of {n} runs"\
             .format( a=self.avg_time, n=self.num_runs )

   def __enter__(self):
      print(">> Enter context")
      print(" Starting {} runs...".format(self.num_runs))
      self.avg_time = 0

   # calc average and print statistic
   def __exit__(self, *args, **kwargs):
      print("<< Exit context")
      self.avg_time /= self.num_runs
      print(self)

@TimeThisDecorator(NUM_RUN)
def func(delay):
   """
   Function just waith for 'sleep' seconds
   Print text and that is all
   """
   sleep = delay/1000 + random()*0.1
   print("Just sleep for {:.5f} sec".format(sleep))
   time.sleep(sleep)

if __name__ == "__main__":
   number = 1000
   try:
      if len(sys.argv) > 1:
         number = int(sys.argv[1])
   except ValueError:
      print("Incorrect value")
      sys.exit(1)

   func(number)
