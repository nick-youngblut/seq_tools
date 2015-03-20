#!/usr/bin/env perl
use strict;
use warnings;

=pod

=head1 NAME

filter_seq.pl -- Use bioperl to filter out sequences in variously formatted sequence files (output to STDOUT).

=head1 VERSION

This is version 0.0.1

=head1 USAGE

    filter_seq.pl [options]

=head1 REQUIRED ARGUMENTS

=over

=item -sf <seq_file> | -seq_file <seq_file>

Input file name. ('-' if from STDIN)

=for Euclid:
seq_file.type: input

=item -ff <filter_file> | -filter_file <filter_file>

List of sequences to filter from input sequence file (1 sequence name per line).
('-' if from STDIN)

=for Euclid:
filter_file.type: input

=back

=head1 OPTIONS

=over

=item -if <in_format> | -in_format <in_format>

Input sequence file format.

Default: in_format.default

=for Euclid:
in_format.type: input
in_format.default: 'fasta'

=item -of <out_format> | -out_format <out_format>

Output sequence file format.

Default: out_format.default

=for Euclid:
out_format.type: input
out_format.default: 'fasta'

=item -keep

Filter file become keep file (all taxa listed are kept).

=item --debug [<log_level>]

Set the log level. Default is log_level.default but if you provide --debug,
then it is log_level.opt_default.

=for Euclid:
    log_level.type:        int
    log_level.default:     0
    log_level.opt_default: 1

=item --version

=item --usage

=item --help

=item --man

Print the usual program information

=back

=head1 DESCRIPTION

Simple script for filtering/keeping select sequences
in a sequence file. See the BioPerl SeqIO documentation
for info on which file formats are accepted.

=head2 WARNINGS

BioPerl will identify the sequence ID as anything after
the '>' and up to the first whitespace character.
For example: the sequence ID for '>Escherichia coli' would be '>Escherichia'.

=head1 AUTHOR

Nick Youngblut (ndy2@cornell.edu)

=head1 BUGS

There are undoubtedly serious bugs lurking somewhere in this code.
Bug reports and other feedback are most welcome.

=head1 COPYRIGHT

Copyright 2010, 2011
This software is licensed under the terms of the GPLv3

=cut

#--- modules ---#
use Data::Dumper;
use Getopt::Euclid;
use Bio::SeqIO;


#--- MAIN ---#
# Input
## sequence file I/O
my $seqfh;
$ARGV{-seq_file} eq '-' ?
  $seqfh = \*STDIN :
  open $seqfh, $ARGV{-seq_file} or die $!;

my $in = Bio::SeqIO->new(-fh => $seqfh,
			 -format => $ARGV{-in_format});
my $out = Bio::SeqIO->new(-fh => \*STDOUT,
			  -format => $ARGV{-out_format});

## filter file
my %ff;
open IN, $ARGV{-filter_file} or die $!;
while(<IN>){
  chomp;
  next if /^\s*$/;
  s/^>//;
  $ff{$_} = 1;
}


## filtering
my %summary = ( input_total => 0, filtered => 0, kept => 0 );
while( my $seqo = $in->next_seq ){
  $summary{input_total}++;

  if( $ARGV{-keep} ){  # keep if exists in filer file
    if( exists $ff{$seqo->id} ){  
      $summary{kept}++;
      $out->write_seq($seqo);
    }
    else{
      $summary{filtered}++;
    }
  }
  else{   # filter if exists in filter file
    if( exists $ff{$seqo->id} ){  
      $summary{filtered}++;
    }
    else{
      $summary{kept}++;
      $out->write_seq($seqo);
    }
  }
}


## summary
printf STDERR "Number of input sequences: %10i\n", $summary{input_total};
printf STDERR "Number of filtered sequences: %10i\n", $summary{filtered};
printf STDERR "Number of written sequences: %10i\n", $summary{kept};


