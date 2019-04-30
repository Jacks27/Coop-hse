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
    id = None
    compiled_select = ""
   



    def __init__(self, *args, **kwargs):
        self.select_query = """SELECT * FROM {}""".format(self.table_name)
        self.where_clause = ''
        self.compiled_select = ""
        self.column_names = []
        self.clean_insert_dict()
        super().__init__()
    def get_record(self):
        """get a rows from the db table"""
    
        query = "SELECT * FROM {}".format(self.table_name)
        BaseModel.query_excute(query)
        result = self.cursor.fetchone()
        return result
    def select(self, fields=[]):
        """Builds the select part of the query
        Keyword Arguments:
            fields {str} -- [fields to select] (default: {"*"})
            fields {List} -- [fields to select])
        """
        if len(fields) > 0:
            formated_fields = ",".join(fields)
            self.select_query = """SELECT {} FROM {}""".format(
                formated_fields, self.table_name)
        else:
            self.select_query = """SELECT * FROM {}""".format(self.table_name)
        return self
    
    def insert_data(self, *args):
        
        list_vals = []
        for item in args:
            val = "'{}'".format(item)
            list_vals.append(val)
        values = ', '.join(list_vals)
        
        query ="""INSERT INTO {} ({}) VALUES({}) RETURNING {}"""\
            .format(self.table_name, ', '.join(self.tbl_colomns), \
                values,', '.join(self.sub_set_cols) )
        self.query_excute(query, True)
        try:
            
            result = self.cursor.fetchone()
            if result is not None:
                self.id = result[self.primary_key]
                self.add_result_to_self(result)


        except psycopg2.ProgrammingError as errorx:
            result=None
            self.errors.append(errorx)
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

    def where(self, where_dict, operator="AND"):
        """sets the where clause for select,delete and update queries
            Arguments:whereDict {[dict()]} -- [fieldname:value,
             fieldname !=: value,
             fieldname >=: value ]
        """
        special_chars = r'[><=!]'
        clause = ""
        if "WHERE" not in self.where_clause:
            clause = "WHERE"
        count = 0
        if bool(re.search(special_chars, self.where_clause)) is True:
            count = 2
        for key, value in where_dict.items():
            count += 1
            comparison = '='
            if bool(re.search(special_chars, key)) is True:
                comparison = ''
            if count == 1:
                clause += " {}{}'{}'".format(key, comparison, value)
            else:
                clause += " {} {}{}'{}'". format(operator,
                                                 key, comparison, value)
        self.where_clause += clause
        print('_____________________>',self.where_clause )
        return self.where_clause 

    def get(self, single=True,  number="all",):
        """Builds and executes the select querry
        """
        query = self.compile_select()
        self.query_excute(query)
        self.where_clause = ''
        if single is True:
            try:
                result = self.cursor.fetchone()
                if result is not None:
                    self.id = result[self.primary_key]
                    self.add_result_to_self(result)
            except psycopg2.ProgrammingError as errorx:
                result = None
                self.errors.append(errorx)
        elif type(number) == int:
            result = self.cursor.fetchmany(number)
        else:
            result = self.cursor.fetchall()
        return result

    def get_one(self, id):
        """Creates self variables with data from db  """
        self.where({self.primary_key: id})
        query = self.compile_select()
        self.query_excute(query)
        self.where_clause = ''
        try:
            result = self.cursor.fetchone()
            if result:
                self.id = result[self.primary_key]
                self.add_result_to_self(result)
        except psycopg2.ProgrammingError as errorx:
            result = None
            self.errors.append(errorx)
        return result


    def check_exist(self):

        """Check if a record exists
        Returns:
            [type] -- [description]
        """
        if self.where_clause != '' and self.get() is None:
            status = False
        else:
            status = True

        return status
    def compile_select(self):
        """compiles the select querry
        """
        if self.select_query:
            query = self.select_query
        else:
            query = self.select()
        if self.where_clause != '' and "WHERE" in self.where_clause:
            query += ' ' + self.where_clause
        self.compiled_select = query

        return self.compiled_select
        
    def add_result_to_self(self, result={}):
        """Adds a dictionary to self as a valiable
        Keyword Arguments:
            result {dict} -- [description] (default: {{}})
        """
        self.__dict__.update(result)

    def delete(self, id=None):
        """Deletes an item from the db

        Arguments:
            id {[type]} -- [description]
        """
        if id is None and self.where_clause == '':
            return False
        self.where({self.primary_key: id})
        query = "DELETE FROM {} ".format(self.table_name)
        query += self.where_clause
        self.query_excute(query, True)

    def sub_set(self, list_to_get=None):
        """gets a dictinary with the fields in the list_to_get
        Keyword Arguments:
            list_to_get {list} -- [description] (default: {[]})
        Returns: [dict] -- [subset of self]
        """
        if list_to_get is None:
            list_to_get = self.sub_set_cols
        list_to_get = [x.lower() for x in list_to_get]
        # convert all fields to lower case

        sub_set = dict.fromkeys(list_to_get, None)
        #  fields:None

        for key, value in self.__dict__.items():
            # displays class's namespace
            if key in list_to_get:

                sub_set[key] = value
        return sub_set
    def clean_insert_dict(self, dynamic_dict={}, full=True):
        """cleans a dictionaly according using table column names
        Keyword Arguments:
            dynamic_dict {dict} -- [description] (default: {{}})
        Returns: [dict] -- [with insertable colums]
        """
        query = "SELECT * FROM {} limit 1".format(self.table_name)
        self.query_excute(query)

        if self.cursor.description is not None:
            self.column_names = [row[0]for row in self.cursor.description]
        clean_dict = {}
        if len(self.column_names) == 0:
            return dynamic_dict
        if full is True:
            for col in self.column_names:
                clean_dict[col] = dynamic_dict.get(col, None)
        else:
            for key, value in dynamic_dict.items():
                key_l = key.lower()
                if key_l in self.column_names:
                    clean_dict[key] = value
        return clean_dict

    def update(self, update_dict, pry_key):
        """pursers update query
        Arguments: update_dict {[type]} -- [description]
        """
        set_part = ''
        data_len = len(update_dict)
        for key, value in update_dict.items():
            
            if data_len==1:
                set_part += " {}='{}'".format(key, value)
            else:
                set_part += " {}='{}',".format(key, value)
        self.where({self.primary_key: pry_key})
        query = "UPDATE {} SET {} ".format(self.table_name, set_part)
        query += self.where_clause
        query += " RETURNING {}".format(','.join(self.sub_set_cols))
        self.query_excute(query, True)
        try:
            result = self.cursor.fetchone()
            if result:
                self.id = result[self.primary_key]
                self.add_result_to_self(result)
        except psycopg2.ProgrammingError as errorx:
            result = None
            self.errors.append(errorx)
        self.where_clause = ''
        return result
