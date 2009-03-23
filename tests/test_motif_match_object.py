from more_assertions import *

from oldowan.mitotype import Motif
from oldowan.mitotype.motif import MotifMatchObject

def test_motif_match_object_initialization():
    """MotifMatchObject initialization"""
    # an empty initialization is not ok
    assert_raises(Exception, lambda: MotifMatchObject(),
            "MotifMatchObject should have one essential argument")
    
    # any motif object should fit the bill
    assert(MotifMatchObject(Motif()) is not None)

    # MotifMatchObject instance must have these accessors:
    #  - motif
    #  - match
    #  - mismatch
    #  - extra
    #  - missing
    #  - score
    mmo = MotifMatchObject(Motif())
    assert(mmo.motif is not None)
    assert(mmo.match is not None)
    assert(mmo.mismatch is not None)
    assert(mmo.extra is not None)
    assert(mmo.missing is not None)
    assert(mmo.score is not None)

    # all but score should be unassignable
    assert_not_assignable(mmo, "motif")
    assert_not_assignable(mmo, "match")
    assert_not_assignable(mmo, "mismatch")
    assert_not_assignable(mmo, "extra")
    assert_not_assignable(mmo, "missing")

    # score should have a default (non-calculated) value of -1
    assert_equal(-1, mmo.score)

    # should be able to set and properly retrieve score
    mmo.score = 10
    assert_equal(10, mmo.score)

def test_motif_match_object_string_representation():
    """MotifMatchObject string representation"""
    mmo = MotifMatchObject(Motif(label="hello"))
    assert_find("hello", str(mmo))
    assert_find("scored", str(mmo))

def test_motif_match_object_sorting():
    """MotifMatchObject sorting"""
    mmo1 = MotifMatchObject(Motif())
    mmo1.score = 10
    mmo2 = MotifMatchObject(Motif())
    mmo2.score = 20
    mmo_list = [mmo1, mmo2]
    mmo_list.sort()
    assert_equal(mmo1, mmo_list[0])
    mmo_list.sort(reverse=True)
    assert_equal(mmo2, mmo_list[0])


