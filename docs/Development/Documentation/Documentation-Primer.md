---
title: Documentation Primer
icon: material/file-document-edit-outline
---

# Documentation Primer

- For all features reference, see [mkdocs-material Reference](https://squidfunk.github.io/mkdocs-material/reference/#reference){:target=_blank}
- For built-in plugin reference, see [mkdocs-material Plugins](https://squidfunk.github.io/mkdocs-material/plugins/#built-in-plugins){:target=_blank}

    !!! tip "Plugins"
        Unused plugins will need to be enabled, consult the plugin documentation for enabling them in `mkdocs.yml`

## Navigation

The documentation uses [mkdocs-literate-nav](https://oprypin.github.io/mkdocs-literate-nav/index.html){:target=_blank} for navigation.

## External Linking

Please use the Markdown attribute lists extension to add `target=_blank` to external links.  This opens them in a new tab and will not interrupt documentation flow.

=== "Usage"

    ```md
    [Link](https://www.google.com/){:target=_blank}
    ```

=== "Result"

    [Link](https://www.google.com/){:target=_blank}


## Relative Linking

### Documents

Links to other Markdown files must use paths relative to the source Markdown file, and include the `.md` extension.

=== "Usage"

    ```md
    [Link](../Reverse-Engineering/OVL-File-Formats.md)
    ```

=== "Result"

    [Link](../Reverse-Engineering/OVL-File-Formats.md)


### Images and Other Assets

Other assets such as images must also be linked relative to the source Markdown file. 

#### docs/assets/images

For images in the root assets folder, you will need to traverse every subfolder with `../`

=== "Usage"

    ```md
    ![Image](../../assets/Cobra_Tools_Logo.png)
    ```

=== "Result"

    ![Image](../../assets/Cobra_Tools_Logo.png)

#### Images Subfolders

!!! warning "Remote vs Local"
    All asset links should start with at least `./` because of the way Markdown files in subfolders are rendered to a URI. For some reason links without `./` can resolve correctly locally but **not remotely**.

```shell
/docs/
  |-- Guides
    |-- Plugin
      |-- images/
        |-- image.png     # /docs/Guides/Plugins/images/image.png
      |-- index.md        # /docs/Guides/Plugins/index.md
      |-- Page.md         # /docs/Guides/Plugins/Page.md
```

In both `index.md` and `page.md`, links to `Plugin/images` should start with `./images/`.  Links starting with `images/` **will not work for `page.md`** as the URI will be `Guides/Plugin/Page/`.


## Admonitions

For full documentation see [Admonitions Usage](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#usage){:target=_blank}.

### Custom Admonitions

#### FAQ

The FAQ admonition is used for Q&A formatting, with the Question as the custom admonition name.

=== "Usage"

    ```md
    !!! faq "Question?"
        Answer
    ```

    ```md
    !!! faq "Q. Question 1?<br>Q. Question 2?"
        Answer for both questions
    ```

=== "Result"

    !!! faq "Question?"
        Answer

    !!! faq "Q. Question 1?<br>Q. Question 2?"
        Answer for both questions

!!! tip
    Be mindful of the use of quotes, line breaks, and indentation in the above example.

## Content Tabs

For full documentation see [PyMdown Extensions Tabbed](https://facelessuser.github.io/pymdown-extensions/extensions/tabbed/#syntax){:target=_blank}

Paragraphs, code blocks, and entire sections can be turned into tabs with the following syntax:

=== "Usage"

    ```
    === "Tab 1"

        Tab 1 Content

    === "Tab 2"

        Tab 2 Content
    ```

=== "Result"

    === "Tab 1"

        Tab 1 Content

    === "Tab 2"

        Tab 2 Content

!!! tip
    Be mindful of the use of quotes, line breaks, and indentation in the above example.
