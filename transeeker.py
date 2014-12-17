from Bio.Blast.Applications import NcbiblastnCommandline
from Bio import SeqIO
import StringIO
import os.path
import glob
import re



fasta_in_dir = '' # directory of fasta files to check
fasta_out_dir = '' # directory to save hits fasta too
blast_db = '' # repbase local blast db
file_hits_file = 'te_file_hits.csv' # output of files that contain hits
hits_file = 'te_hits.csv' # output of sequence hits
evalue = 0.001



if not os.path.isfile(file_hits_file) :
    fasta_files = glob.glob(fasta_in_dir + '*.fas')
    status_count = 1
    target_recs = []
    for f in fasta_files :
        re_search = fasta_in_dir + '(.+?).fas'
        file_name = re.search(re_search, f).group(1)
        print "Processing fasta file %s / %s..." %(status_count, len(fasta_files))
        handle = open(f, 'r')
        for record in SeqIO.parse(handle, 'fas') :
            longest_rec = record
            if longest_rec :
                if len(record.seq) > len(longest_rec.seq) :
                    longest_rec = record


        target_recs.append(longest_rec)
        status_count += 1
        out_file = fasta_out_dir + file_name + '.fas'
        if longest_rec :
            out_handle = open(out_file, 'w')
            SeqIO.write(longest_rec, out_handle, 'fas')
        else:
            print "File %s skipped as no sequence was present." %file_name
            with open('transeeker_errors.log', 'a') as ef:
                ef.write(f+'\n')

    fasta_files = glob.glob(fasta_out_dir + '*.fas')

    te_file_hits = []
    for f in fasta_files :
        print "Searching file %s for transposable elements..." %f
        blastn_cline = NcbiblastnCommandline(query=f, db=blast_db, evalue=evalue, outfmt='6', max_target_seqs=1)
        stdout, stderr = blastn_cline()
        tab_out = str(stdout)
        
        if tab_out :
            hit_rec = tab_out.split()
            hit_rec.insert(0, str(f))
            if float(hit_rec[3]) == 100.00 :
                te_file_hits.append(hit_rec) 

    if te_file_hits :
        with open(file_hits_file, 'a') as f:
            for h in te_file_hits :
                f.write(",".join(h)+'\n')


else :
    print "\n\n"
    print "TE File Positives List Found. Jumping to fine-grained search.\n"
    te_hits = []

    hits_file_handle = open(hits_file, 'r')

    for line in hits_file_handle :
        re_search = fasta_out_dir + '(.+?).fas'
        re_out = re.search(re_search, line.split(",")[0]).group(1)
        fname = fasta_in_dir + re_out + ".fas"
        if os.path.isfile(fname) :
            print "Searching positive hits file %s for transposable elements..." %fname
            blastn_cline = NcbiblastnCommandline(query=fname, db=blast_db, evalue=evalue, outfmt='6', max_target_seqs=1)
            stdout, stderr = blastn_cline()
            tab_out = str(stdout)
            
            if tab_out :
                tabs_list = tab_out.split("\n")
                for t in tabs_list :
                    if len(t) == 0 :
                        tabs_list.remove(t)
                for t in tabs_list :
                    hit_rec = t.split()
                    hit_rec.insert(0, str(fname))
                    if float(hit_rec[3]) > 99.00 :
                        te_hits.append(hit_rec)

    if te_hits :
        with open(hits_file, 'a') as f:
            for h in te_hits :
                f.write(",".join(h)+'\n')
