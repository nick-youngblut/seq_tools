#!/usr/bin/env python

"""
seqIntersect: Get the intersection of 2 read files (just same reads in both).

Usage:
  seqIntersect [options] <seq1> <seq2>
  seqIntersect [options] <seq1> <seq2> <out1> <out2>
  seqIntersect -h | --help
  seqIntersect --version

Options:
  <seq1>         Sequence-1 file (fastq, fasta, or screedDB).
  <seq2>         Sequence-2 file (fastq, fasta, or screedDB).
  <out1>         File name for output of sequence-1
  <out2>         File name for output of sequence-2
  -k --keep      Keep the created screed databases (if fastq or fasta files).
  -v --verbose   Verbose output.
  --version      Show version.
  -h --help      Show this screen.

Description:
  The intersection is determined on read names (everything before a ' ' in the name).

  Input:
    The read files can be fastq or fasta formatted sequence files,
    or they can be screed databases (file names must end in '_screed').
    If fastq or fasta files are provided, screed databases are created
    from the files. By default, the screed databases will be deleted
    after the intersecting sequences are written.

  Output:
   If <out1> and/or <out2>: sequences written to respective files.
   Else: only the sequences from <seq1> are written to STDOUT.
"""

from docopt import docopt
import sys,os
from itertools import imap
import screed
import logging
from time import gmtime, strftime


def my_time():
    return strftime('%H:%M:%S', gmtime())

def openDB(fileName):
    """Opening screed DB; making if not already existing
    Args:
    fileName -- Name of sequence file or screedDB file
    """
    logging.info('{}: Making/opening screed database for: "{}"'.format(my_time(), fileName))
    
    # making db if needed
    if not fileName.endswith('_screed'):
        try:
            screed.read_fastq_sequences(fileName)
            fileName = fileName + '_screed'
        except KeyError:
            try:
                screed.read_fasta_sequences(fileName)
                fileName = fileName + '_screed'
            except IOError:
                msg = 'Cannot open {}'.format(fileName)
                raise IOError(msg)

    # init screed db
    return screed.ScreedDB(fileName)


def write_seq(screed_db, key, outFH):
    """Writing a sequence object from a screed db object.
    Args:
    screed_db -- screed db object
    key -- screed db object key
    outFH -- output file handle
    """
    seq = screed_db[key]
    try:
        outFH.write('@{} {}\n{}\n+\n{}\n'.format(seq['name'], seq['annotations'], 
                                                 seq['sequence'],
                                                 seq['accuracy']))
    except KeyError:
        outFH.write('>{} {}\n{}\n'.format(seq['name'],
                                          seq['description'],
                                          seq['sequence']))

        
def get_screed_key_intersect(screed1, screed2, out1=None, out2=None):
    """Getting the intersection of screed db keys.
    Args:
    screed1 -- screed object
    screed2 -- screed object
    out1 -- output file name
    out2 -- output file name
    """
    logging.info('{}: Finding sequence intersection'.format(my_time()))

    # output files
    outFH1 = sys.stdout
    outFH2 = None
    if out1:
        outFH1 = open(out1, 'w')
    if out2:
        outFH2 = open(out2, 'w')
        
    # writing intersecting sequences                            
    for x in reduce(set.intersection, imap(set, [screed1.keys(), screed2.keys()])):
        if outFH1:
            write_seq(screed1, x, outFH1)
        if outFH2:
            write_seq(screed2, x, outFH2)

    # IO        
    if outFH1:        
        outFH1.close()
        logging.info('{}: File written: "{}"'.format(my_time(), out1))
    if outFH2:
        outFH2.close()
        logging.info('{}: File written: "{}"'.format(my_time(), out2))        

    
def rm_screed_db(fileName):
    """Delete the screed database file associated with the
    provided file. Associated Screed database assumeded
    to be 'fileName' + '_screed'.
    Args:
    fileName -- name of file that has an associated '*_screed' file
    """

    screedName = fileName + '_screed'
    if os.path.isfile(screedName):
        os.unlink(screedName)

    logging.info('{}: Removed screed db file: "{}"'.format(my_time(), screedName))


def main(uargs):
    if uargs['--verbose']:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    
    # init screed DB objects
    db_r1 = openDB(uargs['<seq1>'])
    db_r2 = openDB(uargs['<seq2>'])

    # intersection of read names
    get_screed_key_intersect(db_r1, db_r2, uargs['<out1>'], uargs['<out2>'])                

    # delete screed files
    if not uargs['--keep']:
        rm_screed_db(uargs['<seq1>'])
        rm_screed_db(uargs['<seq2>'])
        
    

if __name__ == '__main__':
    uargs = docopt(__doc__, version='0.1')
    main(uargs)

