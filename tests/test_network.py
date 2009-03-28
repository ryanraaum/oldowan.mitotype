import os

from oldowan.mitotype.network import read_network_csv, network_haplotypes

CSV_FILEPATH = os.path.join(os.path.dirname(__file__), 
        'test_files', 'genebase.csv')

def test_read_network_csv():
    """Read haplotype network from my csv format."""
    assert read_network_csv(CSV_FILEPATH) is not None

def test_network_haplotypes():
    """Extract haplotypes from a network."""
    g = read_network_csv(CSV_FILEPATH)
    assert network_haplotypes(g) is not None
