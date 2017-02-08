"""
Run the line search method for finding the best value for K for BNMF.
We use the parameters for the true priors.

The BIC tends to give overly simple models, preferring K=1 oftentimes.
The log likelihood and AIC tend to peak at the true K if the correct priors are
given (this has to do with converging to a good local minimum).

If we give the wrong prior (true/5) we still obtain good convergence (with 
true*5 all values get pushed to 0, leading to terrible solutions), and we get
a nice peak for the log likelihood and AIC around the true K.
"""

project_location = "/Users/thomasbrouwer/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.data_toy.bnmf.generate_bnmf import generate_dataset, try_generate_M
from BNMTF.code.cross_validation.line_search_bnmf import LineSearch
from BNMTF.code.models.bnmf_vb_optimised import bnmf_vb_optimised

import numpy, matplotlib.pyplot as plt

##########

restarts = 5
iterations = 1000

I, J = 100, 80
true_K = 10
values_K = range(1,20+1)

fraction_unknown = 0.1
attempts_M = 100

alpha, beta = 1., 1. #1., 1.
tau = alpha / beta
lambdaU = numpy.ones((I,true_K))
lambdaV = numpy.ones((J,true_K))

classifier = bnmf_vb_optimised
initUV = 'random'

# Generate data
(_,_,_,_,R) = generate_dataset(I,J,true_K,lambdaU,lambdaV,tau)
M = numpy.ones((I,J))
#M = try_generate_M(I,J,fraction_unknown,attempts_M)

# Run the line search. The priors lambdaU and lambdaV need to be a single value (recall K is unknown)
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU[0,0]/10, 'lambdaV':lambdaV[0,0]/10 }
line_search = LineSearch(classifier,values_K,R,M,priors,initUV,iterations,restarts)
line_search.search()

# Plot the performances of all three metrics
metrics = ['loglikelihood', 'BIC', 'AIC', 'MSE', 'ELBO']
for metric in metrics:
    plt.figure()
    plt.plot(values_K, line_search.all_values(metric), label=metric)
    plt.legend(loc=3)
    
# Also print out all values in a dictionary
all_values = {}
for metric in metrics:
    all_values[metric] = line_search.all_values(metric)
    
print "all_values = %s" % all_values

