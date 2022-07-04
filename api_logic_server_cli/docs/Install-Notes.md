
## Installation Notes

### Alert - Project fails to start

Recent updates to included libs have broken previous versions of API Logic Server.  This is fixed in a new version (5.00.06), and is strongly recommended.  You can also repair broken installations as described in [Troubleshooting](../Troubleshooting).

### Heads up - Certificate Issues
We sometimes see Python / Flask AppBuilder Certificate issues - see [Troubleshooting](../Troubleshooting#certificate-failures).

### Default Python version
In some cases, your computer may have multiple Python versions, such as ```python3```.  ```ApiLogicServer run``` relies on the default Python being 3.8 or higher.  You can resolve this by:
* making ```python3``` the default Python, or
* using ```ApiLogicServer create```, and running ```python3 api_logic_server_run.py```

&nbsp; &nbsp;