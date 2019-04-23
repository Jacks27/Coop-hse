""" validate.py """
class Validate:

    @classmethod
    def required(cls, data_fields=[], dataDict={}):
        notFound=[]

        if len(data_fields) > 0:
            notFound= [i for i in data_fields if i not in dataDict or len(str(dataDict[i])) < 1]
        print(notFound)
        if (len(notFound) > 0):
            res ="The following fields are required {}".format(', '.join(notFound))
            return cls.make_dict(False, res)
        else:
            return cls.make_dict(True)


    @classmethod
    def make_dict(cls, status, res=''):
        """ returns a dict  {resp: resp, status:status }"""
        return dict(res=res, status= status)
