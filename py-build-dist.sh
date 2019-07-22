echo "Cleaning build directory..."
rm -rf build
rm -rf dist
echo "Building wheel..."
python3 setup.py sdist bdist_wheel

# To upload to the test server
# twine upload --repository-url=https://test.pypi.org/legacy/  --sign dist/chipgr8-0.0.X* d

# To upload to pypi
# 
