from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio import SeqIO
import glob
import os



orig_repbase_dir = '' # directory containing raw repbase files
out_file ='' # fasta file output name



new_fasta = open(out_file, 'a')
rec_count = 1
repbase_files = glob.glob(orig_repbase_dir + "*.ref")

print "\nBeginning converson with the following parameters:"
print "-"*65
print "\nIn Dir: %s" %orig_repbase_dir
print "Repbase Files: %s" %len(repbase_files)
print "Out File: %s\n" %out_file
print "-"*65
print "\nConverting Repbase to makeblastdb friendly fasta:"

temp_no_tabs = open('repbase_notabs.fasta', 'a')
print "   -Removing blast-unfriendly characters from record descriptions..."
for f in repbase_files:
    rep_f = open(f, 'r')
    for line in rep_f:
        new_line = line.replace('\t', ':')
        temp_no_tabs.write(new_line+'\n')
temp_no_tabs.close()


no_tabs_handle = open('repbase_notabs.fasta', 'r')
print "   -Removing gaps and converting ambiguous sequence characters to blast-friendly values..."
for line in no_tabs_handle:
	seq = None
	if line.startswith('>') :
		id_list = line.split(':')
		if len(id_list) == 1:
			id = id_list[0][1:].strip('\n')
		elif len(id_list) == 2:
			id = id_list[0][1:]
			element = id_list[1].strip('\n')
		elif len(id_list) >=3:
			id = id_list[0][1:]
			element = id_list[1]
			organism = id_list[2].strip('\n')

	else:
		seq = line.replace('*', 'n').strip('\n')
                seq = seq.replace('-', '').strip('\n')
	
	if seq:
		if element and organism:	
			record = SeqRecord(Seq(seq, IUPAC.unambiguous_dna), id=id, name=element, description=element+" "+organism)
		elif element and not organism:
			record = Seqrecord(Seq(seq, IUPAC.unambiguous_dna), id=id, name=element, description=element)
		else:
			record = Seqrecord(Seq(seq, IUPAC.unambiguous_dna), id=id)
		SeqIO.write(record, new_fasta, "fasta")
	rec_count += 1

print "Cleaning up temp files..."
os.remove('repbase_notabs.fasta')

print "Conversion Complete."
print "%s records successfully converted." %rec_count