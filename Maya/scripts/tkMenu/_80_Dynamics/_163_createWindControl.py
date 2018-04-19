import pymel.core as pc
import tkMayaCore as tkc
import tkNodeling as tkn

WINDCTRL_NAME = "Wind_ctrl"
WINDCTRL_ROOT = WINDCTRL_NAME + "_root"
WINDCTRL_SENSOR = WINDCTRL_NAME + "_sensor"
WINDCTRL_SOURCE = WINDCTRL_NAME + "_source"

def createWindControl():
    windRoot = None
    windControl = None
    
    if not pc.objExists(WINDCTRL_ROOT):
        #Create root
        windRoot = pc.group(name=WINDCTRL_ROOT, empty=True, world=True)

        pc.setAttr(windRoot.t, lock=True, keyable=False, channelBox=False)
        pc.setAttr(windRoot.r, lock=True, keyable=False, channelBox=False)
        pc.setAttr(windRoot.s, lock=True, keyable=False, channelBox=False)
        
        #Create control
        points=[(0, 0, 0)]
        points.append((5, 0, 0))
        points.append((4, .5, 0))
        points.append((4, 0, .5))
        points.append((5, 0, 0))
        points.append((4, .5, 0))
        points.append((4, 0, -.5))
        points.append((5, 0, 0))
        points.append((4, 0, -.5))
        points.append((4, -.5, 0))
        points.append((5, 0, 0))
        points.append((4, 0, .5))
        points.append((4, -.5, 0))

        windControl = pc.curve(d=1,p=points, name=WINDCTRL_NAME)
        tkc.setObjectColor(windControl,(255, 200, 0, 200))

        windRoot.addChild(windControl)
        
        windSensor = pc.group(name=WINDCTRL_SENSOR, empty=True, world=True)
        
        windSource = pc.group(name=WINDCTRL_SOURCE, empty=True, world=True)
        windRoot.addChild(windSource)
        tkc.constrain(windSource, windControl, "point")

        windSource.addChild(windSensor)
        windSensor.t.set([5,0,0])
        tkc.constrain(windSensor, windControl)
        
        #Controller params
        tkc.addParameter(windControl, name="categ", inType="enum;WIND", default=1, min=0, max = 100, nicename="-------------------- ", expose=True, readOnly=True, keyable=False)
        
        tkc.addParameter(windControl, name="Amplitude", inType="double", default=1, min=0, max = 100)
        tkc.addParameter(windControl, name="Turbulence_Amplitude", inType="double", default=1, min=0, max = 100)
        tkc.addParameter(windControl, name="Turbulence_Frequency", inType="double", default=1, min=0, max = 100)
        
        #Results params
        tkc.addParameter(windRoot, name="Wind_X", inType="double", default=0)
        div = tkn.div(windSensor.tx, 5.0)
        div >> windRoot.Wind_X
        
        tkc.addParameter(windRoot, name="Wind_Y", inType="double", default=0)
        div = tkn.div(windSensor.ty, 5.0)
        div >> windRoot.Wind_Y
        
        tkc.addParameter(windRoot, name="Wind_Z", inType="double", default=0)
        div = tkn.div(windSensor.tz, 5.0)
        div >> windRoot.Wind_Z
    else:
        windRoot = pc.PyNode(WINDCTRL_ROOT)
        windControl = pc.PyNode(WINDCTRL_NAME)
        
    #Reconnect
    winds = pc.ls(["*:TK_Wind_Global_Params_Root_RigParameters", "TK_Wind_Global_Params_Root_RigParameters"])
    for wind in winds:
        realAttr = tkc.getRealAttr("{0}.{1}".format(wind, "Wind_Global_Params_Wind_Amplitude"))
        if realAttr != None and realAttr != windControl.Amplitude.name():
            pc.connectAttr(windControl.Amplitude, realAttr)

        realAttr = tkc.getRealAttr("{0}.{1}".format(wind, "Wind_Global_Params_Turbulence_Amplitude"))
        if realAttr != None and realAttr != windControl.Turbulence_Amplitude.name():
            pc.connectAttr(windControl.Turbulence_Amplitude, realAttr)
        
        realAttr = tkc.getRealAttr("{0}.{1}".format(wind, "Wind_Global_Params_Turbulence_Frequency"))
        if realAttr != None and realAttr != windControl.Turbulence_Frequency.name():
            pc.connectAttr(windControl.Turbulence_Frequency, realAttr)
        
        realAttr = tkc.getRealAttr("{0}.{1}".format(wind, "Wind_Global_Params_Wind_X"))
        if realAttr != None and realAttr != windRoot.Wind_X.name() and not "constraintTranslate" in realAttr:
            pc.connectAttr(windRoot.Wind_X, realAttr)
        
        realAttr = tkc.getRealAttr("{0}.{1}".format(wind, "Wind_Global_Params_Wind_Y"))

        if realAttr != None and realAttr != windRoot.Wind_Y.name() and not "constraintTranslate" in realAttr:
            pc.connectAttr(windRoot.Wind_Y, realAttr)
            
        realAttr = tkc.getRealAttr("{0}.{1}".format(wind, "Wind_Global_Params_Wind_Z"))
        if realAttr != None and realAttr != windRoot.Wind_Z.name() and not "constraintTranslate" in realAttr:
            pc.connectAttr(windRoot.Wind_Z, realAttr)

    return windControl

pc.select(createWindControl())