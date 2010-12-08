=================
py-JSON-validator
=================

This JSON validator enforces a lightweight schema for JSON serializations.  When an API receives JSON data from a client, it needs to meet a number of constraints before it's considered useful.  Checking each value in the JSON explicitly is prone to errors and code duplication, and is tedious.  The goal of this tool is to provide a way to validate JSON against a schema, but to be at least an order of magnitude simpler than `DTD <http://en.wikipedia.org/wiki/Document_Type_Definition>`_ =]

Try some examples!

Examples
========

Dictionary with a required key 'one', which must be a string::

	>>> schema = { 'one' : (bool, ) }
	>>> json_data = { 'one' : True }
	>>> validate_json(json.dumps(json_data), schema)
	True

	>>> json_data = { 'one' : 8 }
	>>> validate_json(json.dumps(json_data), schema)
	jsonvalidator.ValidationError: Value '8' is not of type bool	

	>>> json_data = json.dumps({})
	>>> validate_json(json_data, schema)
	jsonvalidator.ValidationError: Required key 'one' not found


The key 'one' can be optional::
	
	>>> schema = { 'one?' : (bool, ) }
	>>> validate_json(json.dumps(json_data), schema)
	True

and it can map to other types, like a list::

	>>> schema = { 'one' : [ (int, ) ] }
	>>> json_data = { 'one' : [1, 2, 3] }
	>>> validate_json(json.dumps(json_data), schema)
	True

	>>> json_data = { 'one' : ['one', 2, 3] }
	>>> validate_json(json.dumps(json_data), schema)
	jsonvalidator.ValidationError: Value 'one' is not of type int

The key 'one' can also map to another dictionary::

	>>> schema = { 'one' : { 'two' : (int, ) } }
	>>> json_data = { 'one' : { 'two' : 3 } }
	>>> validate_json(json.dumps(json_data), schema)
	True

Finally, additional checks on values can be done with validator functions.  Two functions, 'rexp' and 'enum', are provided::

	>>> schema = { 'one' : (basestring, rexp(r'.+@.+\..+')) }
	>>> json_data = { 'one' : 'not_an_email_address' }
	>>> validate_json(json.dumps(json_data), schema)
	jsonvalidator.ValidationError: String 'not_an_email_address' does not match the format .+@.+\..+

	>>> schema = { 'one' : (basestring, enum('two', 'three')) }
	>>> json_data = { 'one' : 'not_two_or_three' }
	>>> validate_json(json.dumps(json_data), schema)
	jsonvalidator.ValidationError: Value 'not_two_or_three' must be one of (two,three)
		
See the tests if you want examples of how to write your own validator functions, and how you can chain them together.


Syntax
======

A full explanation of syntax will be put here whenever I have the motivation to do more documentation.  I'll add some notes here that aren't covered in the examples:
	- Lists must be homogenous; the same validation will be applied to every element of the list.
	- By default, lists are not allowed to be empty.  Add 'None' as the last parameter of the [] part of the schema if you allow empty lists.
	- This version only supports dictionaries at the root level (hopefully explaining why all the examples were "{ 'one' : ____ }".  The API this was geing designed for didn't require any non-dictionary types, but I hope to add this soon.  
