"""
 	Methods to convert Maya to and from string for oscar zmq layer 
 	Choosen Unit for angles is Degrees. See dteulerrotationtostring and stringtodteulerrotation
	Author : Stephane Bonnot - Parallel Dev
	Copyright : Toonkit Studio
"""
import OscarZmqString as ozs
from pymel.all import *
import pymel.core.datatypes as dt
import math

#Starting with Maya 2018 (maybe 2017) PyNode.getRotation sometimes return OpenMaya.EulerRotation !
def getPymelRotation(inNode, space="object"):
	r = inNode.getRotation(space=space)
	print "getPymelRotation",inNode
	if not isinstance(r, dt.EulerRotation):
		radToDeg = (180.0/math.pi)
		print " -not EulerRotation (",type(r),")", dt.EulerRotation(radToDeg*r.x, radToDeg*r.y, radToDeg*r.z)
		return dt.EulerRotation(radToDeg*r.x, radToDeg*r.y, radToDeg*r.z)

	print " -EulerRotation", r
	return r

def dtvec3tostring(vec3):
	ret = ozs.floattostring(vec3.x)+ozs.subsubsplitcharacter+ozs.floattostring(vec3.y)+ozs.subsubsplitcharacter + ozs.floattostring(vec3.z)
	return ret
def stringtodtvec3(st):
	spl = st.split(ozs.subsubsplitcharacter)
	ret = dt.Vector(ozs.stringtofloat(spl[0]),ozs.stringtofloat(spl[1]),ozs.stringtofloat(spl[2]))
	return ret	

def dteulerrotationtostring(vec3):
	ret = dtvec3tostring((180.0/math.pi)*vec3.asVector())
	return ret
def stringtodteulerrotation(st):
	spl = st.split(ozs.subsubsplitcharacter)
	ret = dt.EulerRotation([ozs.stringtofloat(spl[0]),ozs.stringtofloat(spl[1]),ozs.stringtofloat(spl[2])], unit='degrees')
	return ret	

def TRStostring(t,r,s):
	ret = dtvec3tostring(t)+ozs.subsplitcharacter+dteulerrotationtostring(r)+ozs.subsplitcharacter+ozs.vec3tostring(s)
	return ret
def stringtoTRS(st):
	spl = st.split(ozs.subsplitcharacter)
	t = stringtodtvec3(spl[0])
	r = stringtodteulerrotation(spl[1])
	s = ozs.stringtovec3(spl[2])
	return (t,r,s)

def inttointerpolation(intinterpolation):
	if intinterpolation == 0:
		return "linear"

	return "spline"

def interpolationtoint(strinterpolation):
	if strinterpolation == "linear":
		return 0

	return 1

def inttoextrapolation(intextrapolation):
	if intextrapolation == 1:
		return "linear"
	elif intextrapolation == 2:
		return "cycle"
	elif intextrapolation == 3:
		return "cycleRelative"

	return "constant"

def extrapolationtoint(strextrapolation):
	if strextrapolation == "linear":
		return 1
	elif strextrapolation == "cycle":
		return 2
	elif strextrapolation == "cycleRelative":
		return 3

	return 0
