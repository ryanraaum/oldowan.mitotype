from more_assertions import *

from oldowan.mitotype.motif import MotifQuery
from oldowan.mitotype.matcher import MotifQueryMaker

from oldowan.polymorphism import Polymorphism

def test_initialization():
    """MotifQueryMaker initialization"""
    qm = MotifQueryMaker()

def test_some_examples():
    """MotifQueryMaker query from pre-aligned sequence"""
    qm = MotifQueryMaker()

    indian    = "TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACAGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCCCTCCCCATGCTTACAAGCAAGTACAGCAATCAACCCTCAACTATCACACATCAACTGCAACTCCAAAGCCACCCCTCACCCACTAGGATACCAACAAACCTACCCACCCTTAACAGTACATAGTACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGCCCCCATGGATGACCCCCCTCA"
    ethiopian = "TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACGGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCCCTCCCCATGCTTACAAGCAAGTACAGCAATCAACCTTCAACTATCACACATCACCTGCAACTCCAAAGCCACCCCTCACCCACTAGGATACCAACAAACCTACCCACCCTTAACAGTACATAGCACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGCCCCCATGGATGACCCCCCTCA"

    indian_query = qm.new_query(indian)
    ethiopian_query = qm.new_query(ethiopian)

    assert_instance_of(MotifQuery, indian_query)
    assert_instance_of(MotifQuery, ethiopian_query)

    #assert_equal(360, len(indian_query.all_polymorphisms))
    #assert_equal(360, len(ethiopian_query.all_polymorphisms))

    assert_equal(2, len(indian_query.defining_polymorphisms))
    assert_equal(4, len(ethiopian_query.defining_polymorphisms))

    assert Polymorphism(16129,0,'A') in indian_query.defining_polymorphisms
    assert Polymorphism(16362,0,'C') in indian_query.defining_polymorphisms

    assert Polymorphism(16362,0,'C') in ethiopian_query.defining_polymorphisms
    assert Polymorphism(16241,0,'C') in ethiopian_query.defining_polymorphisms
    assert Polymorphism(16311,0,'C') in ethiopian_query.defining_polymorphisms
    assert Polymorphism(16223,0,'T') in ethiopian_query.defining_polymorphisms

def test_new_queries_from_unaligned_LONG():
    """MotifQueryMaker query from unaligned sequence"""
    qm = MotifQueryMaker()

    indian = "TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACAGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCCCTCCCCATGCTTACAAGCAAGTACAGCAATCAACCCTCAACTATCACACATCAACTGCAACTCCAAAGCCACCCCTCACCCACTAGGATACCAACAAACCTACCCACCCTTAACAGTACATAGTACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGCCCCCATGGATGACCCCCCTCA"

    a_indian = indian[3:-3]  

    query = qm.new_query(a_indian)

    #assert_equal(360, len(query.all_polymorphisms))
    assert_equal(2, len(query.defining_polymorphisms))

    assert Polymorphism(16129,0,'A') in query.defining_polymorphisms
    assert Polymorphism(16362,0,'C') in query.defining_polymorphisms

    b_indian = indian[:100] + indian[101:] 

    query = qm.new_query(b_indian)

    assert_equal(3, len(query.defining_polymorphisms))

    assert Polymorphism(16129,0,'A') in query.defining_polymorphisms
    assert Polymorphism(16362,0,'C') in query.defining_polymorphisms

def test_new_query_from_site_str():
    """MotifQueryMaker query from sites string"""
    
    qm = MotifQueryMaker()

    sites = '16129A 16362C'

    query = qm.new_query_from_sites(sites)

    assert_equal(2, len(query.defining_polymorphisms))

    print query.defining_polymorphisms
    assert Polymorphism(16129,0,'A') in query.defining_polymorphisms
    assert Polymorphism(16362,0,'C') in query.defining_polymorphisms


