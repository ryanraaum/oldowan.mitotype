"""This is the oldowan.mitotype package."""

import os

VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION')).read().strip()

__all__ = ['read_network_csv', 'network_haplotypes', 'Motif', 'MotifCollection'] 

try:
    from oldowan.mitotype.network import read_network_csv
    from oldowan.mitotype.network import network_haplotypes
    from oldowan.mitotype.motif import Motif
    from oldowan.mitotype.motif import MotifCollection
except:
    from network import read_network_csv
    from network import network_haplotypes
    from motif import Motif
    from motif import MotifCollection
