# OneStepDataAnalysis

This repository is made to host scripts for predictive modeling of data stored as a short form csv file.

Usage with example data from BraTS 2018 survival challenge

Rscript -e "rmarkdown::render( 'survival_analysis.RMD', output_file = './survival_exampleout.pdf',params = list( csvPath='exampledata.csv', outCsvName='exampledata_withpredictions.csv', survival='survival', status=NULL, regexp='(Volume|Mean)', fixed_inputs='age', exclude_inputs = '(Absolute|RootMean)', leaveOneOut=TRUE, nfold=5, foldID=1, breaks=c(-Inf,304,456,Inf) ))"


Usage with binary short/long survivor data

Rscript -e "rmarkdown::render( 'binary_analysis.RMD', output_file = './binary_exampleout.pdf', params = list( csvPath='exampledata.csv', target='survivalClass', positive_class='short', regexp='(VoxelNum|firstorder)', fixed_inputs='age',leaveOneOut=TRUE, nfold=5, foldID=1) )"

