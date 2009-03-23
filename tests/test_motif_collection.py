from oldowan.mitotype import MotifCollection
from oldowan.mitotype import Motif
from more_assertions import *
from types import StringType

MOTIF_TEST_YAML = """---
- "id": 516
  "label": N1-I
  "source":
  - Kivisild et al 2004
  - Metspalu et al 2004
  "polymorphisms":
    "16129": A
    "16189": C
    "16223": T
- "id": 1549
  "label": M
  "source":
  - Metspalu et al 2004
  "polymorphisms":
    "16172": C
    "16223": T
    "16039": T
- "id": 1
  "label": H
  "source":
  - Metspalu et al 2004
  - Kivisild et al 2004
  - Richards et al 2000
  "polymorphisms": {}

- "id": 2582
  "label": U2
  "source":
  - Metspalu et al 2004
  "polymorphisms":
    "16051": G
    "16086": C
    "16353": T
    "16291": T
    "16259": T
- "id": 1033
  "label": H
  "source":
  - Metspalu et al 2004
  "polymorphisms":
    "16129": A
    "16300": G
"""

def test_motif_collection_yaml_loading():
    """MotifCollection intialization with yaml data"""
    mc = MotifCollection(yaml=MOTIF_TEST_YAML)
    assert_equal(5, len(mc))
    assert(mc.has_key(516))
    assert(mc.has_key(1549))
    assert(mc.has_key(1))
    assert(mc.has_key(2582))
    assert(mc.has_key(1033))

def test_motif_collection_motifs_loading():
    """MotifCollection intialization with Motif list"""
    m1 = Motif(id=1, label="1")
    m2 = Motif(id=2, label="2")
    m3 = Motif(id=3, label="3")
    mc = MotifCollection(motifs=[m1, m2, m3])

    assert_equal(3, len(mc))
    assert(mc.has_key(1))
    assert(mc.has_key(2))
    assert(mc.has_key(3))

    assert_equal("1", mc[1].label)
    assert_equal("2", mc[2].label)
    assert_equal("3", mc[3].label)

def test_motif_collection_to_yaml():
    """MotifCollection yaml export
    
    Test MotifCollection's to_yaml method by loading a motifs definition 
    string, then converting it back to yaml via the to_yaml method,
    then reloading the new yaml file and comparing with the original.
    """

    mc1 = MotifCollection(yaml=MOTIF_TEST_YAML)
    assert_instance_of(StringType, mc1.to_yaml())
    mc2 = MotifCollection(yaml=mc1.to_yaml())

    assert_equal(len(mc1), len(mc2))

    for key in mc1:
        assert(mc2.has_key(key))
        assert_equal(mc1[key].id, mc2[key].id)
        assert_equal(mc1[key].label, mc2[key].label)

        assert_equal(len(mc1[key].sources), len(mc2[key].sources))
        for val in mc1[key].sources:
            assert(val in mc2[key].sources)

        assert_equal(len(mc1[key].polymorphisms), len(mc2[key].polymorphisms))
        for poly in mc1[key].polymorphisms:
            assert poly in mc2[key].polymorphisms

def test_motif_collection_sources_methods():
    """MotifCollection sources attribute"""
    mc = MotifCollection(yaml=MOTIF_TEST_YAML)

    assert_has_attribute(mc, 'sources')
    assert_instance_of(set, mc.sources)
    assert_not_assignable(mc, 'sources')

    assert_equal(3, len(mc.sources))
    


