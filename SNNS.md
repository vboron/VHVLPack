# SNNS Pipeline

## This file gives a description of the process for creating the training the SNNS and building a model, then testing it.

1. All pre-processing happens as done for Weka ML([VHVL Pack ReadME](https://github.com/vboron/VHVLPack#readme)).
However, the encoding method needs to be 4d vectors created by ARCM lab, as this creates the correct subpattern for
the SNNS to process.

2. The final .csv containing all of the files for training is turned into an arff (with normalization)
([csv2arff](https://github.com/AndrewCRMartin/bioscripts/blob/master/csv2arff.pl)). Here the output will be 'angle'.
`csv2arff -v -norm -ni input.dat output mycsvfile.csv > myfile.arff`

3. This arff file is converted to a .pat file using
([arff2snns](https://github.com/AndrewCRMartin/bioscripts/blob/master/arff2snns.pl)).
`arff2snns myfile.arff > final.pat`

4. A program called ([batchman](https://github.com/ACRMGroup/papa/blob/master/training/papa_batchman.pl)) trains the
neural network and produces a .csm file for it. It uses the final.pat, so we need to keep this name.
`batchman -f final_training.cmd`

5. File needs to be moved to the 'papa/training/' directory, and then it is recompiled to produce a new program for
running the model.
`./install.sh $HOME/name_for_new_papa`

6. This new version can now be run as:
`~/name_for_new_papa/papa`
