import cStringIO

class StringCloner(object):
    """
    Clones a string.  This has proven to be kinda tricky.
    copy.copy(), copy.deepcopy() only return the reference to
    a python string.  Normally, strings are immutable and this is the
    right thing to do.  NLot so effective when strings aren't so immutable.

    "".join(somestring) works for copying but is pretty slow.

    So far the fastest way to clone without creating another c extension
    is to write to a string io buffer and then request the value
    for as many times as it is needed
    """

    def __init__(self, toclone):
        """
        Inits the string cloner.  Opens a cStringIO buffer and writes
        the original string to it
        """
        self.stream = cStringIO.StringIO()
        self.stream.write(toclone)

    def __enter__(self):
        """
        For use with the the with context
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Close the stream when exiting the with context
        """
        self.stream.close()

    def clone(self):
        """
        Return a copy of the string
        """
        return self.stream.getvalue()
