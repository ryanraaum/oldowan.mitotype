from more_assertions import *

from oldowan.mitotype.motif import MotifQuery
from oldowan.mitotype.externals.immutable_dict import ImmutableDict

from oldowan.polymorphism import Polymorphism

def test_motif_query():
    """MotifQuery, initialization"""
    # an empty initialization is ok
    assert(MotifQuery() is not None)
    
    # MotifQuery instance must have 'all_polymorphisms' 
    # and 'defining_polymorphisms' accessors
    mq = MotifQuery()
    assert(mq.all_polymorphisms is not None)
    assert(mq.defining_polymorphisms is not None)

    # only readers, not writers
    assert_not_assignable(mq, "all_polymorphisms")
    assert_not_assignable(mq, "defining_polymorphisms")

def test_motif_query_string_representation():
    """MotifQuery, string representation"""
    p1 = Polymorphism(1,0,'A')
    p2 = Polymorphism(2,0,'G')
    mq = MotifQuery(all_polymorphisms=(p1,p2), 
            defining_polymorphisms=(p1,))
    assert_match("Query covers 2 polymorphisms, with 1 defining", str(mq))
    assert_find("1A", str(mq))

