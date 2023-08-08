[
    {
    "name": "{name}_GRP", # "name": "{name}:{name}"_GRP"  <= allGrp
    "attrs": self.hiLockedTransformAttrs,
    "type":"transform"
    },
    {
    "name":"{name}",
    "attrs": self.hiLockedTransformAttrs,
    "type":"transform",
    "parent":"{name}:{name}_GRP"
    },
    {
    "name": "{geometris}", # ns+"geometry_GRP" <= geoGrp
    "patterns": ["{name}:Geometries"],
    "attrs": self.hiLockedTransformAttrs,
    "parent": "{name}:{name}_GRP",
    "type":"transform"
    },
    {
    "name": "TKRig", # ns + ns[:-1] <= rigGrp
    "attrs": self.hiLockedTransformAttrs,
    "parent": "{name}:{name}",
    "type":"transform"
    },
    {
    "name": "setRoot",
    "type": "objectSet",
    },
    {
    "name": "{geoSetName}",
    "type": "objectSet",
    "groups":["{name}:setRoot"]
    },
    {
    "name": "{ctrlSetName}",
    "type": "objectSet",
    "groups":["{name}:setRoot"],
    "patterns":["{name}:ctrls_set"]
    }
]