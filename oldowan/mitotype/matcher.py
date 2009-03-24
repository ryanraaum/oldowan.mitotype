from oldowan.mitotype.motif import MotifMatchResult
from oldowan.mitotype.motif import MotifMatchObject
from oldowan.mitotype.motif import MotifCollection
from oldowan.mitotype.motif import MotifQuery

from oldowan.mtconvert import seq2sites, str2sites

from oldowan.fasta import fasta

from pkg_resources import resource_string, resource_filename

import shelve


class MotifQueryMaker(object):
    
    def new_query(self, seq, label='Query'):
        all_polymorphisms  = {}
        defining_polymorphisms = {}

        return MotifQuery(defining_polymorphisms=seq2sites(seq), label=label)

    def new_query_from_sites(self, sites, label='Query', add16k=False):

        return MotifQuery(defining_polymorphisms=str2sites(sites, add16k), label=label)


class MotifMatcher(object):

    def __init__(self, motif_collection):
        self.__motifs = motif_collection

    def __get_motifs(self):
        return self.__motifs

    motifs = property(fget=__get_motifs)

    def match(self, query):

        matchdata = []
      
        for m in self.__motifs.itervalues():
            missing  = 0
            match    = 0
            mismatch = 0
            extra    = 0

            # first looking from the query defining polymorphisms side
            for q_poly in query.defining_polymorphisms:
                # query defining position not part of motif
                if not q_poly in m.polymorphisms:
                    extra += 1
                # or query defining position part of motif and value matches
                elif q_poly in m.polymorphisms:
                    match += 1
                # otherwise, must be a mismatch
                else:
                    mismatch += 1

            # NOTE: if we are only given defining polymorphisms 
            # (i.e. don't know which polymorphisms
            # the query actually covers), then when a 
            # motif value is not one of the
            # query defining polymorphisms, we can't tell if 
            # that is because those data aren't 
            # known ('missing') or those data are 
            # known and the value is not a
            # variant ('mismatch').  The algorithm 
            # here errs on the side of caution
            # and will call these 'missing'.
        
            # next, we want to find any further missing and mismatch polymorphisms
            for m_poly in m.polymorphisms:
                # if a motif position is not a variant, 
                # but the position exists in
                # the query, then it is a mismatch
                if not m_poly in query.defining_polymorphisms:
                    if m_poly in query.all_polymorphisms:
                        mismatch += 1
                    # if it's not in the query at all, it's missing
                    else: 
                        missing += 1

            md = MotifMatchObject(m, match=match,
                                     mismatch=mismatch,
                                     missing=missing,
                                     extra=extra)
            matchdata.append(md)
      
        return MotifMatchResult(query, matchdata)


class HVRMatcher(object):

    def __init__(self):
        
        try:
            # first try to load hvr1 motif collection from shelve
            shelf_fn = resource_filename(__name__, 
                    '../../data/motifs.shelved')
            shelf = shelve.open(shelf_fn)
            mc = shelf['hvr1']
            shelf.close()
            self.__mm = MotifMatcher(mc)
        except:
            # create the motif collection from the starting yaml
            # (this is much, much slower...)
            motif_yaml = resource_string(__name__, 
                    '../../data/hvr1_motifs.yaml')
            self.__mm = MotifMatcher(MotifCollection(yaml=motif_yaml))

        # create a query maker
        self.__qm = MotifQueryMaker()

    def match(self, text, validation_info=None, label='Query'):
        if validation_info is None:
            return self.match_sequence(text, label=label)
        if validation_info.valid:
            if 'dna' == validation_info.looks_like:
                return self.match_sequence(text, label=label)
            elif 'fasta' == validation_info.looks_like:
                return self.match_fasta(text)
            elif 'sites' == validation_info.looks_like:
                return self.match_sites(text, label=label)
            raise ArgumentError("Don't know how to handle input that "\
                    "looks like '%s'" % validation_info.looks_like)
        else:
            raise ArgumentError("ValidationInfo instance given is not valid")

    def match_sequence(self, seq, label='Query'):
        return [self.__mm.match(self.__qm.new_query(seq, label=label))]

    def match_sites(self, sites, label='Query'):
        return [self.__mm.match(self.__qm.new_query_from_sites(sites, label=label))]

    def match_fasta(self, fasta_text, do_align=False):
        fasta_fileobj = fasta(fasta_text, 's').readentries()

        queries = []   
        for entry in fasta_fileobj:
            query = self.__qm.new_query(entry['sequence'])
            query.label = entry['name']
            queries.append(query)
        return [self.__mm.match(q) for q in queries]

