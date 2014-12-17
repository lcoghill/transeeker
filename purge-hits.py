import shutil
import glob
import re



out_dir = '' # dir where fasta files with TEs removed will be saved
in_dir = '' # directory with the original fasta files
hits_file = open('te_hits.csv', 'r') # hits file in csv format



fasta_files = glob.glob(in_dir + "*.fas")
te_hits = []

for line in hits_file:
    record = line.split(',')
    hit_name = re.search('/(.+?).fas', record[0]).group(1)
    te_hits.append(hit_name)

for f in fasta_files:
    search_str = "".join([in_dir,"(.+?).fas"])
    file_name = re.search(search_str, f).group(1)
    dst = out_dir + file_name + '.fas'
   
    if file_name not in te_hits:
        print "Copying file %s..." %f
        shutil.copyfile(f, dst)