import re

def assert_equal(true_value, test_value, msg=''):
    assert (true_value == test_value),\
        '%s was expected, but got %s' % (true_value, test_value)

def assert_not_equal(true_value, test_value, msg=''):
    assert (true_value != test_value), \
        '%s was not expected, but got it' % true_value

def assert_instance_of(klass, obj):
    assert isinstance(obj, klass), \
        '%s is not an instance of %s' % (obj, klass)

def assert_raises(exp, action, msg=''):
    try:
        action()
    except exp:
        pass # this is what we want
    else:
        raise AssertionError(msg)

def assert_has_attribute(obj, attr):
    try:
        obj.__getattribute__(attr)
    except:
        raise AssertionError(
        '%s should have had an attribute"%s", but did not' % (obj, attr))

def assert_not_assignable(obj, attr, val="whatever"):
    try:
        obj.__setattr__(attr, val)
    except:
        pass # this is what we want
    else:
        raise AssertionError('%s should not have been assignable' % attr)

def assert_match(pat, st, msg=''):
    default_msg = "Could not match '%s' to '%s'" % (pat, str)
    assert(re.match(pat, st) is not None, default_msg + '; ' + msg)

def assert_find(pat, st, msg=''):
    default_msg = "Could not find '%s' in '%s'" % (pat, str)
    assert(re.search(pat, st) is not None, default_msg + '; ' + msg)


