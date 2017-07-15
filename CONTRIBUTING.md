# Contributing Guidelines

Thanks for contributing to Django REST Pandas!  Here are some guidelines to help you get started.

## Questions

Feel free to use the issue tracker to ask questions!  We don't currently have a separate mailing list or active chat tool.  However, note that as the project grows we may eventually move questions to a separate tool.

## Bug Reports

Bug reports can take any form as long as there is enough information to diagnose the problem.  To speed up response time, try to include the following whenever possible:
 * Versions of Django REST Framework and Pandas
 * Expected (or ideal) behavior
 * Actual behavior

## Pull Requests

Pull requests are very welcome and will be reviewed and merged as time allows.  To speed up reviews, try to include the following whenever possible:
 * Reference the issue that the PR fixes (e.g. [#5](https://github.com/wq/django-rest-pandas/issues/5))
 * Failing test case fixed by the PR
 * If the PR provides new functionality, update the documentation in [README.md](https://github.com/wq/django-rest-pandas/blob/master/README.md)
 * Ensure the PR passes lint and unit tests.  This happens automatically, but you can also run these locally with the following commands:
 
```bash 
./runtests.sh # run the test suite
LINT=1 ./runtests.sh # run code style checking
```

If you would like help implementing any part of your PR, feel free to enable write access and we'll take a look as time allows.
