This script requires requests_html module:

```
pip install requests_html
```
or just use requirements.txt
```
pip install -r requirements.txt
```


Config file usage:

Write an url and xpath locator(s) with ; as a separator

Possible formats:

```
url;
```
```
url;locator1
```
```
url;locator1;locator2;
```

Example:

```
https://www.example.com/;//a[@href];//h1[contains(text(), 'Example Domain')]
```

In this case this script checks site https://www.example.com/ and looks for elements with xpaths '//a[@href]' and '//h1[contains(text(), 'Example Domain')]'

You can also use config.txt file in the project's directory as an example.

If a site doesn't have locators specified, the script only checks a status code.


Arguments to run:
```
-h 	--help			help
-ar 	--allow_redirect	allow redirects. No redirects by default
-d 	--delay			set delay (in seconds). Default value - 60
-t 	--timeout		set request timeout (in seconds). Default value - 5
-cfg	--config_file		set a path to the config file. Default path is "config.txt" in the project's directory
-logs 	--logging_level		set logging level: DEBUG, INFO, WARNING, ERROR. Default level - INFO
-lfsize	--log_file_size		change maximum size of a log file (in bytes). Default value - 20971520. The last log file will be backed up when the size limit is reached.
```
