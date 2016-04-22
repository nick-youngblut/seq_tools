seq_tools: General tools for working with sequence files
========================================================

# TOOLS

* fasta_info: general info on a fasta (e.g, number of sequences, sequence length, sequence G+C)
* fasta_rename: rename sequences in a fasta file (fuzzy matches allowed)
* fasta_unwrap: unwrap hard-wrapped fastas (resulting sequences are just 1 line)
* filter_seq: Use bioperl to filter out sequences in variously formatted sequence files
* GC_content: Calculate the GC content of a fasta file
* nseq: relatively quick check of number of sequences in fast[aq] file
* seqIntersect: Get the intersection of 2 read files (just same reads in both)
* Tm_calc: calculate the melting temp of >= 1 sequence


# INSTALL

### Clone the repo

```sh
git clone https:github.com/nyoungb2/seq_tools.git
cd seq_tools
```

### set up paths; add bash completion

The command below will add the `seq_tools`
command to your PATH and add bash completion
for viewing subcommands when typing <tab> (much like git).
NOTE: you MUST run the command in the "seq_tools" directory.

```sh
echo 'source '`pwd`'/sourceMe' >> ~/.bashrc
```

# SUPPORT AND DOCUMENTATION

Main command documentation: `seq_tools -h`

Each subcommand has documentation available: `seq_tools [subcommand] -h`


