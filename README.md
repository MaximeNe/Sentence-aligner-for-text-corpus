# Sentence aligner for FR - FRNB corpus

## Tool used:
**The hunalign sentence aligner**  
*github: https://github.com/danielvarga/hunalign*  
*paper: D. Varga, L. Németh, P. Halácsy, A. Kornai, V. Trón, V. Nagy (2005). Parallel corpora for medium density languages In Proceedings of the RANLP 2005, pages 590-596. (pdf)*
It remains unchanged and in the directory *hunalign*

## Auto generation of the required dictionary:
The file "Appendix NB.xlsx" from the All-inGMT projet is used to generate a dictionary from French to NonBinary French. It is completed with words used in both FR and FRNB texts to align.

## Author of added code:
Maxime NEMO  
Maxime.Nemo@grenoble-inp.org

## How to use:
### Choice 1 (preferred):
Use the built app in the github repo -> click "actions", and then select the lasted build. Then on the "artifact" section, click "app"  
To use the app, then unzip the file, and go to *dist/run*.
* create a file named "fr.txt" containing the source sentences (one by line)
* create a file named "nb.txt" containing the target sentences (one by line)
* run the program name **run**
* The output is a *.xls* file named *output.xls*

### Choice 2 (for developpers):
#### install hunalign 
check the [hunaligh github](https://github.com/danielvarga/hunalign)
#### install dependencies
<pre>  pip install xlwt xlrd==1.2.0 </pre>
#### use it
* create a file named "fr.txt" containing the source sentences (one by line)
* create a file named "nb.txt" containing the target sentences (one by line)
* run the python script
  <pre> python3 run.py </pre>
* The output is a *.xls* file named *output.xls*


## Licence
Licensed under the GNU LGPLv3 or later.