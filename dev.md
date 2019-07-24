# Dev.md

Commands reference.

```bash
# Build
mekpie build

# Run C tests
mekpie test

# Run module locally
python -m chipgr8

# Build local dist
python3 setup.py sdist bdist_wheel

# Clean dist
rm -rf ./dist

# Upload to test.pypi (Replace X with version)
twine upload --repository-url=https://test.pypi.org/legacy/ dist/chipgr8-0.0.X* dist/

# Upload to pypi (Replace X with version)
twine upload dist/chipgr8-0.0.X* dist./
```