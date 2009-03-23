from oldowan.mitotype import Motif
from oldowan.polymorphism import Polymorphism
from more_assertions import *
from types import TupleType
from oldowan.mitotype.externals.immutable_dict import ImmutableDict

import re

def test_motif_default_initialization():
    """Motif default initialization"""
    m = Motif()

    # test the default values
    assert_equal('', m.id)
    assert_equal('', m.label)
    assert_equal((), m.sources)
    assert_equal((), m.polymorphisms)

def test_motif_valid_data_initialization():
    """Motif initialization with valid data"""
    good_id = "an id"
    good_label = "a label"
    good_sources = ("Someone 2004",)
    good_polymorphisms = (Polymorphism(1,0,'A'), Polymorphism(2,0,'T'))
    
    m = Motif(id=good_id, 
              label=good_label, 
              sources=good_sources,
              polymorphisms=good_polymorphisms)

    assert_equal(good_id, m.id)
    assert_equal(good_label, m.label)
    assert_equal(good_sources, m.sources)
    assert_equal(good_polymorphisms, m.polymorphisms)

def test_motif_invalid_data_initialization():
    """Motif initialization with invalid data"""
    bad_sources = ["string", 4, {}]
    bad_polymorphisms = [[1,2,3], "string", 5]

    for src in bad_sources:
        assert_raises(Exception, lambda: Motif(sources=src), "Motif \
            initialization should have failed given a sources value \
            of '%s', but didn't" % src)

    for pos in bad_polymorphisms:
        assert_raises(Exception, lambda: Motif(polymorphisms=pos), """Motif 
            initialization should have failed given a polymorphisms value 
            of '%s', but didn't""" % pos)

def test_motif_class_immutability():
    """Motif attributes should be immutable"""
    m = Motif()

    # the Motif attributes id, label, sources, and polymorphisms
    # should be created at initialization and immutable after
    assert_not_assignable(m, "id", "whatever")
    assert_not_assignable(m, "label", "whatever")
    assert_not_assignable(m, "sources", ["whatever"])
    assert_not_assignable(m, "polymorphisms", (Polymorphism(1,0,'A'),))

    # Also, both sources and polymorphisms should be immutable
    #  - sources should be a tuple (immutable by definition)
    #  - polymorphisms should be an ImmutableDict (defined in mt_identify.extras)
    assert_instance_of(TupleType, m.sources)
    assert_instance_of(TupleType, m.polymorphisms)

def test_motif_equality():
    """Motif custom equality comparison"""
    m1 = Motif()
    m2 = Motif()
    assert_equal(m1, m2)

    p1 = Polymorphism(1,0,'A')
    p2 = Polymorphism(2,0,'G')
    p3 = Polymorphism(3,0,'T')

    m1 = Motif(polymorphisms=(p1,p2))
    m2 = Motif(polymorphisms=(p1,p2))
    m3 = Motif(polymorphisms=(p3,p2))
    assert_equal(m1, m2)
    assert_not_equal(m1, m3)

def test_motif_string_representation():
    """Motif string representation"""
    p1 = Polymorphism(1,0,'A')
    p2 = Polymorphism(2,0,'G')
    m = Motif(polymorphisms=(p1,p2))
    assert(re.search("1A", str(m)) is not None)
    assert(re.search("2G", str(m)) is not None)


