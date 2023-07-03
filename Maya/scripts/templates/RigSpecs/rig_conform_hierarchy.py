[
    {
    "name": "{name}_GRP", # "name": "{name}:{name}"_GRP"  <= allGrp
    "attrs": "{attrs}",
    "patterns":["{name}"],
    "type":"transform"
    },
    {
    "name": "{geometris}", # ns+"geometry_GRP" <= geoGrp
    "patterns": ["{name}:Geometries"],
    "attrs": "{attrs}",
    "parent": "{name}:{name}_GRP",
    "type":"transform"
    },
    {
    "name": "TKRig", # ns + ns[:-1] <= rigGrp
    "attrs": "{attrs}",
    "parent": "{name}:{name}_GRP",
    "type":"transform"
    },
    {
    "name": "setRoot",
    "type": "objectSet",
    },
    {
    "name": "{name}:{geoSetName}",
    "type": "objectSet",
    "groups":["{name}:setRoot"]
    },
    {
    "name": "{name}:{ctrlSetName}",
    "type": "objectSet",
    "groups":["{name}:setRoot"]
    }
]