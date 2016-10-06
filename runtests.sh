set -e
if [ "$LINT" ]; then
    flake8 tests rest_pandas --exclude migrations
    flake8 */*/migrations --ignore E501
else
    python setup.py test
fi
