"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Authors : Cyril GIBAUD - Toonkit, Stephane Bonnot - Parallel Dev
    Copyright (C) 2014-2017 Toonkit
    http://toonkit-studio.com/

    Toonkit Module Lite is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Toonkit Module Lite is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Toonkit Module Lite.  If not, see <http://www.gnu.org/licenses/>
-------------------------------------------------------------------------------
"""

__author__ = "Cyril GIBAUD - Toonkit, Stephane Bonnot - Parallel Dev"

#Methods to convert generic to and from string for oscar zmq layer 

# methods to convert string to data

splitcharacter = '#';
subsplitcharacter = '~';
subsubsplitcharacter = ',';
subsubsubsplitcharacter = ';';


keyseparator = '$SHARP_Separator$';
keysubseparator = '$TILDE_SubSeparator$';
keysubsubSeparator = '$COMMA_SubSubSeparator$';
keysubsubsubSeparator = '$SEMICOLON_SubSubSeparator$';

def encodestring(inString):
	if inString == None:
		return ""
	return inString.replace(splitcharacter, keyseparator).replace(subsplitcharacter, keysubseparator).replace(subsubsplitcharacter, keysubsubSeparator)

def decodestring(inString):
	if inString == None:
		return ""
	return inString.replace(keyseparator, splitcharacter).replace(keysubseparator, subsplitcharacter).replace(keysubsubSeparator, subsubsplitcharacter)

def objecttostring(obj):
	if isinstance(obj, float):
		return "float" + subsplitcharacter + floattostring(obj)
	elif isinstance(obj, bool):
		return "bool" + subsplitcharacter + booltostring(obj)
	elif isinstance(obj, int):
		return "int" + subsplitcharacter + inttostring(obj)
	elif isinstance(obj, tuple):
		return "color" + subsplitcharacter + colortostring(obj)
	elif obj is None:
		return "null" + subsplitcharacter + "Null"

	return "string" + subsplitcharacter + str(obj)

def stringtoobject(strobj):
	value = None
	type_value = strobj.split(subsplitcharacter)

	if type_value[0] == "float" or type_value[0] == "double":
		value = stringtofloat(type_value[1])
	elif type_value[0] == "bool":
		value = stringtobool(type_value[1])
	elif type_value[0] == "int":
		value = stringtoint(type_value[1])
	elif type_value[0] == "color":
		value = stringtocolor(type_value[1])
	elif type_value[0] == "null":
		value = None
	else:
		value = str(type_value[1])

	return value

def stringtolistobject(st):
	spl = st.split(subsubsplitcharacter)
	while "" in spl:
		spl.remove("")

	return [stringtoobject(strObj) for strObj in spl]
	
def listobjecttostring(lst):
	'''
	strNames = ""

	for obj in lst:
		if len(strNames) != 0:
			strNames = strNames + subsubsplitcharacter + objecttostring(obj)
		else:
			strNames = objecttostring(obj)
	'''
	return subsubsplitcharacter.join([objecttostring(obj) for obj in lst])

def stringtobool(bs):
	return (bs == '1' or bs == 'True')

def booltostring(b):
	if (b):
		return "True"
	return "False"

def stringtoint(istr):
	return int(istr)

def inttostring(i):
	return str(i)

def stringtofloat(fs):
	return float(fs)

def floattostring(f):
	return str(f)

def vec3tostring(vec3):
	ret = floattostring(vec3[0])+subsubsplitcharacter+floattostring(vec3[1])+subsubsplitcharacter + floattostring(vec3[2])
	return ret

def stringtovec3(st):
	spl = st.split(subsubsplitcharacter)
	ret = (stringtofloat(spl[0]),stringtofloat(spl[1]),stringtofloat(spl[2]))
	return ret	

def stringtoliststring(st):
	spl = st.split(subsubsplitcharacter)
	while "" in spl:
		spl.remove("")
	return spl

def liststringtostring(lst):
	'''
	strNames = ""
	first = True
	for stringObj in lst:
		if not first:
			strNames = strNames + subsubsplitcharacter + stringObj
		else:
			first = False
			strNames = stringObj
	'''

	return subsubsplitcharacter.join(lst)

def stringtolistfloat(st):
	spl = st.split(subsubsplitcharacter)
	while "" in spl:
		spl.remove("")
	return [float(val) for val in spl]
	
def listfloattostring(lst):
	return subsubsplitcharacter.join([`num` for num in lst])
	'''
	strNames = ""
	first = True
	for stringObj in lst:
		if not first:
			strNames = strNames + subsubsplitcharacter + str(stringObj)
		else:
			first = False
			strNames = str(stringObj)

	return strNames
	'''

def stringtolistint(st):
	spl = st.split(subsubsplitcharacter)
	while "" in spl:
		spl.remove("")
	return [int(val) for val in spl]
	
def listinttostring(lst):
	return subsubsplitcharacter.join([`num` for num in lst])
	'''
	strNames = ""
	for stringObj in lst:
		if len(strNames) != 0:
			strNames = strNames + subsubsplitcharacter + str(stringObj)
		else:
			strNames = str(stringObj)

	return strNames
	'''

def stringtocolor(st):
	spl = st.split(subsubsplitcharacter)
	return (int(spl[0]),int(spl[1]),int(spl[2]),int(spl[3]))

def colortostring(color):
	strcol = ""
	strcol = str(color[0]) + subsubsplitcharacter
	strcol = strcol + str(color[1]) + subsubsplitcharacter
	strcol = strcol + str(color[2]) + subsubsplitcharacter
	strcol = strcol + str(color[3])
	return strcol

def stringtolisttuple(st):
	listtuple = []
	spl = st.split(subsplitcharacter)
	while "" in spl:
		spl.remove("")

	for strtuple in spl:
		lst = strtuple.split(subsubsplitcharacter)
		if len(lst) > 0:
			floatlst = []
			for strval in lst:
				floatlst.append(stringtofloat(strval))
			listtuple.append(tuple(floatlst))

	return listtuple

def listtupletostring(lst):
	strNames = ""
	first = True
	for tup in lst:
		subfirst = True
		strtup = ""
		for val in tup:
			if not subfirst:
				strtup = strtup + subsubsplitcharacter + floattostring(val)
			else:
				subfirst = False
				strtup = floattostring(val)
		if strtup != "":
			if not first:
				strNames = strNames + subsplitcharacter + strtup
			else:
				first = False
				strNames = strtup

	return strNames

def stringtodic(st):
	dictionary = {}
	spl = st.split(subsubsplitcharacter)
	while "" in spl:
		spl.remove("")

	for keyValueSplit in spl:
		key_value = keyValueSplit.split(subsplitcharacter)
		if key_value[0] != "":
			dictionary[key_value[0]] = decodestring(key_value[1])

	return dictionary

def dictostring(dic):
	keys = dic.keys()
	first = True
	strNames = ""
	for key in keys:
		if first:
			strNames += key + subsplitcharacter + encodestring(dic[key])
			first = False
		else:
			strNames += subsubsplitcharacter + key + subsplitcharacter + encodestring(dic[key])

	return strNames

def stringtoanim(st):
	spl = st.split(subsubsplitcharacter)
	while "" in spl:
		spl.remove("")

	#StaticValue, Pre-Infinity, Post-Infinity
	anim = [stringtoobject(spl.pop(0)), stringtoint(spl.pop(0)), stringtoint(spl.pop(0))]

	for timeValue in spl:
		time_value = timeValue.split(subsubsubsplitcharacter)
		anim.append((stringtofloat(time_value[0]), stringtoobject(time_value[1]),stringtofloat(time_value[2]), stringtoobject(time_value[3]),stringtofloat(time_value[4]), stringtoobject(time_value[5]), stringtoint(time_value[6]), stringtoint(time_value[6])))

	return anim

def animtostring(anim):
	#StaticValue, Pre-Infinity, Post-Infinity
	strAnim = "%s,%s,%s" % (objecttostring(anim.pop(0)), inttostring(anim.pop(0)), inttostring(anim.pop(0)))

	for key in anim:
		strAnim += subsubsplitcharacter + floattostring(key[0]) + subsubsubsplitcharacter + objecttostring(key[1]) + subsubsubsplitcharacter + floattostring(key[2]) + subsubsubsplitcharacter + objecttostring(key[3]) + subsubsubsplitcharacter + floattostring(key[4]) + subsubsubsplitcharacter + objecttostring(key[5]) + subsubsubsplitcharacter + inttostring(key[6])

	return strAnim