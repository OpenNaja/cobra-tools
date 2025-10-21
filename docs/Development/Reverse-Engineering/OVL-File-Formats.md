---
title: Reverse Engineering an OVL File Format
description: A primer for the reverse engineering workflow of OVL file formats
icon: octicons/file-binary-16
---

# Reverse Engineering an OVL File Format

This tutorial assumes that you have basic knowledge of a hex editor, data types and reverse engineering in general.

## Workflow

1. Download the source code for cobra tools, open in an IDE. For a new format, you need to do three things:
    * In `/source/formats/`, duplicate an existing OVL file format's folder (eg. `animalresearch`) and rename it to your new format. Rename the XML inside of it, too.
    * Run `python -m codegen` to generate `.py` files from the XML structure definitions in `/source/formats/`. These will be put in in `/generated/formats/`. Whenever you have made a change to an XML definition, run the codegen again to update the `.py` files.
    * In `/modules/formats/`, create a new `.py` file with a class that handles your format. This tells the tools which XML-defined struct class to use (eg. `ResearchRoot`) and which file extension to apply this to (eg. `.animalresearchunlockssettings`). Minimal example:
    ```python
    from generated.formats.animalresearch.compound.ResearchRoot import ResearchRoot
    from modules.formats.BaseFormat import MemStructLoader


    class AnimalresearchunlockssettingsLoader(MemStructLoader):
        target_class = ResearchRoot
        extension = ".animalresearchunlockssettings"
    ```

2. Open an OVL file with your format in the OVL editor, run `Util > Dump Debug Data`.

    !!! note "DEV MODE"
        Certain dev functions require the existence of a `.git` folder in the `cobra-tools` location. Either checkout the repository with `git`, or create this folder to enable Dev Mode.

3. Open the `.stack` file that was created in your OVL's folder. Search for your file extension. You will find, for example, the following:

    ```
    FILE [  0 |    896] (  64) cc_anubis.fgm
    PTR @ 16   -> SUB [  0 |    164] ( 120)
    PTR @ 24   -> SUB [  0 |    288] ( 608)
    PTR @ 32   -> SUB [  0 |   1008] (  40)
        DEP @ 0    -> cc_anubis.paosamplertexture.tex
        DEP @ 8    -> cc_anubis.pbasecolourtexture.tex
        DEP @ 16   -> cc_anubis.pflexicolourmaskssamplertexture.tex
        DEP @ 24   -> cc_anubis.pmetalsmoothnesscavitysamplertexture.tex
        DEP @ 32   -> cc_anubis.pnormaltexture.tex
    PTR @ 40   -> SUB [  0 |      0] ( 164)
    ```

4. The above tells you that the main struct for `cc_anubis.fgm` starts in pool number 0 at offset `896` and occupies `64` bytes, starting at that offset.

5. Open the pool `.dmp` file in a hex editor. If you set the width to `8` (not always useful), navigate to offset `896`, you will see the following:

    ```
    Offset(d) 00       04
    00000896  05000000 00000000  ........
    00000904  26000000 00000000  &.......
    00000912  40504F49 4E544552  @POINTER
    00000920  40504F49 4E544552  @POINTER
    00000928  40504F49 4E544552  @POINTER
    00000936  40504F49 4E544552  @POINTER
    00000944  00000000 00000000  ........
    00000952  00000000 00000000  ........
    ```

    The hex and the stack log tell you a number of things:

    * There are 4 pointers in your struct, which occupy 32 bytes in total (from 912-944, or relative to the struct: 16-48). For convenience, pointers are always given with `PTR @ relative_offset` in the log and marked `@POINTER` in the `.dmp`.
    * There are likely integers at relative offsets 0 (`5`) and 8 (`38`). These could represent counts for one of the pointers.
    * This file depends on 5 external files (in this case `.tex` textures, which makes sense, as a `.fgm` material has to refer to them). These are marked `DEP @ relative_offset` in the log and marked `@DEPENDS` in the `.dmp`. But these do not appear directly in the main struct.

    Let's start by writing an XML representation for the main struct, which covers its 64 bytes:
    ```xml
        <struct name="FgmHeader" inherit="MemStruct">
            <field name="count_0" type="uint64" />
            <field name="count_1" type="uint64" />
            <field name="ptr_0" type="Pointer" />
            <field name="ptr_1" type="Pointer" />
            <field name="ptr_2" type="Pointer" />
            <field name="ptr_3" type="Pointer" />
            <field name="unk_0" type="uint64" />
            <field name="unk_1" type="uint64" />
        </struct>
    ```
    Setting `type` to `Pointer` will make the tool read those 8 bytes as a pointer and then read a sub-struct at the address that this pointer points to. But first, you need to figure out the data layout of the pointer's sub-struct for this to work.

