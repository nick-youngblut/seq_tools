#!/usr/bin/env perl
use strict;
use warnings;

=pod

=head1 NAME

Tm_calc.pl -- calculate the melting temp of >= 1 sequence

=head1 VERSION

This is version 0.0.1

=head1 USAGE

    Tm_calc.pl [options]

=head1 REQUIRED ARGUMENTS

=head1 OPTIONS

=over

=item -sf <seq_file> | -seq_file <seq_file>

Input file name. ('-' if from STDIN)

=for Euclid:
seq_file.type: input
seq_file.default: '-'


=item -if <in_format> | -in_format <in_format>

Input sequence file format.

Default: in_format.default

=for Euclid:
in_format.type: input
in_format.default: 'fasta'


=item -sc <salt_conc> | -salt_conc <salt_conc>

Set the Na+ concentration on which to base the calculation

Default: salt_conc.default

=for Euclid:
salt_conc.type: number
salt_conc.default: 0.05


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

Calculate the melting temperature of sequences by usihng the Tm
function in Bio::SeqFeature::Primer.

The output is a tab-delimited table: seq_name<tab>Tm

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
use Bio::SeqFeature::Primer;

#--- I/O error ---#
#--- MAIN ---#


my $seqfh;
$ARGV{-seq_file} eq '-' ?
  $seqfh = \*STDIN :
  open $seqfh, $ARGV{-seq_file} or die $!;

my $in = Bio::SeqIO->new(-fh => $seqfh,
			 -format => $ARGV{-in_format});

while( my $seqo = $in->next_seq ){
  my $primer = Bio::SeqFeature::Primer->new( -seq => $seqo );

  print join("\t", 
	     $primer->seq->primary_id,
	     $primer->Tm(-salt => $ARGV{-salt_conc})), "\n";
}

