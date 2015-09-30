"""
Recover the toy dataset generated by example/generate_toy/bnmf/generate_bnmtf.py
using the non-probabilistic NMTF, and plot the MSE against timestamps.

We can plot the MSE, R2 and Rp as it converges, on the entire dataset.

We have I=100, J=80, K=5, L=5, and no test data.
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.nmtf_np import NMTF

import numpy, random, scipy, matplotlib.pyplot as plt

##########

input_folder = project_location+"BNMTF/experiments/generate_toy/bnmtf/"

repeats = 10

iterations = 10000
I, J, K, L = 100,80,5,5

init_FG = 'kmeans'
init_S = 'exponential'
expo_prior = 1/10.

# Load in data
R = numpy.loadtxt(input_folder+"R.txt")
M = numpy.ones((I,J))

# Run the VB algorithm, <repeats> times
times_repeats = []
performances_repeats = []
for i in range(0,repeats):
    # Set all the seeds
    numpy.random.seed(3)
    random.seed(4)
    scipy.random.seed(5)
    
    # Run the classifier
    nmtf = NMTF(R,M,K,L) 
    nmtf.initialise(init_S,init_FG,expo_prior)
    nmtf.run(iterations)

    # Extract the performances and timestamps across all iterations
    times_repeats.append(nmtf.all_times)
    performances_repeats.append(nmtf.all_performances)

# Check whether seed worked: all performances should be the same
assert all(numpy.array_equal(performances, performances_repeats[0]) for performances in performances_repeats), \
    "Seed went wrong - performances not the same across repeats!"

# Print out the performances, and the average times
all_times_average = list(numpy.average(times_repeats, axis=0))
all_performances = performances_repeats[0]
print "np_all_times_average = %s" % all_times_average
print "np_all_performances = %s" % all_performances


# Print all time plots, the average, and performance vs iterations
plt.figure()
plt.title("Performance against time")
plt.ylim(0,10)
for times in times_repeats:
    plt.plot(times, all_performances['MSE'])

plt.figure()
plt.title("Performance against average time")
plt.plot(all_times_average, all_performances['MSE'])
plt.ylim(0,10)

plt.figure()
plt.title("Performance against iteration")
plt.plot(all_performances['MSE'])
plt.ylim(0,10)