6. Look at the sub-structs pointed to by the pointers.

    For `PTR @ 16`, you'll find 120 bytes starting at offset 164. You'll notice a repetition in the pattern after 24 bytes.
    ```
    Offset(d) 00       04
    00000160           AC020000      ¬...
    00000168  08000000 00000000  ........
    00000176  00000000 00000000  ........
    00000184  00000000 BE020000  ....¾...
    00000192  08000000 01000000  ........
    00000200  00000000 00000000  ........
    00000208  00000000 D1020000  ....Ñ...
    ........
    ```
    The size `24 (size of sub-sub-struct) * 5 (count) = 120 (size of sub-struct)` indicates that the count is actually used for this pointer, and you're looking at an array. The whole struct for `PTR @ 16`, now set to 24 bytes width. Now you can see the sub-sub-struct is likely composed of 6 `uint`s. The first of these could be a string offset, the second is constantly 8, the third increments (an index?) and the rest are zeros.

    ```
    Offset(d) 00       04       08       12       16       20

    00000144                                               AC020000                      ¬...
    00000168  08000000 00000000 00000000 00000000 00000000 BE020000  ....................¾...
    00000192  08000000 01000000 00000000 00000000 00000000 D1020000  ....................Ñ...
    00000216  08000000 02000000 00000000 00000000 00000000 F1020000  ....................ñ...
    00000240  08000000 03000000 00000000 00000000 00000000 16030000  ........................
    00000264  08000000 04000000 00000000 00000000 00000000           ....................

    ```

    For `PTR @ 32`, you'll find 40 bytes, occupied only by 5 dependency links. The stack log tells you which external file dependency points there.
    ```
    Offset(d) 00       04
    00001008  40444550 454E4453  @DEPENDS
    00001016  40444550 454E4453  @DEPENDS
    00001024  40444550 454E4453  @DEPENDS
    00001032  40444550 454E4453  @DEPENDS
    00001040  40444550 454E4453  @DEPENDS
    ```

7. Now you have some more knowledge of the format, so time to document the struct in XML syntax for the codegen. This will result in something like the following:

    ```xml
        <struct name="FgmHeader" inherit="MemStruct">
            <field name="count_0" type="uint64" />
            <field name="count_1" type="uint64" />
            <field name="array_0" type="ArrayPointer" template="Sub1" arg="count_0"/>
            <field name="ptr_1" type="Pointer" />
            <field name="dependencies" type="Pointer" />
            <field name="ptr_3" type="Pointer" />
            <field name="unk_0" type="uint64" />
            <field name="unk_1" type="uint64" />
        </struct>

        <struct name="Sub1" inherit="MemStruct">
            <field name="offset" type="uint" />
            <field name="constant_eight" type="uint" />
            <field name="index" type="uint" />
            <field name="zero_0" type="uint" />
            <field name="zero_1" type="uint" />
            <field name="zero_2" type="uint" />
        </struct>
    ```
    Notice that `ptr_0` has been renamed to `array_0`, its `type` changed to `ArrayPointer`. Its sub-struct is set to `template="Sub1"`, counted by `arg="count_0"`.


## Tips & Tricks

!!! info "Identifying counts for pointers"
    You'll want to compare the data size of the sub-structs with candidates for counts. If you find integer divisions, you have a likely match. Be aware that these are memory representations and (array) data can be and often is padded to align with 16 bytes offsets.

    In most but not all formats, the count somewhat counter-intuitively _follows_ the array pointer.

!!! info "Data type of sub-structs"
    A quick way to determine the data type of sub-structs is looking at the stack log.

    - Are there any pointers in the sub-struct? &rarr; it must be a struct too
    - Is its length not divisible by 8? &rarr; it is most likely a ZString

!!! info "Finding rare pointers"
    You can easily miss out on conditional pointers if you don't look at all files of a format in the stack log, as null pointers don't necessarily appear in the stack log.

    Once you have defined and implemented a preliminary struct, open an OVL containing your format with `Debug Mode` turned on. All instances of the struct are then checked for pointers missing from the XML specification and you will receive warnings in the console if any are found.

!!! info "Naming arrays and counts"
    If you follow naming conventions for arrays and counts, the count is automatically hidden from the XML on extraction and calculated on injection. Consider the following examples:
    
    - [ ] dependencies, dependency_count
    - [x] dependencies, dependencies_count
    - [x] dependencies, num_dependencies

!!! info "Homogeneous data with no obvious pattern"
    Assuming you have identified the data type already: Modify data, put ingame, observe changes to identify the meaning of the data.

!!! info "Comparing to original"
    Once you have a suitable XML description, extract your file and inject it back into the ovl. If it injected successfully, select the file in the GUI and click Utils > Compare, then select the OVL that contains the original file. If there are differences, you will find warnings in the log. If the injected file is identical to the original, the log will tell you so. You then have a working description of your format, at least for that particular file.
    
