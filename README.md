# Geolocation Service [![Codacy Badge](https://app.codacy.com/project/badge/Grade/5d3845b850a744d5a52f48b16ffb1816)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=deliveryhero/fp-apac-gaia-pathfinder&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/5d3845b850a744d5a52f48b16ffb1816)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=deliveryhero/fp-apac-gaia-pathfinder&utm_campaign=Badge_Coverage)

## Description
This service produces a set of lat/lon spread over a given geographical region.

## Instruction

1.  install [node.js](https://treehouse.github.io/installation-guides/mac/node-mac.html)

2.  making virtual python environment
    1.  install [python3.8](https://www.python.org/downloads/mac-osx/)

    2.  install [virtual env](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

    3.  making virtual environment, activation

        ```python
        python3 -m venv venv
        source venv/bin/activate
        ```

    4.  install python modules

        ```python
        pip install --no-cache-dir -r requirements.txt
        pip install --no-cache-dir -r requirements-test.txt
        ```

3.  install serverless modules

    ```bash
    npm install
    npm install -g serverless
    sls plugin install -n serverless-python-requirements --accountId {accountId}
    ```

## Execute scraping
### Local environment
```bash
sls invoke local -f coverer --accountId {accountId}
```
