"""
Recover the toy dataset generated by example/generate_toy/bnmf/generate_bnmf.py
using VB.

We can plot the MSE, R2 and Rp as it converges.

We have I=100, J=80, K=10, and no test data.
We give flatter priors (1/10) than what was used to generate the data (1).
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmf_gibbs_optimised import bnmf_gibbs_optimised
from ml_helpers.code.mask import calc_inverse_M

import numpy, matplotlib.pyplot as plt

##########

input_folder = project_location+"BNMTF/experiments/generate_toy/bnmf/"

iterations = 200
burn_in = 180
thinning = 2

init_UV = 'random'
I, J, K = 100, 80, 10

alpha, beta = 1., 1.
lambdaU = numpy.ones((I,K))/10
lambdaV = numpy.ones((J,K))/10
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }

# Load in data
R = numpy.loadtxt(input_folder+"R.txt")
M = numpy.ones((I,J))

M_test = calc_inverse_M(numpy.loadtxt(input_folder+"M.txt"))

# Run the Gibbs sampler
BNMF = bnmf_gibbs_optimised(R,M,K,priors)
BNMF.initialise(init_UV)
BNMF.run(iterations)

taus = BNMF.all_tau
Us = BNMF.all_U
Vs = BNMF.all_V

# Plot tau against iterations to see that it converges
f, axarr = plt.subplots(3, sharex=True)
x = range(1,len(taus)+1)
axarr[0].set_title('Convergence of values')
axarr[0].plot(x, taus)
axarr[0].set_ylabel("tau")
axarr[1].plot(x, Us[:,0,0])    
axarr[1].set_ylabel("U[0,0]")
axarr[2].plot(x, Vs[:,0,0]) 
axarr[2].set_ylabel("V[0,0]")
axarr[2].set_xlabel("Iterations")

# Approximate the expectations
(exp_U, exp_V, exp_tau) = BNMF.approx_expectation(burn_in,thinning)

# Also measure the performances
performances = BNMF.predict(M_test,burn_in,thinning)
print performances

# Extract the performances across all iterations
print "gibbs_all_performances = %s" % BNMF.all_performances

'''
gibbs_all_performances = {'R^2': [-662.9645488569937, -13.400122105593619, 0.17645193260128889, 0.6127782497604785, 0.7160099989922473, 0.799814985379875, 0.8550238723756092, 0.8851742486400449, 0.9045722692416157, 0.9164347408803937, 0.9236840810072953, 0.9297835079407162, 0.9355958044926235, 0.9392973352689515, 0.9424581113630625, 0.9444747099045256, 0.9465151361759567, 0.9485159678073823, 0.9491306188626712, 0.9501370627729735, 0.9516156973704143, 0.9525007119739566, 0.9533749694191433, 0.9541311587947142, 0.9550496291734387, 0.956379709543472, 0.9567269656200018, 0.9575168811827212, 0.9585182258460548, 0.9599378612640316, 0.9612796410631373, 0.961737954848491, 0.963070417460247, 0.9638160813763882, 0.9646865044019588, 0.9653743013523047, 0.9656482136757404, 0.9671666565754226, 0.9673712789626085, 0.9680438410991379, 0.9681511996606362, 0.968124655182077, 0.9685789831292737, 0.9685698791021364, 0.9688806661436373, 0.9691126546216264, 0.969591130150267, 0.9696148703746454, 0.9697765567805054, 0.9698402059637805, 0.9700546706960205, 0.9698037372627691, 0.9700401609405201, 0.9702163875362128, 0.969882716871385, 0.970283850618909, 0.9701937047420437, 0.9704534318958341, 0.9702202892856838, 0.9697828656570893, 0.9706386434854384, 0.9705085619239673, 0.9706182157415084, 0.9708256784364551, 0.9710764562903704, 0.9710075142726129, 0.9708353952455039, 0.9709331764462326, 0.9710071161557902, 0.9713005025262038, 0.9715869504052802, 0.971659854980303, 0.9714568128764176, 0.9719050358554164, 0.9724060939978977, 0.9722569492280279, 0.9720255908865315, 0.9723860693790372, 0.9724102719397947, 0.9725964825118425, 0.9725020963895517, 0.972489550018548, 0.9728747978627297, 0.9724732600719914, 0.9723193208686822, 0.9728163682146905, 0.9726870751424986, 0.973004933686741, 0.97277255554827, 0.9727858642175812, 0.9727510852975857, 0.972815451951981, 0.9729410188432301, 0.973056579849678, 0.9729231302691518, 0.973044390031468, 0.9728730907500651, 0.9730371793626005, 0.9730538678908851, 0.9734646162540909, 0.9731357254561516, 0.9732002301298573, 0.973213068415841, 0.9733230900838107, 0.9734592172300852, 0.9732950841173753, 0.9733187281458402, 0.9733613704282363, 0.9733041752541992, 0.9734447422317685, 0.9734403844320773, 0.9737299611116508, 0.9738350446907542, 0.9737207575087727, 0.9737620393919808, 0.9733917044385539, 0.9736063026596005, 0.9733121789189136, 0.9734918180005631, 0.9733402060693486, 0.9738321258675074, 0.9735330545881331, 0.9739889076457805, 0.9740587034980054, 0.9740248815774921, 0.9739553996681505, 0.9739830068035329, 0.974086208464017, 0.9740193918961417, 0.9739298751678279, 0.9739440348762471, 0.9742561307176453, 0.9740948461367266, 0.9740159522162681, 0.9738337528188152, 0.9739035797422545, 0.9737619319032488, 0.9741174414839576, 0.974242714871886, 0.9740222468191709, 0.9737633948480687, 0.9739141222608309, 0.973777254453234, 0.9739636841217783, 0.9740549792888916, 0.9741498259553937, 0.9740229234247583, 0.9744360985909937, 0.9742924496773906, 0.9744291130620703, 0.9745703659073174, 0.9744194223440288, 0.9741908668331777, 0.9742901628371125, 0.9742589756077683, 0.9743963390625072, 0.9739869182347995, 0.9741009817774022, 0.9742231750753376, 0.9741231909256389, 0.9745217211783955, 0.9742570751136441, 0.9742913376218282, 0.9744350656568305, 0.9737190256113751, 0.9740659215808045, 0.9745822421444627, 0.9741563502191798, 0.9743349436619991, 0.9742047055442487, 0.9739407261438568, 0.9738733404084772, 0.9738327476467455, 0.9743037910227257, 0.9744508000376574, 0.9739406996266857, 0.974096634787515, 0.9736489401932201, 0.9740982179857969, 0.9743641633336505, 0.9745007693040291, 0.9742889527411374, 0.9742150067479828, 0.974447348049596, 0.9749209801755785, 0.9746747308445618, 0.974504901556999, 0.9744632995819718, 0.9742063413652295, 0.9742798145511095, 0.9746632170572623, 0.9742877764843395, 0.9745946934443861, 0.9743352520783995, 0.9744455850379188, 0.9743220021009478, 0.9743422598055358, 0.9742022719312583, 0.9740954722931322, 0.974002577675045], 'MSE': [26108.575146577328, 566.24509661095919, 32.38375699653335, 15.226427648767766, 11.167123749229647, 7.8717237334819217, 5.7007864788221392, 4.5152060653004735, 3.7524323909486998, 3.2859734019283664, 3.0009130899099987, 2.7610699435907886, 2.5325174078252841, 2.3869649162088318, 2.2626761114576373, 2.1833789341446233, 2.1031447970503794, 2.0244676100007788, 2.0002981520175798, 1.9607225202942062, 1.9025792917617912, 1.8677785327119623, 1.8334007692539458, 1.8036657070866624, 1.7675493919247824, 1.7152476487793362, 1.7015927610525885, 1.6705315095682822, 1.6311563916718885, 1.5753331431945492, 1.5225713522594468, 1.5045494263505745, 1.4521540081178927, 1.4228328306210245, 1.3886058451418424, 1.361560126519352, 1.3507892796536505, 1.2910806993982948, 1.2830344882237472, 1.2565878366479262, 1.2523662572347878, 1.2534100456635251, 1.2355448518500984, 1.2359028426149046, 1.2236819991352681, 1.2145596918959056, 1.1957449610238802, 1.19481144215868, 1.1884535700631871, 1.1859507414296127, 1.177517507173937, 1.18738477254241, 1.178088063301505, 1.1711584383322409, 1.1842791172026088, 1.168505638619926, 1.1720503766700887, 1.1618373224881779, 1.1710050127925127, 1.1882054908868738, 1.1545543874074953, 1.1596694861408519, 1.155357652112496, 1.1471997536667917, 1.1373386060267285, 1.1400495607824839, 1.1468176669429249, 1.1429726908345736, 1.1400652156288202, 1.1285286055611379, 1.1172648325339232, 1.1143980611395921, 1.1223821320306306, 1.1047569992584707, 1.085054269363785, 1.0909189762047857, 1.100016505064036, 1.085841682286961, 1.084889983318446, 1.0775677660076479, 1.0812792400176168, 1.0817725914634599, 1.0666237822277997, 1.0824131486958279, 1.0884663834122292, 1.068921367029948, 1.0740054605964866, 1.0615065497696656, 1.0706441793330754, 1.0701208526081631, 1.0714884377417091, 1.068957396534602, 1.0640198247595125, 1.0594757068151823, 1.0647232436113061, 1.0599550378055269, 1.0666909097263451, 1.0602385774769012, 1.0595823471170791, 1.043430800282912, 1.0563635240673344, 1.0538270556314016, 1.0533222254338674, 1.0489959267016771, 1.0436431020153059, 1.0500971841114128, 1.0491674478852755, 1.0474906577068257, 1.0497397002226374, 1.0442122914124659, 1.0443836498696391, 1.0329968453898581, 1.0288647233866335, 1.0333587516961127, 1.0317354554647322, 1.0462978563904926, 1.0378593730555645, 1.0494249781760994, 1.0423611666057655, 1.0483228877639912, 1.0289794980627953, 1.040739651500457, 1.0228144869237183, 1.0200699574817924, 1.0213999112494179, 1.0241320957530853, 1.0230465212748177, 1.0189884005323238, 1.0216157778319239, 1.0251357763500391, 1.0245789848587536, 1.0123066764318913, 1.0186487478695123, 1.0217510337587867, 1.0289155226885778, 1.0261697714568172, 1.03173968216274, 1.0177602481413845, 1.0128342175751095, 1.0215035158556247, 1.0316821558914457, 1.0257552159824967, 1.0311371651331567, 1.0238063324567472, 1.0202164017364983, 1.0164868180952678, 1.0214769102064958, 1.0052299360345662, 1.0108785334815045, 1.0055046226984099, 0.99995024403293664, 1.0058856834653525, 1.0148729987376708, 1.0109684571699773, 1.0121948089719632, 1.0067933698640821, 1.0228927150251752, 1.0184074807176298, 1.0136025661976511, 1.0175341672001004, 1.0018630638705739, 1.0122695406632007, 1.0109222620002454, 1.0052705533224431, 1.0334268537859443, 1.0197861262780026, 0.99948324375332998, 1.0162302694111123, 1.0092075747046552, 1.0143288295820259, 1.0247090916368968, 1.0273588498792532, 1.0289550483086773, 1.0104325663474822, 1.0046518421805433, 1.0247101343515337, 1.0185784141090746, 1.0361827696096564, 1.018516159201958, 1.0080585916838252, 1.0026869385598165, 1.0110160408576232, 1.0139237631485032, 1.0047875820929564, 0.98616330467583468, 0.9958463806393193, 1.0025244491055603, 1.0041603320651473, 1.0142645054323718, 1.0113753749839074, 0.99629912857811476, 1.0110622939129292, 0.99899363071557989, 1.0091954470801001, 1.0048569076660436, 1.0097164659094724, 1.0089198875327439, 1.0144245247027166, 1.0186241259953506, 1.02227695071501], 'Rp': [0.0080868070913401556, 0.042026223945636883, 0.59222743921272136, 0.79135543266300012, 0.84700781873695985, 0.8943931917088791, 0.92471565460541638, 0.94084666443884091, 0.95115549337148864, 0.95738527037014032, 0.96113184845078126, 0.96432147219662379, 0.96732090547488569, 0.96920689106411473, 0.97085131948347902, 0.97190493295618596, 0.97295434848452356, 0.97397577245368705, 0.97430866926993853, 0.97477209348082894, 0.9755840866775537, 0.97598169789255962, 0.97645462211220313, 0.97682035007411383, 0.9773323645910047, 0.97799088176935656, 0.97813767699212595, 0.97855375517161403, 0.9790576078167974, 0.97980329463625715, 0.98050743093921455, 0.98074923071955955, 0.98141156773455307, 0.98179593844230639, 0.98222492421364427, 0.98256994391337715, 0.98268942106924551, 0.98349468898837145, 0.9835832998382763, 0.98393993200680263, 0.98400915014156776, 0.98394630830981678, 0.98420290129535892, 0.98418737012471402, 0.98436030955607023, 0.98447706207319485, 0.9846949839062008, 0.98472613093495931, 0.98487440509414526, 0.98483063043650287, 0.98493012041522265, 0.98483171775360023, 0.98491502550391052, 0.98503037006280436, 0.98485719198847865, 0.98505644156273087, 0.98501585114333545, 0.98512560959037132, 0.98503049870854809, 0.98479297943764255, 0.9852176498783507, 0.98516921403608126, 0.98521857205375774, 0.98531850236608198, 0.98545195981485034, 0.98541076480898571, 0.98533846384647772, 0.98537132890907309, 0.98540914012690428, 0.98556628581187966, 0.98570938306278655, 0.98577031748674904, 0.98564352973595348, 0.98585945776649253, 0.98612418793907486, 0.98603471989677971, 0.98592340358776831, 0.98610201537763387, 0.98614859189570847, 0.98621360039966144, 0.98615996904527814, 0.98615599519649455, 0.98635135455433642, 0.98614810294603916, 0.98607592557698542, 0.9863202712995971, 0.9862576071095589, 0.9864194243557789, 0.98630549866876893, 0.98631077035568671, 0.98629987723891899, 0.98631874179751966, 0.98639103231592984, 0.98644675307853591, 0.9863954063341539, 0.98643928866975916, 0.98635164342370263, 0.98644883668903149, 0.98645085125041942, 0.98665910979403293, 0.98648132761751639, 0.98651283778243026, 0.98653098528808036, 0.98657975847266155, 0.98666758773949603, 0.98656246288578997, 0.98657133457052482, 0.9866014652698557, 0.9865628044945659, 0.98663861365550176, 0.9866340269355659, 0.98678619655891464, 0.98683857676654041, 0.98678087515615209, 0.98680228300856632, 0.98661291970907405, 0.98672016232084037, 0.98656710690285643, 0.98666962796110202, 0.98658936483551651, 0.98683520437105099, 0.98669057388738268, 0.9869124903726999, 0.9869477842799389, 0.98693035265881224, 0.98689229416564395, 0.98690577790662204, 0.98696402056495169, 0.98692469970457253, 0.98688434618343401, 0.98688742855025258, 0.98704573674723739, 0.98696331021007089, 0.98692471031452111, 0.98683540680770965, 0.98688760284975541, 0.98680500683905215, 0.98698236512258952, 0.9870378715485274, 0.98692754071474265, 0.98679452127912048, 0.98687584358773794, 0.98680349172780313, 0.98689776941643281, 0.98694236520262413, 0.9870031525311751, 0.98693138982150852, 0.98713940455571847, 0.98706894852779681, 0.98713533097107753, 0.98720473384545226, 0.9871298662096909, 0.987017813997912, 0.98706795380857282, 0.98705057605797997, 0.98711603583059226, 0.98690955920502577, 0.98696920319270831, 0.98703045053091032, 0.98698006489848977, 0.98717929411172267, 0.9870462374213097, 0.98706275007825484, 0.98713976668877412, 0.98677271611344775, 0.98695854021310025, 0.98721002672016633, 0.98699413380974965, 0.98708624978334292, 0.98701896628494501, 0.98688478939624746, 0.98685337709208221, 0.98683281943131707, 0.98707049303729699, 0.98714735547368149, 0.98689317510559904, 0.98696340233636315, 0.9867450509470358, 0.98696559555749919, 0.9871018766188282, 0.98718032895287011, 0.98707148819274693, 0.9870233947751097, 0.98714332799539928, 0.98738579223844425, 0.98725630745290816, 0.9871772239220199, 0.98715020967728984, 0.98702275573789511, 0.98705818888693519, 0.98725159225244863, 0.98706074448914005, 0.98721712506321035, 0.98708655224867037, 0.98714139887910612, 0.98707831469671858, 0.98710027893298424, 0.98701861669410729, 0.98696577836800992, 0.98692203806319778]}
'''

plt.figure()
plt.plot(BNMF.all_performances['MSE'])