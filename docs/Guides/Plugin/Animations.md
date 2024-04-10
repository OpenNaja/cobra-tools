# Animations

## Manis

Manis animations are sampled across all frames for different bones and transform channels. They are generally used for advanced character animation that requires dynamics, constraints or blending between animations.

### Import

Select a target armature you want to animate before importing a manis file.

!!! construction "Limitations"
    - Compressed animations are currently imported incompletely. Specifically, only every 32nd rotation keyframe is imported.
    - Not all anims decompress correctly. If an anim fails to decompress, you may see no keyframes at all or a distorted mess.

### Export

Transforms in blender actions are stored relative to the armature, but absolute in manis. As a result, manis export must know which actions belong to which armature:

- If you have a single action per armature, setting it as the current action in the Action Editor is enough.
- To export multiple actions from an armature, stash them in the NLA Editor.

Export does not read the keyframes directly, but samples the visual transforms across an action's frame range. Constraints are automatically baked. Bones that don't move during an action are automatically discarded.

!!! construction "Limitations"
    Export only produces uncompressed animations, which occupy a lot of disk space and RAM bandwidth in-game. The game uses compressed animations for almost everything.

### Scaling

A command line script is provided to scale compressed animations and ms2 models by a given factor.

## Banis

Banis animations are rigidly sampled for all bones in a model. They are generally used for simple building or character animations, such as:

- guests
- feeders
- exhibit animals

!!! construction "Limitations"
    The transforms used by banis are currently not fully understood. Import is experimental and close to expected for some banis, but totally broken for others. Export is not useable in production.