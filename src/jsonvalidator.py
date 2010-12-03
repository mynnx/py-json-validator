import re
import json

class ValidationError(Exception):
    pass

def rexp(expr):
    '''
    Takes a regular expression and returns a function that validates its 
    argument against that expression.  
    Raises a ValidationError if the argument does not match the expression.
    '''
    def match(value):
        if not re.match(expr, value):
            raise ValidationError('String %s does not match the format %s' 
                % (value, expr))
    return match

def enum(*values):
    '''
    Takes a list of values and returns a function that checks whether or not
    its argument is in that list of values.  
    Raises a ValidationError if the argument is not in the list.
    '''
    def inEnum(value):
        if value not in values:
            valuesStr = ','.join([str(v) for v in values])
            raise ValidationError('Value %s must be one of (%s)' 
                % (value, valuesStr))
    return inEnum

def _checkType(value, type):
    '''
    Raises a ValidationError if value is not an instance of the provided type.
    '''
    if not isinstance(value, type):
        raise ValidationError('Value %s is not of type %s' 
            % (value, type.__name__))

def _validateValue(value, schema):
    '''
    Applies the schema (type, validatorFunc, validatorFunc, ...) to value.
    '''
    _checkType(value, schema[0])
    if len(schema) > 0:
        for validator in schema[1:]:
            if validator is not None:
                validator(value)

def validate_json(json_data, schema):
    try:
        data = json.loads(json_data)
    except ValueError, exc:
        raise ValidationError('Could not parse JSON: %s' % exc)
    validate(data, schema)
        
def validate(data, schema):
    '''
    Apply each schema (each sKey, sValue in schema) to the corresponding 
    element in data.  
         - sKeys not present in the given data are ignored.
         - sKeys ending in '?' means that they are optional, 
           but are validated if present in data.
         - sValues are of the form (type, validator, validator, ...)
         - sValues representing a list are of the form:
            [(type, validator, validator, ...), None]
            where the optional None means that the list may be empty.
            - Lists may only contain homogenous, simple-value entries.
                This is a limitation and will be addressed in a later release.
    '''
    for (k, v) in schema.iteritems():
        required = False if k[-1] == '?' else True
        dataK = k if required else k[:-1]
        if required and dataK not in data:
            raise ValidationError('Required key %s not found' % k)
        elif dataK not in data:
            continue

        if isinstance(v, dict):
            _checkType(data[dataK], dict)
            validate(data[dataK], schema[k])
        elif isinstance(v, list):
            _checkType(data[dataK], list)
            allowEmpty = True if v[-1] is None else False
            
            if not allowEmpty and len(data[dataK]) == 0:
                raise ValidationError('List named %s may not be empty' % k)
            map(lambda value: _validateValue(value, schema[k][0]), data[dataK])
        elif isinstance(v, tuple):
            _validateValue(data[dataK], schema[k])

# vim:et:fdm=indent:fdn=1
