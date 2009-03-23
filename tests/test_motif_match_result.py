from more_assertions import *
from nose import with_setup

from oldowan.mitotype import Motif
from oldowan.mitotype.motif import MotifMatchResult
from oldowan.mitotype.motif import MotifMatchObject
from oldowan.mitotype.motif import MotifQuery

from oldowan.polymorphism import Polymorphism

p1 = Polymorphism(1,0,'A')
p2 = Polymorphism(2,0,'G')
p3 = Polymorphism(2,0,'A')

def test_motif_match_result_initialization():
    """MotifMatchResult initialization"""
    # make sure we can create a simple MMR without errors
    assert(MotifMatchResult(MotifQuery(), []) is not None)
    mmr = MotifMatchResult(MotifQuery(), [])

    # now check default values
    assert_equal(2, mmr.match_value)
    assert_equal(2, mmr.mismatch_penalty)
    assert_equal(1, mmr.extra_penalty)
    assert_equal(1, mmr.missing_penalty)
    assert_equal(10, mmr.perfect_bonus)

def test_motif_match_result_attribute_accessors():
    """MotifMatchResult attribute accessors"""
    mmr = MotifMatchResult(MotifQuery(), [])

    # check that attributes can be read
    assert_has_attribute(mmr, "matchdata")
    assert_has_attribute(mmr, "match_value")
    assert_has_attribute(mmr, "mismatch_penalty")
    assert_has_attribute(mmr, "extra_penalty")
    assert_has_attribute(mmr, "missing_penalty")
    assert_has_attribute(mmr, "perfect_bonus")

def test_motif_match_result_attributes():
    """MotifMatchResult attributes should be immutable"""
    mmr = MotifMatchResult(MotifQuery(), [])

    assert_not_assignable(mmr, "matchdata")
    assert_not_assignable(mmr, "match_value")
    assert_not_assignable(mmr, "mismatch_penalty")
    assert_not_assignable(mmr, "extra_penalty")
    assert_not_assignable(mmr, "missing_penalty")
    assert_not_assignable(mmr, "perfect_bonus")

def test_score():
    """MotifMatchResult scoring"""
    m = Motif(polymorphisms=(p1,))
    mmo = MotifMatchObject(m, match=1)
    mq = MotifQuery(all_polymorphisms=(p1,p2), 
                    defining_polymorphisms=(p1,))
    mmr = MotifMatchResult(mq, [mmo])
    mmr.score()

def test_sort():
    """MotifMatchResult sorting"""
    m1 = Motif(polymorphisms=(p1,))
    mmo1 = MotifMatchObject(m1, match=1)
    m2 = Motif(polymorphisms=(p3,))
    mmo2 = MotifMatchObject(m2, mismatch=1)
    mq = MotifQuery(all_polymorphisms=(p1,p2), 
                    defining_polymorphisms=(p1,))
    mmr = MotifMatchResult(mq, [mmo2, mmo1])
    assert_equal(mmo1, mmr.matchdata[0])
    assert_equal(mmo2, mmr.matchdata[1])

def test_top_matches():
    """MotifMatchResult top_matches"""
    m1 = Motif(polymorphisms=(p1,))
    mmo1 = MotifMatchObject(m1, match=1)
    m2 = Motif(polymorphisms=(p3,))
    mmo2 = MotifMatchObject(m2, mismatch=1)
    mq = MotifQuery(all_polymorphisms=(p1,p2), 
                    defining_polymorphisms=(p1,))
    mmr = MotifMatchResult(mq, [mmo2, mmo1])
    assert_equal(mmo1, mmr.matchdata[0])
    assert_equal(mmo2, mmr.matchdata[1])

    assert_equal(12, mmr.top_score)

def test_filter_by():
    """MotifMatchResult filter_by"""
    m1 = Motif(polymorphisms=(p1,), sources=['a', 'b'])
    mmo1 = MotifMatchObject(m1, match=1, missing=1)
    m2 = Motif(polymorphisms=(p3,), sources=['a'])
    mmo2 = MotifMatchObject(m2, mismatch=1)
    m3 = Motif(polymorphisms=(p1,p2), sources=['b'])
    mmo3 = MotifMatchObject(m3, match=2)

    mq = MotifQuery(all_polymorphisms=(p1,p2), 
                    defining_polymorphisms=(p1,p2))
    mmr = MotifMatchResult(mq, [mmo1, mmo2, mmo3])

    assert_equal(14, mmr.top_score)

    mmr.filter_by(source='a')
    assert_equal(1, mmr.top_score)

    mmr.reset_filter()
    assert_equal(14, mmr.top_score)

    mmr.filter_by(sources_in=['a'])
    assert_equal(1, mmr.top_score)

    mmr.reset_filter()
    assert_equal(14, mmr.top_score)



