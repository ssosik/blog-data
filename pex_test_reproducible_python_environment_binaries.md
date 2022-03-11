---
title: "pex test, reproducible python environment binaries"
description: ""
lead: ""
date: "2019-06-19T15:07:08-04:00"
lastmod: "2019-06-19T15:07:08-04:00"
tags:
  - work
  - python
draft: true
weight: 50
images: []
contributors:
  - Steve Sosik
---

Links:
https://github.com/pantsbuild/pex
https://pex.readthedocs.io/en/stable/buildingpex.html
https://virtualenv.pypa.io/en/stable/installation/


# Steps

```sh
pip3 install --user virtualenv
virtualenv pex-test
cd pex-test
bin/pip3 install requests
bin/python3
> Python 3.5.2 (default, Nov 12 2018, 13:43:14)
> [GCC 5.4.0 20160609] on linux
> Type "help", "copyright", "credits" or "license" for more information.
> >>> import requests
> >>> requests.__version__
> '2.22.0'
> >>>
bin/pip3 install pex

cat requirements.txt
> xmlrunner
> requests
> nose
bin/pex -r requirements.txt --python python3 -o test.pex
```

asdasd
