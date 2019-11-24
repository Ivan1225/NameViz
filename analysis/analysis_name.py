import nltk
from nltk.corpus import wordnet as wn
import re

def check_outlier(name, name_type):
    d=dict()
    d['isOutlier'] = False
    d['errorMessage']=""
    try:
          if name_type == 'class':
            class_name_helper(name)
          elif name_type == 'interface':
            interface_name_helper(name)
          elif name_type == 'method':
            method_name_helper(name)
          elif name_type == 'variable':
            variable_name_helper(name)
          elif name_type == 'constant':
            constant_name_helper(name)
          else:
            raise Exception("Please specify the name type for the name")
    except Exception as e:
          d['isOutlier'] = True
          d['errorMessage'] = e
    finally:
          print(d)
          return d


def class_name_helper(name):
    if name[0].isupper():
        last_word = camel_case_split(name)[-1]
        synsets = check_sysnsets(last_word)
        for word in camel_case_split(name):
            if not bool(check_sysnsets(word)):
                raise Exception('Unknown word: '+word+', or you should use camel case for class name')
        if 'n' in synsets:
            return True
        else:
            raise Exception('Class name should be a noun')
    else:
        raise Exception('Class name should start with the uppercase letter')


def interface_name_helper(name):
    if name[0].isupper():
        last_word = camel_case_split(name)[-1]
        synsets = check_sysnsets(last_word)
        for word in camel_case_split(name):
            if not bool(check_sysnsets(word)):
                raise Exception('Unknown word: '+word+', or you should use camel case for interface name')
        if 'a' in synsets:
            return True
        else:
            raise Exception('Interface name should be an adjective')
    else:
        raise Exception('Interface name should start with the uppercase letter')


def method_name_helper(name):
    if not name[0].isupper():
      last_word = camel_case_split(name)[0]
      synsets = check_sysnsets(last_word)
      for word in camel_case_split(name):
          if not bool(check_sysnsets(word)):
              raise Exception('Unknown word: '+word+', or you should use camel case for method name')
      if 'v' in synsets:
          return True
      else:
          raise Exception('Method name should be a verb')
    else:
        raise Exception('Method name should start with the lowercase letter')


def variable_name_helper(name):
    if not name[0].isupper():
      if len(name) == 1:
        raise Exception('Avoid using one-character variables name')
      if not check_start_with_special_char(name):
          raise Exception('Variable name should not start with the special characters')
      for word in camel_case_split(name):
          if not bool(check_sysnsets(word)):
              raise Exception('Unknown word: '+word+', or you should use camel case for variable name')
      return True
    else:
        raise Exception('Variable name should start with the lowercase letter')


def constant_name_helper(name):
    if name.isupper():
        if not check_start_with_special_char(name):
            raise Exception('Constant name should not start with the special characters')
        if name[0].isdigit():
            raise Exception('Constant name first letter should not be digit')
        for word in name.split("_"):
            if not bool(check_sysnsets(word)):
                raise Exception('Unknown word: '+word+', or you should use snake case for constant name')
        return True
    else:
        raise Exception('Constant name should all upper case')


def check_sysnsets(name):
    possible_types = set()
    for tmp in wn.synsets(name):
        possible_types.add(tmp.pos())
    return possible_types


def camel_case_split(str):
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str)


def check_start_with_special_char(str):
    return re.match(r'^[a-zA-Z0-9](.*)?$', str)


check_outlier("You", "class")