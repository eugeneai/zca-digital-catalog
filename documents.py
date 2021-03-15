from zope.interface import Interface, implementer, Attribute
from zope.component import getGlobalSiteManager, adapter

# --------- Interfaces ---------------------------

class IFile(Interface):
    """Interface describes files"""
    body = Attribute("The body of the file")

class IImage(Interface):
    """Interface describes various images"""
    picture = Attribute("The picture's pixels")

class IDocument(Interface):
    """Interface describes documents of a logical structure."""
    content = Attribute("The content of the document")


class ISize(Interface):
    """Defines the size attribute of an object"""
    def getsize()->int:
        """Returns the size of an object"""

class IByteSize(ISize):
    """Defines the size attribute in bytes of an object"""


class ICatalog(Interface):
    """Defines set of methods manipulating catalogs of
    documents"""

    documents = Attribute("A data structure storing documents")

    def add(document):
        """Adds a document to the catalog and
        returns its id"""

    def remove(document):
        """Removes a document from the catalog"""

    def contains(document):
        """Does the catalog contain a document"""

class IView(Interface):
    """Defines viewing aspects of objects"""

class ICatalogView(IView):
    """Provides viewing capabilities for catalogs"""

    def listsizes():
        """Lists the content of a catalog"""

# ---------------------------------------------------------

# [Entity]

@implementer(ICatalog)
class Catalog(object):
    """This class implements an emulator of a ICatalog"""

    @property
    def documents(self):
        return self.__documents__

    def __init__(self):
        self.__documents__=set()

    def add(self, document):
        self.documents.add(document)

    def remove(self, document):
        self.documents.remove(document)

    def contains(self, document):
        return document in self.documents

#  --------------- Tests -----------------

@implementer(ICatalogView)
class TextCatalogView(object):
    def __init__(self, catalog):  # TODO: rename as `context`
        self.catalog=catalog

    def listsizes(self):
        print("Sizes of the documents:")
        for o in self.catalog.documents:
            size=ISize(o).getsize()
            print(size)


@implementer(IFile)
class FileObect(object):
    def __init__(self, body=""):
        self.body=body

#@implementer(ISize)
# @adapter(IFile)
class AdapterOfIFileToISize(object):
    def __init__(self, context):  # context = an instance of IFile implementer
        self.context=context

    def getsize(self):
        return len(self.context.body)


GSM=getGlobalSiteManager()
# help(GSM)
GSM.registerAdapter(AdapterOfIFileToISize,[IFile],ISize,"")

class TestCatalog:
    def setUp(self):
        self.cat=Catalog()

    def tearDown(self):
        del self.cat

    def test_test(self):
        return True

    def test_ICatalog_provides(self):
        """a Constraint test"""
        assert ICatalog.providedBy(self.cat)

    def test_lifeSpanOfDocumentInsideCatalog(self):
        c=self.cat
        o=object()

        assert len(list(c.documents))==0
        c.add(o)
        assert len(list(c.documents))==1
        assert c.contains(o)
        c.remove(o)
        assert len(list(c.documents))==0

    def test_lifeSpanOfFileObjectInsideCatalog(self):
        c=self.cat
        f=FileObect("test")

        IFile.providedBy(f)

        assert len(list(c.documents))==0
        c.add(f)
        assert len(list(c.documents))==1
        assert c.contains(f)
        c.remove(f)
        assert len(list(c.documents))==0

    def test_TextCatalogSizesList(self):
        c=self.cat
        f1=FileObect("1")
        f2=FileObect("22")

        for f in [f1,f2]:
            c.add(f)

        v=TextCatalogView(c)
        ICatalogView.providedBy(v)

        v.listsizes()
