# Deployment Guide

## Prerequisites

1. Install required tools:
```bash
pip install --upgrade pip setuptools wheel twine
```

2. Create accounts on:
   - PyPI: https://pypi.org/account/register/
   - TestPyPI (for testing): https://test.pypi.org/account/register/

## Build the Package

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build distribution packages
python setup.py sdist bdist_wheel
```

This creates:
- `dist/profiler-viz-0.1.0.tar.gz` - Source distribution
- `dist/profiler_viz-0.1.0-py3-none-any.whl` - Wheel distribution (if wheel is installed)

## Test on TestPyPI (Recommended)

1. Upload to TestPyPI:
```bash
twine upload --repository testpypi dist/*
```

2. Install from TestPyPI to test:
```bash
pip install --index-url https://test.pypi.org/simple/ profiler-viz
```

3. Test the installed package:
```python
from profiler_viz import func_profile

@func_profile()
def test():
    return sum(range(1000))

test()
```

## Deploy to PyPI

Once tested, upload to the real PyPI:

```bash
twine upload dist/*
```

You'll be prompted for your PyPI username and password.

## Using API Tokens (Recommended)

For better security, use API tokens instead of passwords:

1. Generate API token:
   - Go to https://pypi.org/manage/account/
   - Scroll to "API tokens"
   - Click "Add API token"
   - Give it a name and scope

2. Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-...your-token-here...

[testpypi]
username = __token__
password = pypi-...your-token-here...
```

3. Upload:
```bash
twine upload dist/*
```

## Version Bumping

Before each release:

1. Update version in:
   - `setup.py` - `version="0.1.0"`
   - `profiler_viz/__init__.py` - `__version__ = "0.1.0"`

2. Update CHANGELOG (create if doesn't exist)

3. Commit changes:
```bash
git add .
git commit -m "Bump version to 0.1.0"
git tag v0.1.0
git push origin main --tags
```

## Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install setuptools wheel twine
    - name: Build package
      run: python setup.py sdist bdist_wheel
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Add your PyPI token as a secret in GitHub:
- Go to your repo → Settings → Secrets → New repository secret
- Name: `PYPI_API_TOKEN`
- Value: your PyPI token

## Post-Deployment

After publishing:

1. Test installation:
```bash
pip install profiler-viz
```

2. Share with the community:
   - Tweet about it
   - Post on Reddit (r/Python)
   - Share on LinkedIn
   - Add to awesome-python lists

3. Monitor:
   - PyPI stats: https://pypistats.org/packages/profiler-viz
   - GitHub issues
   - User feedback

## Troubleshooting

### "File already exists"
If you get this error, you need to bump the version number. PyPI doesn't allow re-uploading the same version.

### "Invalid distribution"
Make sure `MANIFEST.in` includes all necessary files:
```
include README.md
include LICENSE
recursive-include profiler_viz *.html
```

### Import errors after installation
Check that `package_data` in `setup.py` includes the template:
```python
package_data={
    "profiler_viz": ["profile_template.html"],
},
```