'''
all_values = {'MSE': [9.6549057058769172, 6.9884484321573099, 5.1934558411893263, 4.0992884584119622, 3.2240598340019346, 2.4818906465963311, 1.8406504508732986, 1.3502204910226565, 1.0333349580316775, 0.78017988120303972, 0.75361070313227285, 0.72978226838232485, 0.7099944773500656, 0.69208188151852712, 0.6725243354242475, 0.65582783054509486, 0.63850413370173831, 0.62299533285704889, 0.60796336865454281, 0.59211139754569109], 'loglikelihood': [-20422.878028449726, -19133.050411760163, -17950.489043043988, -17011.744324390602, -16060.301690117441, -15024.660282332354, -13842.706832984462, -12619.297660607001, -11566.289337162721, -10461.721305930792, -10340.456751510523, -10230.967539005962, -10140.60032716368, -10057.810701562652, -9965.5778556505502, -9887.236373074742, -9803.3442204645653, -9729.0856510921694, -9657.9307609909029, -9581.8361432246875], 'AIC': [41205.756056899452, 38986.100823520326, 36980.978086087976, 35463.488648781204, 33920.603380234883, 32209.320564664707, 30205.413665968925, 28118.595321214001, 26372.578674325443, 24523.442611861585, 24640.913503021045, 24781.935078011924, 24961.20065432736, 25155.621403125304, 25331.1557113011, 25534.472746149484, 25726.688440929131, 25938.171302184339, 26155.861521981806, 26363.672286449375], 'BIC': [42463.451484618607, 41501.491678958635, 40754.06436924544, 40494.270359657821, 40209.080518830655, 39755.493130979637, 39009.281660003013, 38180.158742967244, 37691.83752379784, 37100.39688905314, 38475.563207931751, 39874.28021064178, 41311.241214676382, 42763.35739119348, 44196.587127088424, 45657.599589655962, 47107.510712154763, 48576.689001129133, 50052.07464864575, 51517.580840832481]}
all_values_2 = {'ELBO': [-20559.658764958851, -20424.120723364082, -20209.284045284217, -20012.561227029946, -19889.319197829805, -19657.311622654452, -19473.490336818944, -19267.048016094119, -18912.115938037805, -18329.50591698091, -18809.334650368506, -19304.691887856607, -19767.555234593932, -20268.193885291275, -20773.991056688828, -21189.283504724757, -21734.29803683488, -22241.765567956845, -22688.476168265963, -23197.727483736431], 'MSE': [8.2790315388098428, 6.8495626167282246, 5.5410598879469743, 4.4761883559025826, 3.659717059598115, 2.8588525895825385, 2.2424246746433272, 1.7248753317244685, 1.246168045195883, 0.815548276624941, 0.78717618569773851, 0.76406277232904585, 0.74314774728313038, 0.72298044653208815, 0.70351739691239468, 0.68246368859804385, 0.66522455223188603, 0.64721761219430385, 0.63288920223204137, 0.61885747450694928], 'loglikelihood': [-19807.918073897767, -19052.750182694072, -18209.90007578626, -17363.528085767659, -16566.512224393806, -15589.445367408904, -14630.398834182259, -13595.779982957489, -12313.867350887318, -10640.278910973106, -10516.447007678722, -10415.58251379443, -10323.88595046007, -10235.123139857769, -10145.813053824566, -10051.283796237665, -9972.6960754446864, -9887.9220256319513, -9825.8530977896717, -9763.1045072060951], 'AIC': [39975.836147795533, 38825.500365388143, 37499.800151572519, 36167.056171535318, 34933.024448787612, 33338.890734817804, 31780.797668364517, 30071.559965914978, 27867.734701774636, 24880.557821946211, 24992.894015357444, 25151.165027588861, 25327.771900920139, 25510.246279715539, 25691.626107649132, 25862.56759247533, 26065.392150889373, 26255.844051263903, 26491.706195579343, 26726.20901441219], 'BIC': [41233.531575514688, 41340.891220826452, 41272.886434729982, 41197.837882411935, 41221.501587383391, 40885.063301132737, 40584.665662398605, 40133.123387668216, 39186.993551247033, 37457.512099137763, 38827.54372026815, 40243.510160218721, 41677.812461269161, 43117.982267783707, 44557.057523436459, 45985.694435981815, 47446.214422115008, 48894.3617502087, 50387.919322243295, 51880.117568795293]}
all_values_3 = {'ELBO': [-21125.064897711014, -20571.989577330842, -20272.991198774445, -19983.445693841713, -19622.838854008056, -19340.341371621391, -19109.018736319384, -18765.358979890094, -18492.709811672143, -18265.189938235635, -18746.168582928916, -19234.968068255708, -19746.002103726423, -20193.629857859352, -20691.913809237118, -21142.636408613173, -21645.889637194483, -22028.721629372103, -22560.665261581536, -23127.572735539066], 'MSE': [9.5617648094780243, 7.0945237268428203, 5.5998202391189027, 4.4093450006897905, 3.3595475173542382, 2.58170272484913, 1.9959541205773208, 1.4525652137451439, 1.0722982561501269, 0.78871565269619859, 0.76150405751828432, 0.73841586779604029, 0.71740313575781844, 0.69533903209761327, 0.67670301646851916, 0.65815549982083399, 0.64408404818885046, 0.62312564604417708, 0.6095336857263024, 0.59581504486061132], 'loglikelihood': [-20384.102841284785, -19193.345995658739, -18252.138615674099, -17303.218849775716, -16224.364899192669, -15182.082177098875, -14166.12428681106, -12910.489348603898, -11714.929726037997, -10507.22536100692, -10385.095622822424, -10281.099569057968, -10185.462983132151, -10082.587333208474, -9996.9530910146896, -9908.2977089475735, -9843.2020683396913, -9741.6459243387108, -9678.735610944299, -9613.8831117820064], 'AIC': [41128.205682569569, 39106.691991317479, 37584.277231348198, 36046.437699551432, 34248.729798385335, 32524.16435419775, 30852.248573622121, 28700.978697207796, 26669.859452075994, 24614.45072201384, 24730.191245644848, 24882.199138115935, 25050.925966264302, 25205.174666416948, 25393.906182029379, 25576.595417895147, 25806.404136679383, 25963.291848677422, 26197.471221888598, 26427.766223564013], 'BIC': [42385.901110288723, 41622.082846755788, 41357.363514505661, 41077.21941042805, 40537.206936981114, 40070.33692051268, 39656.116567656209, 38762.542118961035, 37989.118301548391, 37191.404999205392, 38564.840950555554, 39974.544270745799, 41400.966526613323, 42812.910654485124, 44259.337597816702, 45699.722261401628, 47187.226407905022, 48601.809547622215, 50093.684348552546, 51581.674777947119]}
'''