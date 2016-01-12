#!/usr/bin/env perl

=pod

=head1 NAME

GC_content.pl -- Calculate the GC content of a fasta file

=head1 SYNOPSIS

=head2 pipe in fasta

GC_content.pl [flags] < file.fasta > GC.txt

=head2 multiple fasta files

GC_content.pl [flags] file1.fasta file2.fasta > GC.txt 

=head2 Required flags

=over

NONE

=back

=head2 Optional flags

=over

=item -h  <bool>

Print this help message & exit. [FALSE]

=back

=head2 For more information:

perldoc GC_content.pl

=head1 DESCRIPTION

Simple script for calculating GC content of 
nucleotide sequences in fasta format.

The sequences can have gaps (encoded as '-' or '.').

=head2 Output (tab-delimited table)

=over

=item * File_name (if files provided as arguments)

=item * Sequence_name

=item * Sequence_length

=item * GC_content (%)

=back

=head1 EXAMPLES

=head2 Basic usage:

GC_content.pl [flags] < file.fasta > GC.txt

=head1 AUTHOR

Nick Youngblut <ndy2@cornell.edu>

=head1 AVAILABILITY

email me

=head1 COPYRIGHT

Copyright 2010, 2011
This software is licensed under the terms of the GPLv3

=cut


#--- modules ---#
use strict;
use warnings;
use Pod::Usage;
use Data::Dumper;
use Getopt::Long;

#--- args/flags ---#
pod2usage("$0: No files given.") if ((@ARGV == 0) && (-t STDIN));

my ($verbose_b);
GetOptions(
	"verbose" => \$verbose_b,
	"help|?" => \&pod2usage # Help
	);

#--- I/O error ---#

#--- MAIN ---#
if(@ARGV){
  foreach my $file (@ARGV){
    print STDERR "WARNING: cannot find $file. Skipping\n"
      unless -e $file;
    load_fasta($file);
  }
}
else{
  load_fasta();
}

#--- Subroutines ---#
sub load_fasta{
# loading fasta file #
  my $file = shift;

  my $openfh;
  if(defined $file){
    open $openfh, $file or die $!;
  }
  else{
    $openfh = *STDIN;
  }

  my (%fasta, $tmpkey);
  while(<$openfh>){
    chomp;
    s/#.+//;

    if(eof){ # last sequence
      $fasta{$tmpkey} .= $_;
      # calculating GC & writing output
      calc_GC(\%fasta, $file) if %fasta;
    }
    elsif(/>.+/){
      next if  /^\s*$/;

      #calculating GC & writing output
      calc_GC(\%fasta, $file) if %fasta; 

      # loading next sequence
      ($tmpkey = $_) =~ s/^>//;# changing key      
      $fasta{$tmpkey} = "";
    }
    else{
      next if  /^\s*$/;
 
      $fasta{$tmpkey} .= $_; 
    }
  }
  close $openfh;
  #print Dumper %fasta; exit;
 # return \%fasta;
}

sub calc_GC{
# calculting GC of a sequence & writing

  my ($fasta_r, $file) = @_;

  foreach my $name (keys %$fasta_r){
    # removing gaps #
    $fasta_r->{$name} =~ s/[-.]//g;

    # length
    my $len = length $fasta_r->{$name};

    # GC 
    my %GC = ( G => 0, C => 0);
    while( $fasta_r->{$name} =~ /G/gi ){
      $GC{G}++;
    }
    while( $fasta_r->{$name} =~ /C/gi ){
      $GC{C}++;
    }
    my $GC_sum = $GC{G} + $GC{C};

    # writing output
    if(defined $file){ # writing file name in output
      print join("\t", $file, $name, $len, $GC_sum / $len * 100), "\n";
    }
    else{
      print join("\t", $name, $len, $GC_sum / $len * 100), "\n";
    }
  }

  %$fasta_r = ();
}
