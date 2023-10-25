# SeleniumOC
整合Selenium常用命令

## 前置步骤
在正式使用前需要将已实例化的driver传入MailOC，如下：
```python
from selenium import webdriver
from selenium_oc import SeleniumOC

driver = webdriver.Chrome()

SeleniumOC(driver)
```