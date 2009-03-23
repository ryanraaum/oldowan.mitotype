from more_assertions import *

from oldowan.mitotype import Motif
from oldowan.mitotype.motif import MotifCollection
from oldowan.mitotype.motif import MotifQuery
from oldowan.mitotype.matcher import MotifMatcher

from oldowan.polymorphism import Polymorphism

p1 = Polymorphism(1,0,'A')
p2 = Polymorphism(2,0,'G')

def test_motif_matcher_initialization():
    """MotifMatcher initialization"""
    # make sure we can create a simple MM without errors
    mm = MotifMatcher(MotifCollection(motifs=[Motif()]))

def test_motif_matcher_attributes():
    """MotifMatcher attributes"""
    mm = MotifMatcher(MotifCollection(motifs=[Motif()]))

    # check that readers can be read and not written
    assert_has_attribute(mm, 'motifs')
    assert_not_assignable(mm, 'motifs')

def test_motif_matcher_matching():
    """MotifMatcher match method"""
    # create some motifs
    m1 = Motif(id='1', label="m1", polymorphisms=(p1,))
    m2 = Motif(id='2', label="m2", polymorphisms=(p2,))
    
    # create a MotifCollection 
    mc = MotifCollection(motifs=[m1, m2])

    # create a new motifmatcher object
    mm = MotifMatcher(mc)

    # create some query objects
    m1query = MotifQuery(defining_polymorphisms=(p1,))
    m2query = MotifQuery(defining_polymorphisms=(p2,))

    # do the match on the first query
    m1match_result = mm.match(m1query)
    # m1 motif should be the best match
    assert_equal( m1, m1match_result.matchdata[0].motif )

    # do the match on the second query
    m2match_result = mm.match(m2query)
    # m2 motif should be the best match
    assert_equal( m2, m2match_result.matchdata[0].motif )

    # in matching, scoring is based on:
    #  - matches:    points added for every variant present in the query that is part of the motif
    #  - mismatches: penalty for every variant present in the query different from the motif
    #                  or present in the motif and different in the query
    #  - extra:      penalty for every variant present in the query and absent from the motif
    #  - missing:    penalty for every variant not in the query but part of the motif


