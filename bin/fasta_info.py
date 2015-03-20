#!/usr/bin/env python

"""
fasta_info.py: general info on a fasta (e.g, number of sequences, sequence length, sequence G+C)

Usage:
  fasta_info.py [options] <fastaFile> 
  fasta_info.py -h | --help
  fasta_info.py --version

Options:
  <fastaFile>     Fasta file name.
  --fn            Print file name as first column of output.
  --tn            Print total number of sequences.
  --tl            Print total length of sequences.
  --tgc           Print total mean G+C.
  --sn            Print each sequence name.
  --sl            Print length of each sequence.
  --sgc           Print mean G+C of each sequence.
  --sep=<s>       Output separator. [default: \t]
  --header        Print table header.
  -v --version    Show version.
  -h --help       Show this screen.
"""

from docopt import docopt
import sys,os

import pyfasta


def main(uargs):
    f = pyfasta.Fasta(uargs['<fastaFile>'])

    info = [(k, len(seq)) for k,seq in f.iteritems()]

    # file summary info
    if uargs['--tn']:
        nseqs = len(f)
    if uargs['--tl']:
        total_len = sum(l for k, l in info)
    if uargs['--tgc']:
        g_all = 0
        c_all = 0
        l_all = 0
        for k, l in info:
            seq = str(f[k]).upper()
            g_all += seq.count('G')
            c_all += seq.count('C')
            l_all += l
        gc_total = (g_all + c_all) * 100.0 / float(l_all)


    # header
    if uargs['--header']:
        tblHeader = []
        if uargs['--fn']:
            tblHeader.append('file_name')
        if uargs['--tn']:
            tblHeader.append('total_sequences')
        if uargs['--tl']:
            tblHeader.append('total_seq_length')
        if uargs['--tgc']:
            tblHeader.append('total_GC')
        if uargs['--sn']:
            tblHeader.append('seq_name')
        if uargs['--sl']:
            tblHeader.append('seq_length')
        if uargs['--sgc']:
            tblHeader.append('seq_GC')        
        print uargs['--sep'].join(tblHeader)

    # table body
    tbl = []
    for k, l in info:
        line = []
        # summary info
        if uargs['--fn']:
            line.append(uargs['<fastaFile>'])
        if uargs['--tn']:
            line.append(str(nseqs))
        if uargs['--tl']:
            line.append(str(total_len))
        if uargs['--tgc']:
            line.append('{0:.2f}'.format(gc_total))
        # by-sequence info
        if uargs['--sn'] or uargs['--sl'] or uargs['--sgc']:
            if uargs['--sn']:
                line.append(k)
            if uargs['--sl']:
                line.append(str(l))
            if uargs['--sgc']:
                seq = str(f[k]).upper()
                g = seq.count('G')
                c = seq.count('C')
                gc = (g + c) * 100.0 / float(l)
                line.append('{0:.2f}'.format(gc))
            tbl.append(line)
        else:
            tbl.append(line)
            break

    # writing body of table
    for line in tbl:
        print uargs['--sep'].join(line)
            
        

if __name__ == '__main__':
    uargs = docopt(__doc__, version='0.1')
    main(uargs)

