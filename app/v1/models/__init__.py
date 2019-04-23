#init model
import psycopg2
from app.v1.db_setup import SetUpDb
from collections import OrderedDict 
from flask import jsonify, abort, make_response
import re
db = SetUpDb()
def from_setter(msg):
    res =jsonify({'status':400, 'error':msg})
    return abort(make_response(res, 400))

def _make_setter(dcls):
	code = 'def __set__(self, instance, value):\n'
	for d in dcls.__mro__: #walk MRO and collect output of set_code()
		if 'set_code' in d.__dict__: #if true
			for line in d.set_code():# line in return function
	 			code += '	' + line + '\n' #append the lines to code 
	return code
def _make_init(fields):
    code = 'def __init__(self, %s):\n'%','.join(fields)#assign the fields to the place holders
    for name in fields: 
        code += '   self.%s = %s\n' %(name, name)# concantinate the intialided field to the generated code
    return code
class DescriptorMeta(type):

    """ descriptor meta class """
    def __init__(self, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        code= _make_setter(self)
        exec(code, globals(), clsdict)
        setattr(self, '__set__', clsdict['__set__'])

class Descriptor(metaclass = DescriptorMeta):
    """" holds del set and other methods """
    @staticmethod
    def set_code():
        return ['instance.__dict__[self.name]= value']


class Sized(Descriptor):
    """ validate size of the object """
    def __init__(self, *args, minlen, **kwargs):
        self.minlen=minlen
        super().__init__(*args, **kwargs)

    @staticmethod
    def set_code():
        return ['if len(value) < self.minlen:\n', \
            '    msg ="{} too small must be greater than{}".format(value, self.minlen)\n',
            '    from_setter(msg)']
class Typed(Descriptor): 
    """ validate object type
    Argument ty expected object
    """
    ty = object

    @staticmethod
    def set_code():
        return ['if not isinstance(value, self.ty):\n',\
            '    msg="{} must be a {}".format(value, self.ty)',
            '    from_setter(msg)']
    
class Pattern(Descriptor):
    """ checks object pattern  """
    def __init__(self, *args, pat, **kwargs):
        self.pat=pat
        super().__init__(*args, **kwargs)
        
    @staticmethod
    def set_code():
        return['if not re.match(self.pat, value):\n',\
            '    msg ="{} is invalid string".format(value)\n',
            '    from_setter(msg)']
class Integer(Typed):
    """class expect object to be int """
    ty=int

class String(Typed):
    """ class String expect object to be String """
    ty= str
class Strpatt(String, Pattern):
    """this class validate string object and and object partten"""
    pass
class SizedString(Sized, String):
    """this class validate string object and and object size"""
    pass
class SizedInteger(Integer, Sized):
    """this class validate int object and and object partten"""
    pass



class BaseModelMeta(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, clsname, bases, clsdict):
        fields=[key for key, value  in clsdict.items() if isinstance(value, Descriptor)]
        if fields:
            init_code=_make_init(fields)
            exec(init_code, globals(), clsdict)
        for name in fields:
            clsdict[name].name = name

        clsobj= super().__new__(cls, clsname, bases, clsdict)
        return clsobj

   
class BaseModel(metaclass=BaseModelMeta):
    """ 
    bassmodel that hold all the  function for the rest of the model
    class variables  db.connection , db.connection.cursor
    """
    tbl_colomns = []
    errors = []
    connection  = db.connection
    cursor = db.cursor
    table_name = None
    colomn_name = None
    primary_key = 'id'
    sub_set_cols = [primary_key]


    
               
    def get_record(self):
        """get a rows from the db table"""
    
        query = "SELECT * FROM {}".format(self.table_name)
        BaseModel.query_excute(query)
        result = self.cursor.fetchone()
        return result
    
    def insert_data(self, *args):
        
        list_vals = []
        for item in args:
            val = "'{}'".format(item)
            list_vals.append(val)
        values = ', '.join(list_vals)
        query ="""INSERT INTO {} ({}) VALUES({}) RETURNING {}"""\
            .format(self.table_name, ', '.join(self.tbl_colomns), \
                values,', '.join(self.sub_set_cols) )
        print(query)
        try:
            BaseModel.query_excute(query, True)
            result = self.cursor.fetchone()
            return result
        except psycopg2.ProgrammingError as errorx:
            self.errors.append(errorx)
            print(errorx)
    @classmethod
    def query_excute(cls, query, commit=False):
        try:

            cls.cursor.execute(query)
            if commit:
                cls.connection.commit()
        except psycopg2.Error as errorx:
               cls.errors.append(errorx)
   
    def check_fields(self, data_dict):
        
        fields =[val for val in self.tbl_colomns if val not in data_dict]
        if fields:
            msg ="The flowing following fields are missing{}".format(''.join(fields))
            from_setter(msg)

