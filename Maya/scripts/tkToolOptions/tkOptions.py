"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Cyril GIBAUD - Toonkit
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

import json
import os
import collections
import ordereddict

__author__ = "Cyril GIBAUD - Toonkit"

DEFAULT_DESC = "No description"

class Option(object):
    """
    Base class for simple option, with a name, description and default value
    """
    def __init__(self, inName, inValue, inDescription=DEFAULT_DESC, inNiceName=None, inOptional=False):
        self.name = inName
        self.niceName = inName if inNiceName is None else inNiceName
        self.defaultValue = inValue
        self.description = inDescription
        self.optional = inOptional
        self._type = None

    @property
    def type(self):
        if self._type is None:
            self._type = type(self.defaultValue).__name__

        return self._type

class Options(object):
    """
    Base class for simple options, encapsulating a dictionary (or an object instance in future versions) handling json serialization
    """
    
    def __init__(self, inData=None, inPath=None, inOptions=None):
        self.__options = inOptions

        self.__data = inData
        self.__path = inPath

        if self.__data is None:
            if self.__path is None or not self.load():
                self.__data = Options.OrderedDict()

        if self.options is None:
            for key, value in self.__data.iteritems():
                self.addOption(key, value)

    """
    brackets overload
    """
    def __getitem__(self, key):
        return None if not key in self.__data else self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, self.__data.items())

    def iteritems(self):
        return self.__data.iteritems()

    def __len__(self):
        return len(self.__data)
    """
    data property
    """
    @property
    def data(self):
        return Options.encode_obj(self.__data)

    @data.setter
    def data(self, value):
        self.__data = value

    """
    path property to ease the save/load process
    """
    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value

    @property
    def options(self):
        return self.__options

    @staticmethod
    def OrderedDict():
        orddict = None
        try:
            orddict = collections.OrderedDict()
        except:
            orddict = ordereddict.OrderedDict()

        return orddict

    @staticmethod
    def encode_obj(obj):
        if type(obj).__name__ =='instance':
            return obj.__dict__ 
        return obj

    @staticmethod
    def serialize(obj):
        return json.dumps(obj, default=Options.encode_obj, indent=2)

    @staticmethod
    def deserialize(strObj):
        jsonObj = json.loads(strObj)
        return jsonObj

    def addOption(self, inName, inValue, inDescription=DEFAULT_DESC, inNiceName=None, inOptional=False):
        if self.__options is None:
            self.__options = []

        self.__options.append(Option(inName, inValue, inDescription, inNiceName, inOptional))
        if not inName in self.__data:
            self.__data[inName] = inValue

    def keys(self):
        return self.data.keys()

    def __str__(self):
        return str(self.data)

    def save(self, inPath=None):
        isString = isinstance(inPath, basestring)
        if inPath is None:
            inPath = self.__path
            isString = True
        elif isString:
            self.__path = inPath

        try:           
            if isString:
                dirname = os.path.dirname(inPath)
                if not os.path.exists(dirname):
                    try:
                        os.makedirs(dirname)
                    except OSError as exc: # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise

                with open(inPath, 'w') as content_file:
                    content_file.write(Options.serialize(self.__data))
            else:#Asssume it's a file-like object
                try:
                    inPath.write(Options.serialize(self.__data))
                finally:
                    inPath.close()
                    raise
        except Exception, e:
            print "Error saving options : {0}".format(e)
            return False

        return True

    def load(self, inPath=None):
        isString = isinstance(inPath, basestring)
        if inPath is None:
            inPath = self.__path
            isString = True
        elif isString:
            self.__path = inPath

        readdata = None

        try:
            if isString:
                with open(inPath, 'r') as content_file:
                    readdata = content_file.read()
                    self.__data = Options.deserialize(readdata)
            else:#Asssume it's a file-like object
                try:
                    readdata = inPath.read()
                    self.__data = Options.deserialize(readdata)
                finally:
                    inPath.close()

            assert self.__data is not None, "Can't load data from {0}".format(inPath)
        except Exception, e:
            print "Error loading options : {0}".format(e)
            return False

        return True
