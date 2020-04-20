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

Used to parse arbitrary expression and consider each "term" as a class that overrides all operators and can execute custom code when evaluated.

The base class "Term" is a kind of virtual class that can contain any value type (basically str, int or float), undestanding just numbers and doing nothing with strings
by default. It overrides all operators and let derived class implement operators functions for string values (add, radd, sub, rsub...see https://docs.python.org/2/library/operator.html)

Includes
---------
# Operators : +, -, *, /, **(=pow)
# Functions : abs, min, max, clamp, pow, sin, cos, modulo
# Conditions :
    if/else is managed, but treated as a method : firstTerm.cond(criterion, secondTerm, ifTrue, ifFalse),

    so cases like :

    if(a)       | if(a)
    {           | {
        a = b   |     a = b
    }           | }
    else        |
    {           |
        b = a   |
    }           |

    cannot be managed correctly because these cases cannot be converted to a function call 

Todo
---------
floor, ceil


Example usages
---------
import tkExpressions as tke
reload(tke)
Expr = tke.Expr

expr = "(1 + 2) * 3.1416 + TOTO"

print Expr().compile(expr)
"""
import math
import re
import logging
logging.basicConfig()
import sys

__author__ = "Cyril GIBAUD - Toonkit"

logger = logging.getLogger("tkExpressions")
logger.setLevel(logging.WARNING)


# Values
#################################################################################

EPSILON = sys.float_info.epsilon * 10
OMEGA = 1.0/EPSILON

EPSILON_NAME = "eps"
OMEGA_NAME = "omg"

EMPTY = ""

CONDITION_CRITERIA = ["Equal", "NEqual", "Greather", "GEqual", "Less", "LEqual"]
CONDITION_NICECRITERIA = ["==", "!=", ">", ">=", "<", "<="]

def verbosed(func):
    """
    verbose decorator
    """
    def wrapper(*args):
        verboseMsg = "{0} {1}{2}".format(args[0], func.__name__, (" " + ",".join([str(arg) for arg in args[1:]])) if len(args) > 1 else EMPTY)
        logger.debug(verboseMsg)
        return func(*args)

    return wrapper

class Term(object):

    def __init__(self, value=None):
        self.value = value

    #Operators overloads

    def __str__(self):
        return "{0} ({1}:{2})".format(self.value, self.__class__.__name__, type(self.value))

    def get(self):
        return self.value

    #Unary
    @verbosed
    def __invert__(self):
        if Expr.objectIsNumber(self.value):
            return self.__class__(not self.value)

        return self.__class__(self.reverse())

    @verbosed
    def __neg__(self):
        if Expr.objectIsNumber(self.value):
            return self.__class__(-self.value)

        return self.__class__(self.neg())

    @verbosed
    def __abs__(self):
        if Expr.objectIsNumber(self.value):
            return self.__class__(abs(self.value))

        return self.__class__(self.abs())

    #Binary

    #Comparison
    @verbosed
    def __eq__(self, other):
        return self.__class__(self.cond("==", other, self.__class__(1), self.__class__(0)))

    @verbosed
    def __ne__(self, other):
        return self.__class__(self.cond("!=", other, self.__class__(1), self.__class__(0)))

    @verbosed
    def __lt__(self, other):
        return self.__class__(self.cond("<", other, self.__class__(1), self.__class__(0)))

    @verbosed
    def __gt__(self, other):
        return self.__class__(self.cond(">", other, self.__class__(1), self.__class__(0)))

    @verbosed
    def __le__(self, other):
        return self.__class__(self.cond("<=", other, self.__class__(1), self.__class__(0)))

    @verbosed
    def __ge__(self, other):
        return self.__class__(self.cond(">=", other, self.__class__(1), self.__class__(0)))

    #Operations
    @verbosed
    def __add__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(self.value + other.value)

        return self.__class__(self.add(other))

    @verbosed
    def __radd__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(self.value + other.value)

        return self.__class__(self.radd(other))

    def radd(self, other):
        return other.add(self)

    @verbosed
    def __sub__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(self.value - other.value)

        return self.__class__(self.sub(other))

    @verbosed
    def __rsub__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(other.value - self.value)

        return self.__class__(self.rsub(other))

    def rsub(self, other):
        return self.sub(other, self)

    @verbosed
    def __mul__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(self.value * other.value)

        return self.__class__(self.mul(other))

    @verbosed
    def __rmul__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(self.value * other.value)

        return self.__class__(self.rmul(other))

    def rmul(self, other):
        return other.mul(self)

    @verbosed
    def __truediv__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(self.value / other.value)

        return self.__class__(self.div(other))

    @verbosed
    def __rtruediv__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(other.value / self.value)

        return self.__class__(self.rdiv(other))

    @verbosed
    def __div__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(self.value / other.value)

        return self.__class__(self.div(other))

    @verbosed
    def __rdiv__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(other.value / self.value)

        return self.__class__(self.rdiv(other))

    def rdiv(self, other):
        return other.div(self)

    @verbosed
    def __pow__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(self.value ** other.value)

        return self.__class__(self.pow(other))

    def rpow(self, other):
        return other.pow(self)

    @verbosed
    def __mod__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(self.value % other.value)

        return self.__class__(self.mod(other))

    @verbosed
    def __rmod__(self, other):
        if Expr.objectIsNumber(self.value) and Expr.objectIsNumber(other.value):
            return self.__class__(other.value % self.value)

        return self.__class__(self.rmod(other))

    def rmod(self, other):
        return other.mod(self)

    #Functions
    @staticmethod
    @verbosed
    def _reverse(this):
        if Expr.objectIsNumber(this.value):
            return this.__class__( 1.0 - this.value)

        return this.__class__(this.reverse())

    @staticmethod
    @verbosed
    def _cos(this):
        if Expr.objectIsNumber(this.value):
            return this.__class__( math.cos(this.value))

        return this.__class__(this.cos())

    @staticmethod
    @verbosed
    def _sin(this):
        if Expr.objectIsNumber(this.value):
            return this.__class__( math.sin(this.value))

        return this.__class__(this.sin())

    @staticmethod
    @verbosed
    def _clamp(otherMin, otherMax, this):
        if Expr.objectIsNumber(this.value) and Expr.objectIsNumber(otherMin.value) and Expr.objectIsNumber(otherMax.value):
            return this.__class__(min(max(this.value, otherMin.value), otherMax.value))

        return this.__class__(this.clamp(otherMin, otherMax))

    @staticmethod
    @verbosed
    def _min(this, otherMin):
        if Expr.objectIsNumber(this.value) and Expr.objectIsNumber(otherMin.value):
            return this.__class__(min(this.value, otherMin.value))

        return this.__class__(this.clamp(this.__class__(-OMEGA), otherMin))

    @staticmethod
    @verbosed
    def _max(this, otherMax):
        if Expr.objectIsNumber(this.value) and Expr.objectIsNumber(otherMax.value):
            return this.__class__(max(this.value, otherMax.value))

        return this.__class__(this.clamp(otherMax, this.__class__(OMEGA)))

    @staticmethod
    @verbosed
    def _cond(this, criterion, secondTerm, ifTrue, ifFalse):
        if isinstance(criterion, basestring):
            try:
                criterion = CONDITION_NICECRITERIA.index(criterion)
            except:
                raise ValueError("Criterion string '{0}' is not valid (available values : {1}) !".format(criterion, CONDITION_NICECRITERIA))

        if (Expr.objectIsNumber(this.value) and Expr.objectIsNumber(secondTerm.value)
            and Expr.objectIsNumber(ifTrue.value) and Expr.objectIsNumber(ifFalse.value)):
            return this.__class__(ifTrue.value if eval("{0} {1} {2}".format(this.value, CONDITION_NICECRITERIA[criterion], secondTerm.value)) else ifFalse.value)

        return this.__class__(this.cond(criterion, secondTerm, ifTrue , ifFalse))

    #To give some sense to this class, override these:

    #Unary
    def neg(self, other):
        return "-{0}".format(Expr.getWord(self.value))

    def abs(self, other):
        return "abs({0})".format(Expr.getWord(self.value))

    #Binary
    def add(self, other):
        return "{0} + {1}".format(Expr.getWord(self.value), Expr.getWord(other.value))

    def sub(self, other):
        return "{0} - {1}".format(Expr.getWord(self.value), Expr.getWord(other.value))

    def mul(self, other):
        return "{0} * {1}".format(Expr.getWord(self.value), Expr.getWord(other.value))

    def div(self, other):
        return "{0} / {1}".format(Expr.getWord(self.value), Expr.getWord(other.value))

    def pow(self, other):
        return "{0} ** {1}".format(Expr.getWord(self.value), Expr.getWord(other.value))

    def mod(self, other):
        return "{0} % {1}".format(Expr.getWord(self.value), Expr.getWord(other.value))

    #Functions
    def reverse(self):
        return "reverse({0})".format(Expr.getWord(self.value))

    def cos(self):
        return "cos({0})".format(Expr.getWord(self.value))

    def sin(self):
        return "sin({0})".format(Expr.getWord(self.value))

    def clamp(self, otherMin, otherMax):
        return "clamp({0}, {1}, {2})".format(Expr.getWord(self.value), Expr.getWord(otherMin.value), Expr.getWord(otherMax.value))

    def cond(self, criterion, secondTerm, ifTrue, ifFalse):
        return "cond({0} {1} {2}, {3}, {4})".format(Expr.getWord(self.value), CONDITION_NICECRITERIA[criterion],
         Expr.getWord(secondTerm.value), Expr.getWord(ifTrue.value), Expr.getWord(ifFalse.value))

class Expr(object):
    
    OPERATORS = ["(", ")", "+", "\\-", "*", "/", ",", ">", "<", "=", "!", "%", "~"]

    SPLITTER = re.compile("[ " + "".join(OPERATORS) + "]+")

    FUNCTIONS = ["abs", "pow"]
    TERMMETHODS = ["get"]

    #COND_RE = re.compile("cond\((\S+)\s*({0})\s*(\S+),\s*(\S+)\s*,\s*(\S+)\s*\)".format("|".join(CONDITION_NICECRITERIA)))
    COND_RE = re.compile("cond\(.*({0}).*\)".format("|".join(CONDITION_NICECRITERIA)))
    ISNUMBER = re.compile("^([0-9\.]+)$")

    WORDS = {
        ".":"Dot",
        ":":"DDot",
        "0":"Zero",
        "1":"One",
        "2":"Two",
        "3":"Three",
        "4":"Four",
        "5":"Five",
        "6":"Six",
        "7":"Seven",
        "8":"Eight",
        "9":"Nine"
    }

    def __init__(self, termClass=Term, termModule=None):
        self.termClass = termClass
        self.termModule = termModule
        self.CUSTOMFUNCTIONS = ["clamp", "reverse", "cond", "min", "max", "cos", "sin"]

    @staticmethod
    def getWord(inNumberString):
        if not isinstance(inNumberString, basestring):
            absed = abs(inNumberString)
            if absed <= EPSILON:
                return EPSILON_NAME
            elif absed >= OMEGA:
                return OMEGA_NAME if inNumberString > 0 else "minus"+OMEGA_NAME
            else:
                inNumberString = str(inNumberString)

        word = ""
        for char in inNumberString:
            word += Expr.WORDS.get(char, char)
        return word

    @staticmethod
    def objectIsNumber(inObj):
        return isinstance(inObj, (int, float))

    @staticmethod
    def stringIsNumber(inExpr):
        return not Expr.ISNUMBER.match(inExpr) is None

    @staticmethod
    def stringToNumber(inExpr):
        try:
            return int(inExpr)
        except:
            return float(inExpr)

    @staticmethod
    def getTerms(inExpr):
        return list(set([term for term in Expr.SPLITTER.split(inExpr) if not term == EMPTY and not term in Expr.OPERATORS]))

    def getTermClassName(self):
        return self.termClass.__name__ if self.termModule is None else "{0}.{1}".format(self.termModule.__name__, self.termClass.__name__)

    def compile(self, inExpr):
        logger.debug("compiling:{0}".format(inExpr))

        global_vars = globals()
        local_vars = {}

        terms = sorted(Expr.getTerms(inExpr), key=lambda x: len(x), reverse=True)
        #print "terms",terms
        logger.debug("terms:{0}".format(terms))

        for term in terms:
            if term in Expr.FUNCTIONS:#Native function, simply skip
                continue

            if term in self.CUSTOMFUNCTIONS:#Custom function, replace by staticmethod call
                logger.debug("custom function:{0}".format(term))

                if term == "cond":
                    matches = re.finditer(Expr.COND_RE, inExpr)
                    for matchNum, match in enumerate(matches):
                        logger.debug("condition :{0} ({1})".format(match.group(), ",".join(match.groups())))

                        condString = match.group()
                        condStringFormatted = condString.replace(match.groups()[0], ",'{0}',".format(match.groups()[0]))
                        inExpr = inExpr.replace(condString, condStringFormatted)

                inExpr = re.sub("(?<![\d\w]){0}(?![\d\w])".format(term), "{0}._{1}".format(self.getTermClassName(), term), inExpr)

                continue

            for termMethod in Expr.TERMMETHODS:
                if term.endswith(termMethod):#Term class method, rewrite term
                    logger.debug("term method:{0}".format(term))
                    term = ".".join([w for w in term.split(".")[:-1]])
                    break

            termWord = Expr.getWord(term)
            logger.debug("term:{0} => termWord:{1}".format(term, termWord))
            if Expr.stringIsNumber(term):
                local_vars[termWord] = self.termClass(Expr.stringToNumber(term))
            else:
                local_vars[termWord] = self.termClass(term)

            logger.debug("termValue:{0}".format(local_vars[termWord]))

            inExpr = re.sub("(?<![\d\w]){0}(?![\d\w])".format(term), termWord, inExpr)

        logger.debug("expr:{0}".format(inExpr))

        logger.debug("local_vars:{0}".format(local_vars))

        retval = None

        #try:
        context = {}

        code = "def anon(" + ','.join(local_vars.keys()) + "):\n    return (" + inExpr + ").value"

        if not self.termModule is None:
            global_vars[self.termModule.__name__] = self.termModule

        exec code in global_vars, context
        retval = context['anon'](*(local_vars.values()))
        """except:
            logger.error("An error occurred in Expr.eval:")
            logger.error("globals : {0}\n".format(global_vars))
            logger.error(str(sys.exc_info()) + "\n")
            logger.error("in this code:\n" + code + "\n")
        """
        return retval