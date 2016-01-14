#!/usr/bin/env python

"""
fasta_rename.py: rename sequences in a fasta file

Usage:
  fasta_rename.py [options] <fasta_file> <mapping_file>
  fasta_rename.py -h | --help
  fasta_rename.py --version

Options:
  <fasta_file>     Fasta file.
  <mapping_file>   Mapping file (old_name<tab>new_name).
  --version        Show version.
  --debug          Debug mode (no parallel processing).
  -h --help        Show this screen.

Description:
  Re-name a fasta file using a mapping file (old_name -> new_name).

  NOTE: only sequences in the mapping file will be written (others ignored).
"""

from docopt import docopt
import sys,os
from functools import partial
import pyfasta
import pandas as pd


def main(uargs):
    # load
    fasta = pyfasta.Fasta(uargs['<fasta_file>'])
    df = pd.read_csv(uargs['<mapping_file>'], sep='\t', header=None)

    # assert
    msg = 'The mapping file must have 2 columns: <old_name><tab><new_name>'
    assert df.shape[1] >= 2, msg
    
    # rename
    msg = 'Sequence name "{}" not found!'
    new_fasta = []
    for i in xrange(df.shape[0]):        
        old_name = df.loc[i,0]
        new_name = df.loc[i,1]
        try:
            seq = fasta[old_name]
        except KeyError:
            raise KeyError, msg.format(old_name)
        new_fasta.append([new_name,seq])

    # write
    for x in new_fasta:
        print '>{}\n{}'.format(x[0], x[1])
    

if __name__ == '__main__':
    uargs = docopt(__doc__, version='0.1')
    main(uargs)

