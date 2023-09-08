# Copyright (c) 2012-2013 Guillaume Barlier
# This file is part of "anim_picker" and covered by the LGPLv3 or later,
# read COPYING and COPYING.LESSER for details.

from maya import OpenMayaUI
import sys
if sys.version_info.major  > 2:
    long = int

# Main Qt support
try:
    from qtpy import QtCore, QtGui, QtOpenGL, QtWidgets
except:
    try:
        from anim_picker.Qt import QtCore, QtGui, QtOpenGL, QtWidgets
    except:
        raise Exception('Failed to import Qt.py and qtpy.py')

try:
    import sip
except:
    pass

try:
    import shiboken
except:
    try:
        from PySide import shiboken
    except:
        try:
            import shiboken2 as shiboken
        except:
            raise Exception('Failed to import sip or shiboken')
        
    
# Instance handling
def wrap_instance(ptr, base):
    '''Return QtGui object instance based on pointer address
    '''
    if 'sip' in globals():
        try:
            uiObj = sip.wrapinstance(long(ptr), QtCore.QObject)
            if not uiObj is None:
                return uiObj
        except:
            pass

    if 'shiboken' in globals():
        return shiboken.wrapInstance(long(ptr), base)
    
def unwrap_instance(qt_object):
    '''Return pointer address for qt class instance
    '''
    if 'sip' in globals():
        try:
            ptr = sip.unwrapinstance(qt_object)
            if not ptr is None:
                return long(ptr)
        except:
            pass

    if 'shiboken' in globals():
        return long(shiboken.getCppPointer(qt_object)[0])

    return None
    
    
def get_maya_window():
    '''Get the maya main window as a QMainWindow instance
    '''
    try:
        ptr = OpenMayaUI.MQtUtil.mainWindow()
        return wrap_instance(long(ptr), QtWidgets.QMainWindow)
    except:
        #    fails at import on maya launch since ui isn't up yet
        return None