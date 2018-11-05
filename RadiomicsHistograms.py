# uses pyradiomics to generate feature maps and prints a histogram of the data values

# Requires pyradiomics version 2.0 or greater

# example usage: python RadiomicsHistograms.py --file BRATSlist.csv --param exampleVoxel.yaml --writeImage

from radiomics import featureextractor
import matplotlib.pyplot as plt
import six
import sys, os, argparse, csv
import numpy as np

import SimpleITK as sitk


# Get params from cmd line
parser = argparse.ArgumentParser(description = "Plot histograms of radiomics feature" +
    "for multiple images. Optionally save feature maps of the form imageName_maskName_labelNumber_featureName.nii.gz. Feature maps are cropped and need to be put back into the image space with c3d")
parser.add_argument("--file", "-f", help = "CSV with filepaths and columns Image, Mask, Label",
      required = True)
#parser.add_argument("--feature", default = None,
#      help = "feature name: i.e. original_firstorder_Mean. See pyradiomics -h for help")
parser.add_argument("--writeImage", "-w", dest="writeImage", action="store_true",
      help = "Include flag to write out a feature map (NIFTI) for each feature for each row. Cropped to the specific ROI")
parser.add_argument("--directory", "-d", default = "",
      help = "Directory to place output files in")
parser.add_argument("--param", "-p", default = "",
      help = "Pyradiomics parameter file to use for feature extraction. Old parameter files will need the VoxelSettings category added in order to be compatible.")

args = parser.parse_args()

# Check that csv file exists
if not os.path.isfile(args.file):
  sys.exit("Error: csv file " + args.file + " not found")

#Read file
inputCsv = csv.DictReader(open(args.file))
if 'Image' not in inputCsv.fieldnames:
  sys.exit("CSV file does not contain 'Image' column")
elif 'Mask' not in inputCsv.fieldnames:
  sys.exit("CSV file does not contain 'Mask' column")
elif 'Label' not in inputCsv.fieldnames:
  sys.exit("CSV file does not contain 'Label' column")

#set up extractor
if not os.path.isfile(args.param):
  sys.exit("No parameter file given")

extractor = featureextractor.RadiomicsFeaturesExtractor(args.param)

for row in inputCsv:
  imageName = row['Image']
  maskName  = row['Mask']
  label     = int(row['Label'])

  # compute feature maps
  print("Extracting features for:\n" + imageName + "\n" + maskName + "\n" +  "label =" + str(label))
  result = extractor.execute(imageName, maskName, label, voxelBased=True)

  # extract images
  for key, val in six.iteritems(result):
    outname = args.directory + '_'.join([os.path.basename(imageName).rsplit('.')[0],
                          os.path.basename(maskName).rsplit('.')[0],
                          str(label), key]) + '.nii.gz'
   
    print("Creating histogram for feature " + key)
    voxelArray = sitk.GetArrayFromImage(val)
    voxelArray = voxelArray[~np.isnan(voxelArray)] #only non-nan voxels
    voxelMean = voxelArray.mean()
    print("Mean: " + str(voxelMean))

    #Print histogram
    plt.figure()
    n, bins, patched = plt.hist(voxelArray,25,facecolor='gray',alpha=0.75)
    plt.xlabel(key)
    plt.ylabel('frequency')
    plt.title(imageName +"\n"+ maskName +"\n"+str(label))
    plt.grid(True)
    plt.savefig(outname.replace('.nii.gz','.png'), bbox_inches='tight')

    if args.writeImage:
      print('Writing Image ' + outname)
      sitk.WriteImage(val, outname)
 

# Check that feature name is valid


# featureExtractor.enableFeaturesByName()
## key is the feature class name, value is a list of enabled feature names
