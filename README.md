# ChromeDownload
ChromeDownload by har or json

## dependence
```python
from __future__ import print_function

import json
import logging
import os
import time

import requests
```
## quickstart

```python
    ChromeDownload(r'F:\PYWP\ChromeDownload\localhost.json', 'http://localhost/peise/peise/www.peise.net/').download()
```

the json file comes from chrome 'F12' >> 'Network' >> 'F5' >> 'save as HAR from content' >> 'rename as json or keep har'
