---
title: Cobra Tools Development
icon: material/console
---

# Development

## Code Contributions

If you are interested in contributing to the codebase:

1. Install the dev dependencies. From `cobra-tools` directory run:
    ```
    python.exe -m pip install --upgrade pip && pip install .[gui,dev]
    ```

2. Then install the pre-commit hooks:
    
    ```
    pre-commit install -f
    ```

## Documentation Contributions

If you are interested in contributing to the documentation:

1. Install the mkdocs dependencies. From `cobra-tools` directory run:
    ```
    python.exe -m pip install --upgrade pip && pip install .[doc]
    ```

2. Then, you may run mkdocs locally with:
    
    ```
    mkdocs serve
    ```

3. Your documentation edits and additions will be refreshed live as long as the mkdocs server is running.
