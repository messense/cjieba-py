# cjieba-py

[![Build Status](https://travis-ci.org/messense/cjieba-py.svg?branch=master)](https://travis-ci.org/messense/cjieba-py)
[![codecov](https://codecov.io/gh/messense/cjieba-py/branch/master/graph/badge.svg)](https://codecov.io/gh/messense/cjieba-py)
[![PyPI](https://img.shields.io/pypi/v/cjieba.svg)](https://pypi.python.org/pypi/cjieba)

Python cffi binding to [cppjieba](https://github.com/yanyiwu/cppjieba) via [cppjieba-cabi](https://github.com/messense/cppjieba-cabi)

## Installation

```bash
pip install -U cjieba
```

## Example

```python
import cjieba

cjieba.cut('今天天气怎么样')
```

## License

This work is released under the MIT license. A copy of the license is provided in the [LICENSE](./LICENSE) file.
