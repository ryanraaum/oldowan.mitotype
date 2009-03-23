from optparse import OptionParser
import os,sys

from oldowan.mitotype.hvr_matcher import HVRMatcher
from oldowan.mitotype.prevalidate import prevalidate_submission

def run_command():
    """Perform automated human mtDNA haplotype identification."""

    # Set up the options parser
    usage = "usage: %prog [options] sequence|filename"
    parser = OptionParser(usage=usage)
    parser.add_option('-f',
                      '--file',
                      action='store_true',
                      default=False,
                      help='load sequences from FASTA file',
                      dest='use_file')
    parser.add_option('-c',
                      '--csv',
                      action='store_true',
                      dest='csv',
                      default=False,
                      help='output in comma-separated-value format')
    parser.add_option('-n',
                      '--no-csv-header',
                      action='store_false',
                      dest='csv_header',
                      default=True,
                      help='output a csv header')
    parser.add_option('-o',
                      '--out',
                      dest='outfile',
                      help='write results to FILE',
                      default=False,
                      metavar='FILE')

    # Parse the options
    (options, args) = parser.parse_args()

    # At least one argument is always required.
    # It will be either the sequence to be tested, or
    # When the -f flag is used, the filename of the fasta file
    # to be tested
    if len(args) != 1:
        if options.use_file:
            print 'You must provide a filename!'
            print "Type 'mitotype -h' for help."
        else:
            print 'You must provide a sequence to test'
            print "Type 'mitotype -h' for help."
        sys.exit(1)

    # If we've made it this far we're probably going to have to do some
    # actual work; initialize the matcher.
    hvrm = HVRMatcher()

    # Do the work, either:
    # (1) load the fasta file
    # (2) use sequence passed on the command line
    working_text = ''
    if options.use_file:
        if os.path.exists(args[0]):
            f = open(args[0], 'r')
            working_text = f.read()
            f.close()
        else:
            print 'ERROR: Could not find file: %s' % args[0]
            sys.exit(1)
    else:
        working_text = args[0]

    vi = prevalidate_submission(working_text)
    if not vi.valid:
        print 'ERROR: Could not validate input: %s' % vi.problem

    results = hvrm.match(working_text, vi, do_align=options.align)

    # If outfile option is used, make stdout point to that file
    if options.outfile:
        outf = open(options.outfile, 'w')
        sys.stdout = outf

    # If we're outputing to CSV, spit out a header
    if options.csv and options.csv_header:
        print 'Query Label,Query Defining Positions,Motif Label,Match Score,Motif Defining Positions,Source'

    # Output the results
    for r in results:
        if options.csv:
            for row in r.csv_rows():
                print row
        else:
            print r
        sys.stdout.flush()

