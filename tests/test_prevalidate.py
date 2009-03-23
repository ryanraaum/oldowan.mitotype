from oldowan.mitotype.prevalidate import looks_like_dna
from oldowan.mitotype.prevalidate import looks_like_fasta
from oldowan.mitotype.prevalidate import looks_like_sites
from oldowan.mitotype.prevalidate import ValidationInfo
from oldowan.mitotype.prevalidate import prevalidate_submission


def test_looks_like_dna():
    """prevalidate: looks_like_dna"""
    # simple should be ok
    assert looks_like_dna('AGCT')
    # gaps (-) should be ok
    assert looks_like_dna('A-G-CT')
    # missing (?) should be ok
    assert looks_like_dna('AG?CT?')
    # IUPAC ambiguous codes should be ok
    assert looks_like_dna('AGCTRYMKWSDBHVN')
    # any of the above should be ok
    assert looks_like_dna('AGCTR-YM?KWSDBHVN')
    # any kind of whitespace should be ok
    assert looks_like_dna('   A\t G\nC\t\t\tT')
    # should still pass
    assert looks_like_dna('AGCT', 
            allow_gaps=False, 
            allow_missing=False, 
            allow_ambiguous=False)
    # should return False 
    assert not looks_like_dna('A-GCT', 
            allow_gaps=False, 
            allow_missing=False, 
            allow_ambiguous=False)
    # but this should be ok
    assert looks_like_dna('A-GCT', 
            allow_missing=False, 
            allow_ambiguous=False)
    # should return False 
    assert not looks_like_dna('A?GCT', 
            allow_gaps=False, 
            allow_missing=False, 
            allow_ambiguous=False)
    # but this should be ok
    assert looks_like_dna('A?GCT', 
            allow_gaps=False, 
            allow_ambiguous=False)
    # should return False 
    assert not looks_like_dna('ARGCT', 
            allow_gaps=False, 
            allow_missing=False, 
            allow_ambiguous=False)
    # but this should be ok
    assert looks_like_dna('ARGCT', 
            allow_gaps=False, 
            allow_missing=False)

def test_looks_like_fasta():
    """prevalidate: looks_like_fasta"""
    assert looks_like_fasta('>monkey\nAGCT')
    assert not looks_like_fasta('monkeymonkeymonkey')

def test_looks_like_sites():
    """prevalidate: looks_like_sites"""
    assert looks_like_sites('16023A')
    assert not looks_like_sites('AAGGCCE')
    assert looks_like_sites('16023A, 16223')
    assert looks_like_sites('16023A,16223-')
    assert looks_like_sites('16023A,16223-, 15987+C')
    assert looks_like_sites('16023A,\n 16223-\t15987+CC')
    assert not looks_like_sites('A,B,C')
    assert not looks_like_sites('16223del')
    assert not looks_like_sites('16223ins')
    assert not looks_like_sites('16223;16445')

def test_ValidationInfo_initialization():
    """prevalidate: ValidationInfo initialization"""
    assert ValidationInfo() is not None

def test_ValidationInfo_attributes():
    """prevalidate: ValidationInfo attributes"""
    vi = ValidationInfo()
    # not valid by default
    assert not vi.valid
    # both data attributes are None by default
    assert vi.looks_like is None
    assert vi.problem is None

def test_prevalidate_submission_with_valid_data():
    """prevalidate: prevalidate_submission with valid data"""
    # first a simple sequence of the proper length
    vi = prevalidate_submission('AGCT'*90)
    assert vi is not None
    assert vi.valid
    assert vi.looks_like is not None
    assert "dna" == vi.looks_like

    # next some fasta looking thing
    vi = prevalidate_submission('>a_sequence\nAGCTTGA')
    assert vi is not None
    assert vi.valid
    assert vi.looks_like is not None
    assert "fasta" == vi.looks_like

    # next some sites
    vi = prevalidate_submission('16223, 16129A 16234+C')
    assert vi is not None
    assert vi.valid
    assert vi.looks_like is not None
    assert "sites" == vi.looks_like

def test_prevalidate_submission_with_invalid_data():
    """prevalidate: prevalidate_submission with invalid data"""
    # first a simple sequence of the proper length
    vi = prevalidate_submission('MONKEY!')
    assert vi is not None
    assert not vi.valid
    assert vi.problem is not None
    assert "doesn't look like" in vi.problem


