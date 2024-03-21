---
title: Documentation Guidelines
icon: material/file-document-edit-outline
---

# Documentation Guidelines

## File and Folder Naming

- [x] For correct URIs both Markdown files and folders must use `Title-Case`, with whitespace replaced by dashes.
    - Exception: `index.md` for index pages.
    - Exception: `SUMMARY.md` for navigation.
- [ ] DO NOT use whitespace in subfolder or Markdown file names

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

- [x] For consistency with the combined TOC/nav, please use **short** Title Case headings
- [ ] DO NOT use sentence case or long, run-on heading text.


=== "Good"

    ```md
    ## Using Manager Interfaces
    ```

=== "Bad"

    ```md
    ## Calling other Managers code using their interface
    ```
