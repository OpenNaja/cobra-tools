---
title: Supported Formats
description: List of supported formats, their use, and how to edit them
icon: octicons/file-16
---

# Supported Formats

## Main Formats

| Format                | Purpose                                                                   | Editor                                                                                                 |
|-----------------------|---------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| ASSETPKG              | OVL resolve name                                                          | Any text editor                                                                                        |
| MDL2 & MS2            | Mesh data link & buffer                                                   | Blender 3.6+ & Cobra Plugin                                                                            |
| FGM                   | Fragment Material properties                                              | FGM Editor                                                                                             |
| TEX / PNG / DDS       | Textures, GUI images                                                      | Any image editor for PNG (Recommended: GIMP, Photoshop), Any text editor for TEX (change compression settings) |
| FDB                   | Stats, asset definitions                                                  | SQLite database editor (Recommended: [SQliteStudio](https://sqlitestudio.pl/))                         |
| TXT                   | In-game texts                                                             | Any text editor                                                                                        |
| MOTIONGRAPH           | Behavior graph for animation system                                       | Any text editor (Note: Not every .motiongraph fully supported)                                         |
| BANI & BANIS          | Baked animations, only location and rotation keys                         | Blender 3.6+ & Cobra Plugin (partial import)                                                           |
| MANI & MANIS          | Animations supporting location, rotation, scale, shear, shape keys and IK | Blender 3.6+ & Cobra Plugin (full support for uncompressed, partial support for compressed)            |
| MATERIALCOLLECTION    | Additional material options & linking                                     | Matcol Editor                                                                                          |
| LUA                   | Game logic                                                                | Currently not reliably decompiled                                                                      |
| PSCOLLECTION          | Game database queries                                                     | Any text editor                                                                                        |
| XML                   | Game logic                                                                |                                                                                                        |
| FCT                   | Font File                                                                 |                                                                                                        |
| BNK/AUX               | Sound Files                                                               | WWise to convert .wav to .wem                                                                          |
| USERINTERFACEICONDATA | OVL resolve name/path                                                     | Any text editor                                                                                        |
| GFX                   | Provides UI context                                                       | Flash decompiler (Recommended: [JPEXS](https://github.com/jindrapetrik/jpexs-decompiler))              |


## Miscellaneous Formats

These are editable in any XML or plaintext editor.

| Format                | Purpose                                                                   |
|-----------------------|---------------------------------------------------------------------------|
| .accountcustomisation          |                                                                  |
| .accountlevelsdata             |                                                                  |
| .animalresearchunlockssettings | Animal Research                                                  |
| .assetpacklist                 |                                                                  |
| .assetpackobjectlists          |                                                                  |
| .brush                         |                                                                  |
| .buildingbiomelayer            |                                                                  |
| .buildingset                   |                                                                  |
| .campaigndata                  |                                                                  |
| .cinematic                     | Cutscenes                                                        |
| .curve                         |                                                                  |
| .datastreams                   |                                                                  |
| .decalsettings                 |                                                                  |
| .dinosaurmaterialeffects       | Dinosaur Materials                                               |
| .dinosaurmateriallayers        | Dinosaur Materials                                               |
| .dinosaurmaterialpatterns      | Dinosaur Materials                                               |
| .dinosaurmaterialvariants      | Dinosaur Materials                                               |
| .dlcentitlements               |                                                                  |
| .enumnamer                     | List of values for specdefs                                      |
| .fmvdesc                       |                                                                  |
| .frendercontextset             | Rendering                                                        |
| .frenderfeatureset             | Rendering                                                        |
| .frenderlodspec                | Rendering                                                        |
| .guesteconomy                  |                                                                  |
| .guestonrideanimsettings       |                                                                  |
| .habitatboundarydata           | Barriers                                                         |
| .habitatboundaryprop           | Barriers                                                         |
| .helpnodedata                  |                                                                  |
| .island                        |                                                                  |
| .janitorsettings               |                                                                  |
| .logicalcontrols               | Custom Keybinding customization                                  |
| .lut                           |                                                                  |
| .mechanicresearchsettings      | Mechanic Research                                                |
| .mergedetails                  |                                                                  |
| .missiondata                   |                                                                  |
| .motiongraphvars               |                                                                  |
| .particleatlas                 |                                                                  |
| .particleeffect                |                                                                  |
| .pathextrusion                 | Paths - Curb / Post / Endcap model definitions                   |
| .pathmaterial                  | Paths - Path Part <-> Material associations                      |
| .pathjoinpartresource          | Paths - Scenery <-> Path snapping/joining                        |
| .pathresource                  | Paths - Main Path definition                                     |
| .pathsupport                   | Paths - Path <-> SupportSet associations                         |
| .pathtype                      | Paths - Type <-> Min/Max Width associations                      |
| .supportset                    | Rides and Paths                                                  |
| .physicssurfacesxmlres         |                                                                  |
| .renderfeaturecollection       | Rendering                                                        |
| .renderparametercurves         | Rendering                                                        |
| .renderparameters              | Rendering                                                        |
| .restaurantsettings            |                                                                  |
| .ridesettings                  | Rides                                                            |
| .scaleformlanguagedata         | UI                                                               |
| .sceneryobjectresource         |                                                                  |
| .semanticflexicolours          | FlexiColour Semantic Channel definitions                         |
| .spatialuitheme                |                                                                  |
| .specdef                       | Game component validation                                        |
| .spl                           | Splines                                                          |
| .terraindetaillayers           | Terrain                                                          |
| .terrainindexeddetaillayers    | Terrain                                                          |
| .texatlas                      |                                                                  |
| .trackedridecar                | Rides                                                            |
| .trackelement                  | Rides                                                            |
| .trackmesh                     | Rides                                                            |
| .trackstation                  | Rides                                                            |
| .uimoviedefinition             | UI                                                               |
| .voxelskirt                    | Terrain                                                          |
| .weatherevents                 |                                                                  |
| .wmeta                         |                                                                  |
| .world                         |                                                                  |
| .wsm                           |                                                                  |
| .xmlconfig                     | Settings UI configuration presets                                |
