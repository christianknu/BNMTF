"""
Run the nested cross-validation for the NMTF class, on the Sanger dataset.

Since we want to find co-clusters of significantly higher/lower drug sensitivity
values, we should use the unstandardised Sanger dataset.
"""

import sys
sys.path.append("/home/tab43/Documents/Projects/libraries/")#("/home/thomas/Documenten/PhD/")#

import numpy, random
from BNMTF.code.nmf_np import NMF
from BNMTF.cross_validation.nested_matrix_cross_validation import MatrixNestedCrossValidation
from BNMTF.drug_sensitivity.experiments_gdsc.load_data import load_gdsc


# Settings
standardised = False
train_config = {
    'iterations' : 2000,
    'init_UV' : 'exponential',
    'expo_prior' : 0.1
}
K_range = [6,8,10,12,14]
no_folds = 10
output_file = "./REDO_results.txt"
files_nested_performances = ["./REDO_fold_%s.txt" % fold for fold in range(1,no_folds+1)]

# Construct the parameter search
parameter_search = [{'K':K} for K in K_range]

# Load in the Sanger dataset
(_,X_min,M,_,_,_,_) = load_gdsc(standardised=standardised,sep=',')

# Run the cross-validation framework
random.seed(42)
numpy.random.seed(9000)
nested_crossval = MatrixNestedCrossValidation(
    method=NMF,
    X=X_min,
    M=M,
    K=no_folds,
    P=5,
    parameter_search=parameter_search,
    train_config=train_config,
    file_performance=output_file,
    files_nested_performances=files_nested_performances
)
nested_crossval.run()
