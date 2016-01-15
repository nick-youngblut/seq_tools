#!/usr/bin/env python

"""
fasta_info: general info on a fasta (e.g, number of sequences, sequence length, sequence G+C)

Usage:
  fasta_info [options] <fastaFile>... 
  fasta_info -h | --help
  fasta_info --version

Options:
  <fastaFile>     Fasta file name(s). (Use '-' if from STDIN)
  --fn            Print file name as first column of output.
  --tn            Print total number of sequences.
  --tl            Print total length of sequences.
  --tgc           Print total mean G+C.
  --sn            Print each sequence name.
  --sl            Print length of each sequence.
  --sgc           Print mean G+C of each sequence.
  --header        Print table header.
  --sep=<s>       Output separator. [Default: '\t']
  -n=<n>          Number of processors. [Default: 1]
  --version       Show version.
  --debug         Debug mode (no parallel processing).
  -h --help       Show this screen.

Description:
  Get basic info on a sequence file (in fasta format).
  The output is a table. 
  NOTE: nothing is written by default! You must provide some options!
"""

from docopt import docopt
import sys,os
from functools import partial
import multiprocessing as mp
import pyfasta


def header(uargs):
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
    
def body(inFile, fasta, info, summary_info, uargs):
    # table body
    tbl = []
    for k, l in info:
        line = []
        # summary info
        if uargs['--fn']:
            line.append(inFile)
        if uargs['--tn']:
            nseqs = summary_info['nseqs']
            line.append(str(nseqs))
        if uargs['--tl']:
            total_len = summary_info['total_len']
            line.append(str(total_len))
        if uargs['--tgc']:
            gc_total = summary_info['gc_total']
            line.append('{0:.2f}'.format(gc_total))
        # by-sequence info
        if uargs['--sn'] or uargs['--sl'] or uargs['--sgc']:
            if uargs['--sn']:
                line.append(k)
            if uargs['--sl']:
                line.append(str(l))
            if uargs['--sgc']:
                seq = str(fasta[k]).upper()
                g = seq.count('G')
                c = seq.count('C')
                gc = (g + c) * 100.0 / float(l)
                line.append('{0:.2f}'.format(gc))
            tbl.append(line)
        else:
            tbl.append(line)
            break

    # return
    #print tbl; sys.exit()
    tbl = [uargs['--sep'].join(x) for x in tbl]
    return tbl


def summary_info(fasta, info, uargs):
    # file summary info
    sum_info = dict()
    if uargs['--tn']:
        sum_info['nseqs'] = len(fasta)
    if uargs['--tl']:
        sum_info['total_len'] = sum(l for k, l in info)        
    if uargs['--tgc']:
        g_all = 0
        c_all = 0
        l_all = 0
        for k, l in info:
            seq = str(fasta[k]).upper()
            g_all += seq.count('G')
            c_all += seq.count('C')
            l_all += l
        sum_info['gc_total'] = (g_all + c_all) * 100.0 / float(l_all)

    return sum_info


def by_file(inFile, uargs):
    try:
        fasta = pyfasta.Fasta(inFile)
    except ValueError, TypeError:
        msg = 'ERROR: Could not read file: {}'
        sys.stderr.write(msg.format(inFile) + '\n')
        return None
        
    # fasta file data
    info = [(k, len(seq)) for k,seq in fasta.iteritems()]    
    # fasta summary info
    sum_info = summary_info(fasta, info, uargs)
    # body
    tbl = body(inFile, fasta, info, sum_info, uargs)

    return tbl


def main(uargs):
    if uargs['<fastaFile>'][0] == '-':
        uargs['<fastaFile>'] = [x.rstrip() for x in sys.stdin]

    # header
    if uargs['--header']:
        header(uargs)
    
    # body
    if uargs['--debug']:
        for f in uargs['<fastaFile>']:
            tbl = by_file(f, uargs)
            print '\n'.join(tbl)
    else:
        p = mp.Pool(int(uargs['-n']))
        by_file_p = partial(by_file, uargs=uargs)
        tbls = p.map(by_file_p, uargs['<fastaFile>'])
        for x in tbls:
            print '\n'.join(x)



if __name__ == '__main__':
    uargs = docopt(__doc__, version='0.1')
    uargs['--sep'] = uargs['--sep'].lstrip("'").rstrip("'")
    main(uargs)

