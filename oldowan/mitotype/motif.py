from externals.immutable_dict import ImmutableDict
from oldowan.polymorphism import Polymorphism

from yaml import load as load_yaml

class Motif(object):
    """A haplotype-defining motif class.
    
    Motifs hold information about haplotype definitions. These attributes are:
        - id            (a string or string-coerceable object)
        - label         (a string or string-coercable object)
        - sources       (a tuple, list, or set that will be tupled)
        - polymorphisms (a tuple, list, or set that will be tupled)

    Motifs are (or should be) absolutely immutable, all attributes are
    fixed at initialization.

    """

    def __init__(self, id='', label='', sources=(), polymorphisms=()):
        """Create a new motif instance.

        Default values are provided for all of the arguments, so an empty
        initialization is valid.  However, as Motif instances are immutable,
        you will almost never use the default 'polymorphisms' value.

        """
        self.__id = id
        self.__label = label
        if type(sources) == type(()) or type(sources) == type([]):
            # pass list or tuple type sources through a set initialization 
            # as the entries should be set-like, but make it a tuple in the 
            # end as we want immutability
            self.__sources = tuple(set(sources))
        elif type(sources) == type(set()):
            self.__sources == tuple(sources)
        else:
            raise AttributeError("'sources' argument must be provided as \
                    a list, tuple, or set")
        if type(polymorphisms) == type(()) or type(polymorphisms) == type([]):
            # pass list or tuple type sources through a set initialization 
            # as the entries should be set-like, but make it a tuple in the 
            # end as we want immutability
            self.__polymorphisms = tuple(set(polymorphisms))
        elif type(polymorphisms) == type(set()):
            self.__sources == tuple(polymorphisms)
        else:
            raise AttributeError("'polymorphisms' argument must be provided as \
                    a list, tuple, or set")

        for poly in self.__polymorphisms:
            if not isinstance(poly, Polymorphism):
                raise AttributeError("objects provided as polymorphisms must be Polymorphisms")

    def __get_id(self):
        return self.__id

    def __get_label(self):
        return self.__label

    def __get_sources(self):
        return self.__sources

    def __get_polymorphisms(self):
        return self.__polymorphisms

    id = property(fget=__get_id)
    label = property(fget=__get_label)
    sources = property(fget=__get_sources)
    polymorphisms = property(fget=__get_polymorphisms)

    def __eq__(self, other):
        """Motif objects are equal when labels and polymorphisms are the same"""
        if self.label == other.label and \
          len(self.polymorphisms) == len(other.polymorphisms):
            same = True
            for poly in self.polymorphisms: 
                if poly not in other.polymorphisms:
                    same = False
            return same
        return False 

    def __repr__(self):
        l = []
        for poly in self.polymorphisms: 
            l.append('%s' % str(poly))
        return ', '.join(l)



class MotifCollection(dict):
    '''A dictionary of Motifs.
    
    This is a very thin wrapper over the standard Python Dictionary
    class, primarily providing an initialization routine.

    '''
    
    def __init__(self, yaml="", motifs=None):
        '''Create a new collection of Motifs.

        There are two possible arguments, only one of which will be
        used for any given initialization, in the order that they are
        listed:
         1. yaml="a yaml string"
         2. motifs=[] (a list of Motif objects)

        For example:

          MotifCollection(yaml="---\n <etc>")
          MotifCollection(motifs=[M1, M2, M3])

        '''
        self.__sources = set()

        if yaml != "":
            self._process_yaml(yaml)
        elif motifs:
            for m in motifs:
                self[m.id] = m
                self.__sources.update(m.sources)
        else:
            raise TypeError, 'MotifCollection initialization requires '\
                             'a valid yaml string or motif list.'


    def __get_sources(self):
        return self.__sources

    sources = property(fget=__get_sources)

    def _process_yaml(self, yaml_string):
        yaml_motifs = load_yaml(yaml_string)
        for entry in yaml_motifs:
            polys = list(Polymorphism(int(k),0,v) for k,v in entry['polymorphisms'].iteritems())
            self[entry['id']] = Motif(id=entry['id'],
                                      label=entry['label'],
                                      sources=entry['source'],
                                      polymorphisms=polys)
            self.__sources.update(self[entry['id']].sources)

    def to_yaml(self):
        yaml_list = ['---']
        for motif in self.itervalues():
            yaml_list.append('- "id": %s' % motif.id)
            yaml_list.append('  "label": %s' % motif.label)
            yaml_list.append('  "source":')
            for src in motif.sources:
                yaml_list.append('  - %s' % src)
            if len(motif.polymorphisms) > 1:
                yaml_list.append('  "polymorphisms":')
                for poly in motif.polymorphisms:
                    yaml_list.append('    "%d": %s' % (poly.position, poly.value))
            else:
                yaml_list.append('  "polymorphisms": {}')
                yaml_list.append('')
        return '\n'.join(yaml_list)


