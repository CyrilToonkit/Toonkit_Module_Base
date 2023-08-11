from Toonkit_Core import tkLogger, tkCore
from Toonkit_Core.tkProjects import tkContext
import tkMayaCore as tkc
from maya import cmds
try:
    import winsound
except:
    winsound=None
    tkLogger.debug("Unable to import winsound library.")


try:basestring
except:basestring = str

class mayaGeter():
    name = "maya"
    @tkCore.verbosed
    def detect_context(self, inVariable, inPattern, inContext = None):
        inContext = inContext or {}
        context = inContext.copy()
        if "name" in inVariable:
            assetName = self.getNameSpace()
            if not assetName is None:
                context["name"] = assetName
        detectedTemplate = self.detect_template()
        context.update(detectedTemplate)
        return context

    def detect_template(self):
        project = tkCore.getProject("maya")
        inTemplatesSpecs = project.templatesSpecs
        baseTemplate = project.assetTypeToSpec
        namespace = "::"
        weight = {}
        for key, value in inTemplatesSpecs.items():
            for ctrl, weightFactor in value:
                if isinstance(ctrl, basestring):
                    if cmds.ls(namespace + ctrl):
                        if not key in weight.keys():
                            weight[key] = weightFactor
                        else:
                            weight[key] += weightFactor
                elif isinstance(ctrl, dict):
                    if cmds.ls(**ctrl):
                        if not key in weight.keys():
                            weight[key] = weightFactor
                        else:
                            weight[key] += weightFactor

        sortedKeys = [(x, weight[x]) for x in sorted(weight, key=weight.get, reverse=True)]
        if not len(sortedKeys) == 0:
            if "Bird" in weight and not ("Quadriped" in weight or "Biped" in weight) and "Props" in weight:
                sortedKeys.pop(0)
            for x in sortedKeys:
                templateType = x[0]
                break
        else:
            templateType = None
        for key, value in baseTemplate.items():
            if templateType in value:
                tkLogger.info("Data get: 'assetType' = {0}, 'assetSpec' = {1}".format(key, templateType))
                return {"assetType":key, "assetSpec": templateType}
        return {}

        # if len(sortedKeys) == 1 and weight[sortedKeys[0]] < 1:
        #     cmds.warning("Less than one discriminent argument found on tamplate '{0}'. Props template used !".format(sortedKeys[0]))
        #     return "Props"
        # elif len(sortedKeys) > 1 and weight[sortedKeys[0]] < 1:
        #     cmds.warning("More than one template match with your asset and with an unconfident value to discriminate which one have to be used, Props Tamplate used !")
        #     return "Props"
        # elif weight.values().count(sortedKeys[0]) > 1:
        #     cmds.warning("More than one tamplate match with your asset, first one selected : {0} ".format("".join(sortedKeys)))

    def getSceneName(self):
        sceneName = cmds.file(q=True, sceneName=True).replace("/", "\\")
        if sceneName == "":
            sceneName = None
        return sceneName

    @tkCore.verbosed
    def getNameSpace(self):
        sceneNodes = [x for x in cmds.ls(assemblies=True) if x != "" and ":" in x]
        if len(sceneNodes) > 0:
            rootNode = sceneNodes[0]
            return rootNode.split(":")[-1]
        return None

    def syncDCCProject(self):
        tkc.TOOL.options["project"] = tkCore.PROJECT.name
        if cmds.control(tkc.TOOL.getWindowName(), q=True, exists=True):
            tkc.TOOL.setOptionItem(tkc.TOOL.options.getOption("project"))
    
    def checkSyncProject(self):
        project = tkCore.PROJECT
        try:
            import tkOscar
            oscarProjectName = tkOscar.getOscarProject()
            mayaProjectName = tkCore.PROJECT.name
            
            if not oscarProjectName == mayaProjectName:
                if not winsound is None:
                    winsound.PlaySound("SystemExist", winsound.SND_ASYNC | winsound.SND_ALIAS)
                message = "The OSCAR and Maya projects are different :\n - OSCAR Project   :   {}\n - Maya Project      :   {}\nWhat do you want to do ?".format(oscarProjectName, mayaProjectName)
                anser = cmds.confirmDialog( title='Project Mismatch', message=message, button=['Continue','Change Maya Project','Cancel'], defaultButton='Contiune', cancelButton='Cancel', dismissString='Cancel' )
                if anser == "Cancel":
                    raise Exception("Conform cancelled by user (project mismatch)")
                elif anser == "Change Maya Project":
                    project = tkCore.setProject("maya", oscarProjectName)
                elif anser == "Contrinue":
                    project = tkCore.PROJECT
            return project
        except:
            tkLogger.warning("Can't find anything to sync your project with.")
            return project