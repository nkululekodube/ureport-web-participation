from behave import *
from splinter.browser import Browser
from django.core import management
from selenium import webdriver

def before_all(context):
    context.browser = Browser('firefox')
    # driver = webdriver.Firefox()

def after_all(context):
    context.browser.quit()
    context.browser = None