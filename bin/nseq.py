#!/usr/bin/env python

"""
nseq: relatively quick check of number of sequences in fast[aq] file

Usage:
  nseq <file>
  nseq -q <file>
  nseq -h | --help
  nseq --version

Options:
  <file>          Fasta/fastq file name ('-' if from STDIN)
  -q --fastq      Fastq file (assumes no line wrapping)
  -v --version    Show version.
  -h --help       Show this screen.

Description:
  Quick check of number of reads.

  *fasta*
    Number of lines starting with '>'

  *fastq*
    Assumes each fastq sequence takes up 4 lines.
    Throws an error if any blank lines 
"""

from docopt import docopt
import sys,os


def nseq_fasta(fileName):
    if fileName == '-':
        print sum(1 for x in sys.stdin if x.startswith('>'))        
    else:
        print sum(1 for x in open(fileName) if x.startswith('>'))

def check_line(i, line):
    if line.strip() == '':
        msg = 'Line {}: No empty lines allowed!'
        raise IOError(msg.format(i))
    elif i % 4 == 0 and not line.startswith('@'):
        msg = 'Line {}: Sequence doesn\'t start with "@"'
        raise IOError(msg.format(i))
    else:
        return True
    
def nseq_fastq(fileName):
    if fileName == '-':
        print sum(1 for i,x in enumerate(sys.stdin) \
                  if check_line(i,x)) / 4
    else:
        print sum(1 for i,x in enumerate(open(fileName)) \
                  if check_line(i,x)) / 4

    
def main(uargs):
    if uargs['--fastq']:
        nseq_fastq(uargs['<file>'])
    else:
        nseq_fasta(uargs['<file>'])

    
if __name__ == '__main__':
    uargs = docopt(__doc__, version='0.1')
    main(uargs)

