"""This is the oldowan.mitotype package."""

import os

VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION')).read().strip()

__all__ = ['Motif',      
           'MotifCollection',
           'HVRMatcher',
           'prevalidate_submission'] 

try:
    from oldowan.mitotype.motif import Motif
    from oldowan.mitotype.motif import MotifCollection
    from oldowan.mitotype.matcher import HVRMatcher
    from oldowan.mitotype.prevalidate import prevalidate_submission
except:
    from motif import Motif
    from motif import MotifCollection
    from matcher import HVRMatcher
    from prevalidate import prevalidate_submission
