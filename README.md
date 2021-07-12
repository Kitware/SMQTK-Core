# SMQTK - Core

## Intent
Provide a light-weight framework for developing interfaces that have built-in
implementation discovery and factory construction from configuration.

## Libraries

SMQTK-Core is used by 6 SMQTK-* libraries, all of which are pip-installable:

[SMQTK-Classifier](https://github.com/Kitware/SMQTK-Classifier) provides interfaces and implementations around classification.

[SMQTK-Descriptors](https://github.com/Kitware/SMQTK-Descriptors) provides algorithms and data structures around computing descriptor vectors.

[SMQTK-Relevancy](https://github.com/Kitware/SMQTK-Relevancy) provides interfaces and implementations around providing search relevancy estimation.

[SMQTK-Image-IO](https://github.com/Kitware/SMQTK-Image-IO) provides interfaces and implementations around image input/output.

[SMQTK-Indexing](https://github.com/Kitware/SMQTK-Indexing) provides interfaces and implementations around the k-nearest-neighbor algorithm.

[SMQTK-Dataprovider](https://github.com/Kitware/SMQTK-Dataprovider) provides data structure abstractions.

## Documentation
https://smqtk-core.readthedocs.io/en/stable/

You can also build the sphinx documentation locally for the most up-to-date
reference:
```bash
# Install dependencies
poetry install
# Navigate to the documentation root.
cd docs
# Build the docs.
poetry run make html
# Open in your favorite browser!
firefox _build/html/index.html
```
