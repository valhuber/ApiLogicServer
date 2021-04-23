from safrs import SAFRSJSONEncoder
from sqlalchemy_utils.types.choice import Choice


class SAFRSJSONEncoderExt(SAFRSJSONEncoder):
    """
        Quick example on adding additional types via CustomEncoder

        see also https://gist.github.com/KodeKracker/b44dea8df6c0c90fdcdb
        https://github.com/thomaxxl/safrs/blob/master/examples/demo_geoalchemy.py
    """

    def default(self, obj, **kwargs):
        if isinstance(obj, Choice):
            return obj.code

        return super().default(obj, **kwargs)
