
class Interface(object):
    """
    Dummy class that serves as a interface that all Sketches and Bloom Filters must implement
    """
    def __init__(self):
        super(Interface, self).__init__()

    def add(self, item):
        raise NotImplementedError("Method is not implemented for class" + str(type(self))[17:-2])

    def get_number_estimate(self):
        raise NotImplementedError("Method is not implemented for class" + str(type(self))[17:-2])

    def join(self, *args):
        raise NotImplementedError("Method is not implemented for class" + str(type(self))[17:-2])

    def get_name(self):
        raise NotImplementedError("Method is not implemented for class" + str(type(self))[17:-2])

    def __sizeof__(self):
        raise NotImplementedError("Method is not implemented for class" + str(type(self))[17:-2])