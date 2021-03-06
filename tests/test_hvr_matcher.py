from more_assertions import *
from oldowan.mitotype.matcher import HVRMatcher
from oldowan.mitotype.prevalidate import ValidationInfo

fasta_text = """> indian
TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACAGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCCCTCCCCATGCTTACAAGCAAGTACAGCAATCAACCCTCAACTATCACACATCAACTGCAACTCCAAAGCCACCCCTCACCCACTAGGATACCAACAAACCTACCCACCCTTAACAGTACATAGTACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGCCCCCATGGATGACCCCCCTCA
> ethiopian
TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACGGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCCCTCCCCATGCTTACAAGCAAGTACAGCAATCAACCTTCAACTATCACACATCACCTGCAACTCCAAAGCCACCCCTCACCCACTAGGATACCAACAAACCTACCCACCCTTAACAGTACATAGCACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGCCCCCATGGATGACCCCCCTCA
"""

def test_initialization():
    """HVRMatcher initialization"""
    hvrm = HVRMatcher()

def test_basic_matching():
    """HVRMatcher match pre-aligned sequences"""
    # some test sequences
    indian    = "TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACAGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCCCTCCCCATGCTTACAAGCAAGTACAGCAATCAACCCTCAACTATCACACATCAACTGCAACTCCAAAGCCACCCCTCACCCACTAGGATACCAACAAACCTACCCACCCTTAACAGTACATAGTACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGCCCCCATGGATGACCCCCCTCA"
    ethiopian = "TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACGGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCCCTCCCCATGCTTACAAGCAAGTACAGCAATCAACCTTCAACTATCACACATCACCTGCAACTCCAAAGCCACCCCTCACCCACTAGGATACCAACAAACCTACCCACCCTTAACAGTACATAGCACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGCCCCCATGGATGACCCCCCTCA"

    hvrm = HVRMatcher()

    imr = hvrm.match(indian)[0]
    emr = hvrm.match(ethiopian)[0]

    # these tests are probably brittle, may break if the 
    # hvr1 motifs data are updated
    assert_equal(14, imr.top_score)
    assert_equal(5, emr.top_score)

    vi = ValidationInfo()
    vi.valid = True
    vi.looks_like = 'dna'

    imr = hvrm.match(indian, vi)[0]
    emr = hvrm.match(ethiopian)[0]
    assert_equal(14, imr.top_score)
    assert_equal(5, emr.top_score)

def test_fasta_matching():
    """HVRMatcher match pre-aligned sequences from FASTA file"""
    hvrm = HVRMatcher()
    matches = hvrm.match_fasta(fasta_text)

    assert_equal('indian', matches[0].query.label)
    assert_equal('ethiopian', matches[1].query.label)

    vi = ValidationInfo()
    vi.valid = True
    vi.looks_like = 'fasta'

    matches = hvrm.match(fasta_text, vi)

    assert_equal('indian', matches[0].query.label)
    assert_equal('ethiopian', matches[1].query.label)


