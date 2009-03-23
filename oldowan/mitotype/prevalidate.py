import re, string

DNA_ALLOK = re.compile('^[-?AGCTRYMKWSDBHVN]+$', re.I)
DNA_NOGAP = re.compile('^[?AGCTRYMKWSDBHVN]+$', re.I)
DNA_NOMISSING = re.compile('^[-AGCTRYMKWSDBHVN]+$', re.I)
DNA_NOAMBIG = re.compile('^[-?AGCT]+$', re.I)
DNA_NOGAP_NOMISSING = re.compile('^[AGCTRYMKWSDBHVN]+$', re.I)
DNA_NOGAP_NOAMBIG = re.compile('^[?AGCT]+$', re.I)
DNA_NOMISSING_NOAMBIG = re.compile('^[-AGCT]+$', re.I)
DNA_STRICT = re.compile('^[AGCT]+$', re.I)

def looks_like_dna(test_text, 
        allow_gaps=True, 
        allow_missing=True, 
        allow_ambiguous=True):
    """Determine if text looks like dna sequence.

    Checks to see if the test text could plausibly be DNA 
    sequence data. Whitespace is stripped out before the test. 
    With default settings, gaps (-) are OK,
    missing (?) is OK, and ambiguous (RYMKWSBDHVN) bases are OK.
    Case is ignored.
    """
    text = test_text.translate(string.maketrans("",""), string.whitespace)
    if allow_gaps and allow_missing and allow_ambiguous:
        return DNA_ALLOK.match(text) is not None
    elif not allow_gaps and allow_missing and allow_ambiguous:
        return DNA_NOGAP.match(text) is not None
    elif allow_gaps and not allow_missing and allow_ambiguous:
        return DNA_NOMISSING.match(text) is not None
    elif allow_gaps and allow_missing and not allow_ambiguous:
        return DNA_NOAMBIG.match(text) is not None
    elif not allow_gaps and not allow_missing and allow_ambiguous:
        return DNA_NOGAP_NOMISSING.match(text) is not None
    elif not allow_gaps and allow_missing and not allow_ambiguous:
        return DNA_NOGAP_NOAMBIG.match(text) is not None
    elif allow_gaps and not allow_missing and not allow_ambiguous:
        return DNA_NOMISSING_NOAMBIG.match(text) is not None
    else:
        return DNA_STRICT.match(text) is not None

FASTA_START = re.compile('^>[^\n]+$[^>]', re.M)

def looks_like_fasta(test_text):
    """Determine if text looks like FASTA formatted data.

    Looks to find at least two lines. The first line MUST 
    start with '>' and the second line must NOT start with '>'.
    Ignores any starting whitespace.  
    """
    text = test_text.strip()
    return FASTA_START.match(text) is not None

SITE_TRANSITION = re.compile('^[0-9]+$')
SITE_EXPLICIT = re.compile('^[0-9]+[AGCT]$', re.I)
SITE_DELETION = re.compile('^[0-9]+-$', re.I)
SITE_INSERTION = re.compile('^[0-9]+\+[AGCT]+$', re.I)

SITE_SPLITTER = re.compile('[,\s]+')

def looks_like_sites(test_text):
    """Determine if text looks like variant sites (i.e. 16223C)

    Sites may be separated by whitespace or commas. Acceptable 
    formats are: 
    
    16223    : Differs by a transition at site 16223
    16223C   : 'C' at 16223 (implies reference does not 'C')
    16223-   : Missing reference site 16223
    16223+C  : One 'C' inserted after reference site 16223
    16223+CC : Two 'C's inserted after reference site 16223
    """
    entries = SITE_SPLITTER.split(test_text)
    for entry in entries:
        if (SITE_TRANSITION.match(entry) or SITE_EXPLICIT.match(entry)
                or SITE_DELETION.match(entry) or SITE_INSERTION.match(entry)) is None:
            return False
    return True
    
class ValidationInfo(object):

    def __init__(self):
        self.valid = False
        self.looks_like = None
        self.problem = None

def prevalidate_submission(submitted_text):
    """Determine if the submitted text seems handleable
    
    Returns a ValidationObject.
    """
    vi = ValidationInfo()
    if submitted_text == '':
        vi.problem = "Nothing submitted."
    elif looks_like_fasta(submitted_text):
        vi.valid = True
        vi.looks_like = 'fasta'
    elif looks_like_dna(submitted_text):
        vi.valid = True
        vi.looks_like = 'dna'
    elif looks_like_sites(submitted_text):
        vi.valid = True
        vi.looks_like = 'sites'
    else:
        vi.problem = "Submission doesn't look like DNA sequence, "\
                "FASTA formatted sequences, or defining sites."
    return vi
    

