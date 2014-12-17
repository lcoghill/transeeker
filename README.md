transeeker
==========

Transposable element identification tool

Python script to use blast to compare a directory of fasta sequence files to the transposable element database Repbase.
Useful for quick identification of potential TEs in sequence sets that can be problematic for comparative analyses. 

<h4>Minimum requirements:</h4>
* [Python 2.7](http://www.python.org)
* [Biopython](http://www.biopython.org)
* [NCBI Blast+](http://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)
* [Repbase](http://www.girinst.org/repbase/)

<h4>Basic use:</h4>
1. Download [Repbase](http://www.girinst.org/repbase/)
2. Choose which files you want to include (ie: all of them, eukarotyoes only, only mice, etc.)
3. Place those files in a directory
4. Run `python convert-repbase.py` specifying the directory where you decompressed Repbase.
5. Build a blast DB with this fasta file: `makeblastdb -in REPBASE.FASTA -out XXXX -dbtype 'nucl'`
6. Run `python transeeker.py` specifying your new blastdb and a directory of sequence files in fasta format to check.
  7. The results are in the form of a CSV file that can easily be parsed with code or opened in Excel, LibreOffice etc.
