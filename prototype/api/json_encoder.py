from safrs import SAFRSJSONEncoder
# FIXME Achim    from database.models.types.choice_ext import Choice as ChoiceExt
from sqlalchemy_utils.types.choice import Choice


class SAFRSJSONEncoderExt(SAFRSJSONEncoder):
    """
        Quick example on adding additional types via CustomEncoder

        see also https://gist.github.com/KodeKracker/b44dea8df6c0c90fdcdb
        https://github.com/thomaxxl/safrs/blob/master/examples/demo_geoalchemy.py
    """

    def default(self, obj, **kwargs):
        """ FIXME Achim
        if isinstance(obj, ChoiceExt):
            return obj.code
        """
        if isinstance(obj, Choice):
            return obj.code

        return super().default(obj, **kwargs)
