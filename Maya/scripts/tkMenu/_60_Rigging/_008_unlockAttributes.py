import pymel.core as pc

ATTRS = ["t{AXIS}", "r{AXIS}", "s{AXIS}", "v"]

VARIABLES = {
    "AXIS":["x", "y", "z"]
}

def lockAttrs(inObj, inLock=True):
    for attr in ATTRS:
        attrs = []
        
        isVar = False
        for variable, values in VARIABLES.iteritems():
            if variable in attr:
                isVar = True
                for value in values:
                    attrs.append(attr.format(**{variable:value}))
        
        if not isVar:
            attrs.append(attr)

        for subAttr in attrs:
            inObj.attr(subAttr).setLocked(inLock)

def lockAttrsSelected(inLock=True):
    for selObj in pc.selected():
        lockAttrs(selObj, inLock)
        
lockAttrsSelected(False)