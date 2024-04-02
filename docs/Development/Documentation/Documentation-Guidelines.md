---
title: Documentation Guidelines
description: Contributing guidelines for writing cobra-tools documentation
icon: material/file-document-edit-outline
---

# Documentation Guidelines

## Document Metadata

### Title

It is recommended to supply a title at the top of the document with the following syntax:

``` title="Some-Document.md"
---
title: Some Better Document Title
---
```

This allows for nice, short URIs in the URL while providing a more descriptive title for the document.

### Description

It is recommended to supply a title at the top of the document with the following syntax:

``` title="Some-Document.md"
---
description: A summary of what this document entails
---
```

The description is useful as it will display in social cards i.e. the preview when linked in Discord, etc.

### Icon

!!! tip inline end "Icon Naming"

    === "Prefix"
        - `:material-`
        - `:octoicons-`
        - `:simple-`
        - `:fontawesome-brands-`
        - `:fontawesome-regular-`
        - `:fontawesome-solid-`

    === "Path"
        - `material/`
        - `octoicons/`
        - `simple/`
        - `fontawesome/brands/`
        - `fontawesome/regular/`
        - `fontawesome/solid/`


You may want to supply a custom icon for the page which will be displayed in navigation entries. The syntax is as follows:

``` title="Some-Document.md"
---
icon: material/file-document-edit-outline
---
```

1. You can search available icons at the following [mkdocs-material page](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#search){:target=_blank}.
2. After finding a suitable icon, you must convert it from the `:icon-name:` format to an extensionless path.
    - [x] Refer to the Icon Naming guide to the right, or the path can be found in the [`.icons` folder in the mkdocs-material repository](https://github.com/squidfunk/mkdocs-material/tree/master/material/templates/.icons){:target=_blank}.
    - [ ] Do not leave the `:` on either side of the icon path

The result of using all three is as follows:

``` title="Some-Document.md"
---
title: Some Better Document Title
description: A summary of what this document entails
icon: material/file-document-edit-outline
---
```

## File and Folder Naming

- [x] For correct URIs both Markdown files and folders must use `Title-Case`, with whitespace replaced by dashes.
    - Exception: `index.md` for index pages.
    - Exception: `SUMMARY.md` for navigation.
- [ ] DO NOT use whitespace in subfolder or Markdown file names.

=== "Good"

    ```shell
    /docs/
      |-- Guides
        |-- Some-Guide
          |-- index.md
          |-- Page-One.md
          |-- Page-Two.md
    ```

=== "Bad"

    ```shell
    /docs/
      |-- Guides
        |-- Some guide
          |-- index.md
          |-- page one.md
          |-- Page-two.md
    ```

## Headings

- [x] For consistency with the combined TOC/nav, please use **short** Title Case headings.
- [ ] DO NOT use sentence case or long, run-on heading text.


=== "Good"

    ```md
    ## Using Manager Interfaces
    ```

=== "Bad"

    ```md
    ## Calling other Managers code using their interface
    ```

## Discord Channel Links

OpenNaja server channels may often need to be linked to, here is a list for copying/pasting where necessary (note the Copy button in each code block):

- **[:discord-rules: rules](https://discord.com/channels/680909673607463131/680910494151868532)**
    ```md
    **[:discord-rules: rules](https://discord.com/channels/680909673607463131/680910494151868532)**
    ```
- **[:discord-channel: guidelines](https://discord.com/channels/680909673607463131/1223893560881840151)**
    ```md
    **[:discord-channel: guidelines](https://discord.com/channels/680909673607463131/1223893560881840151)**
    ```
- **[:discord-announcements: announcements](https://discord.com/channels/680909673607463131/680910508756303894)**
    ```md
    **[:discord-announcements: announcements](https://discord.com/channels/680909673607463131/680910508756303894)**
    ```
- **[:discord-topic: modding-help-pz](https://discord.com/channels/680909673607463131/1020301021756543017)**
    ```md
    **[:discord-topic: modding-help-pz](https://discord.com/channels/680909673607463131/1020301021756543017)**
    ```
- **[:discord-topic: modding-help-jwe2](https://discord.com/channels/680909673607463131/1020306232281677916)**
    ```md
    **[:discord-topic: modding-help-jwe2](https://discord.com/channels/680909673607463131/1020306232281677916)**
    ```