class MotifMatchObject(object):
    """A container for information about a Motif match."""

    def __init__(self, motif, match=0, mismatch=0, extra=0, missing=0):
        self.__motif = motif
        self.__match = match
        self.__mismatch = mismatch
        self.__extra = extra
        self.__missing = missing
        self.score = -1

    def __get_motif(self):
        return self.__motif

    def __get_match(self):
        return self.__match

    def __get_mismatch(self):
        return self.__mismatch

    def __get_extra(self):
        return self.__extra

    def __get_missing(self):
        return self.__missing

    motif = property(fget=__get_motif)
    match = property(fget=__get_match)
    mismatch = property(fget=__get_mismatch)
    extra = property(fget=__get_extra)
    missing = property(fget=__get_missing)

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

    def __eq__(self, other):
        return self.score == other.score

    def __repr__(self):
        return "%s, scored %d for motif %s (%s)" % \
            (self.motif.label, self.score, self.motif, 
                    ', '.join(self.motif.sources))


class MotifMatchResult(object):

    def __init__(self, query, matchdata, match_value=2, mismatch_penalty=2,
            extra_penalty=1, missing_penalty=1, perfect_bonus=10):
        self.__query = query
        self.__matchdata = matchdata
        self.__all_matchdata = matchdata
        self.__matchdata = self.__all_matchdata
        self.__match_value = match_value
        self.__mismatch_penalty = mismatch_penalty
        self.__extra_penalty = extra_penalty
        self.__missing_penalty = missing_penalty
        self.__perfect_bonus = perfect_bonus
        # make sure results are scored, sorted,
        # and ready to be used
        self.score()
        self.sort()

    def __get_query(self):
        return self.__query

    def __get_matchdata(self):
        return self.__matchdata

    def __get_match_value(self):
        return self.__match_value

    def __get_mismatch_penalty(self):
        return self.__mismatch_penalty

    def __get_extra_penalty(self):
        return self.__extra_penalty

    def __get_missing_penalty(self):
        return self.__missing_penalty

    def __get_perfect_bonus(self):
        return self.__perfect_bonus

    def __get_top_score(self):
        return self.__matchdata[0].score

    query = property(fget=__get_query)
    matchdata = property(fget=__get_matchdata)
    match_value = property(fget=__get_match_value)
    mismatch_penalty = property(fget=__get_mismatch_penalty)
    extra_penalty = property(fget=__get_extra_penalty)
    missing_penalty = property(fget=__get_missing_penalty)
    perfect_bonus = property(fget=__get_perfect_bonus)
    top_score = property(fget=__get_top_score)

    def score(self):
        for md in self.matchdata:
            md.score = 0
            md.score += md.match    * self.match_value
            md.score -= md.mismatch * self.mismatch_penalty 
            md.score -= md.missing  * self.missing_penalty
            md.score -= md.extra    * self.extra_penalty
            if md.match == len(md.motif.polymorphisms) and md.extra + md.missing == 0:
                md.score += self.perfect_bonus

    def sort(self):
        self.matchdata.sort(reverse=True)

    def filter_by(self, source=None, sources_in=None):
        """Filter the match objects by various criteria.

        NOTE: filter_by always starts with the complete set of match objects!
        So successive filter_by calls are not additive - put all the filters
        you want in the same call.
        """
        result = self.__all_matchdata
        if source:
            result = [m for m in result if source in m.motif.sources]
        if sources_in:
            in_set = set(sources_in)
            result = [m for m in result if in_set.intersection(m.motif.sources)]
        self.__matchdata = result

    def reset_filter(self):
        """Return to un-filtered state, all match objects enabled."""
        self.__matchdata = self.__all_matchdata

    def __repr__(self):
        lines = [str(self.__query)] 
        for md in self.matchdata:
            if md.score < self.top_score:
                break
            lines.append('  ' + str(md))
        return '\n'.join(lines) 

    def csv_rows(self):
        """Return an array of csv rows.
    
        Each row has these fields (in this order): 
            Query Label
            Query Defining polymorphisms
            Motif Label
            Motif Defining polymorphisms
            Motif Source
        """
        rows = []
        for md in self.matchdata:
            if md.score < self.top_score:
                break
            # create a list of query polymorphisms
            query_polys_list = []
            for poly in self.query.defining_polymorphisms:
                query_polys_list.append(str(poly))
            # create a list of motif polymorphisms
            motif_polys_list = []
            for poly in md.motif.polymorphisms:
                motif_polys_list.append(str(poly))
            info = (self.query.label,
                    ' '.join(query_polys_list),
                    md.motif.label,
                    md.score,
                    ' '.join(motif_polys_list),
                    '; '.join(md.motif.sources),
                    )
            rows.append('%s,%s,%s,%d,%s,%s' % info)
        return rows


class MotifQuery(object):

    def __init__(self, defining_polymorphisms=(), all_polymorphisms=(), label='Query'):
        self.__defining_polymorphisms = tuple(defining_polymorphisms)
        self.__all_polymorphisms = tuple(all_polymorphisms)
        self.label = label

    def __get_all_polymorphisms(self):
        return self.__all_polymorphisms

    def __get_defining_polymorphisms(self):
        return self.__defining_polymorphisms

    all_polymorphisms = property(fget=__get_all_polymorphisms)
    defining_polymorphisms = property(fget=__get_defining_polymorphisms)

    def __repr__(self): 
        str_list = []
        if len(self.all_polymorphisms) > 0:
            str_list.append("%s covers %d polymorphisms, with %d defining:" 
                % (self.label, len(self.all_polymorphisms), len(self.defining_polymorphisms)))
        else:
            str_list.append("%s has %d defining polymorphisms:" 
                % (self.label, len(self.defining_polymorphisms)))
        for poly in self.defining_polymorphisms:
            str_list.append(str(poly))
        return ' '.join(str_list)

