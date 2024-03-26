
# Updating

!!! warning inline inline-wide end "Mid-Project Tool Updates"
    Updating the tools in the middle of a project may require re-extraction of files due to format changes, or the recreation of .blend files by re-importing your models.  Thus, it is recommended to avoid upgrades unless you are willing to update your project files.

## GUI Tools

To update the tools themselves, you should delete the contents of your `cobra-tools`(1) folder entirely and extract the newer tools into the same folder. This clears out any old, unused, or cached files that may interfere with tool updates.
{ .annotate }

1. e.g. `cobra-tools-master`

## Python Dependencies

The tools have an auto-updater to handle Python dependency updates for you, which will operate the same as the automatic installer in [Installing Python Dependencies](Download.md#installing-python-dependencies).

## Blender Plugin

!!! warning "Construction"
    This area is currently under construction!

## Symlinking Guide

If you would prefer to ensure that your GUI tools and Blender Plugin are always synced, you can create a symlink so that both operate from the same location. 

!!! warning "Construction"
    This area is currently under construction!
