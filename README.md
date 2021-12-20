### Hexlet tests and linter status:
[![Actions Status](https://github.com/VVtatarinoff/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/VVtatarinoff/python-project-lvl3/actions)
[![Linter-check](https://github.com/VVtatarinoff/python-project-lvl3/actions/workflows/linter.yml/badge.svg)](https://github.com/VVtatarinoff/python-project-lvl3/actions/workflows/linter.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/74a5be3859e7be31d50f/maintainability)](https://codeclimate.com/github/VVtatarinoff/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/74a5be3859e7be31d50f/test_coverage)](https://codeclimate.com/github/VVtatarinoff/python-project-lvl3/test_coverage)

# Page loader
'Page-loader' is a tool that upload specified html file and all related domain files to local drive
    
The package provides as terminal session work as python package to include in other packages
The output is an HTML file and domain files saved in separate directory. HTML file's link is replaced by 
links to saved files. That way page could be opened in off-mode and working files expected
Naming on files is straight way - using literals of url and replacing all non-literals by '-'.
The package is created during educational courses at [Hexlet](https://ru.hexlet.io) step 3.

## Installation
to install the package you could enter a command:

##### python3 -m pip install --user git+https://github.com/VVtatarinoff/python-project-lvl3

to uninstall use the opposite command

## Usage

### Terminal session
command: page-loader
usage: page-loader [options] <url>

positional arguments:
  url                   url link to website

optional arguments:
  -h, --help            show this help message and exit
  -o [dir], --output [dir]

### as a library
import function page_loader.download
arguments:
    url - web address, including schema
    directory - path to directory where to save HTML file
## Links
This project was built using these tools:

| Tool                                                                        | Description                                             |
|-----------------------------------------------------------------------------|---------------------------------------------------------|
| [poetry](https://poetry.eustace.io/)                                        | "Python dependency management and packaging made easy"  |
| [flake](https://flake8.pycqa.org/en/latest/)                                | "Tool For Style Guide Enforcement"                      |
| [pytest](https://pytest.org/en/latest/)                                     | "Helps you write better programs"                       |


### Videos captured the running scenarios

## 1st - loading page and images
[![asciicast](https://asciinema.org/a/2HhovVO8UqARL3jIbwXp3c8j8.svg)](https://asciinema.org/a/2HhovVO8UqARL3jIbwXp3c8j8)

## 2nd - loading all domain links
[![asciicast](https://asciinema.org/a/XguMARmUR2sq3WoFgDOgAGhgy.svg)](https://asciinema.org/a/XguMARmUR2sq3WoFgDOgAGhgy)

## 3rd - introducing logging
[![asciicast](https://asciinema.org/a/K9bLLT7h9wvUysIw8mQfEflaB.svg)](https://asciinema.org/a/K9bLLT7h9wvUysIw8mQfEflaB)

## 4th - introducing errors handling
[![asciicast](https://asciinema.org/a/pQQtZ0r6PqJp1ZPJB7dLJoqBa.svg)](https://asciinema.org/a/pQQtZ0r6PqJp1ZPJB7dLJoqBa)

## 5th - visualization of progress
[![asciicast](https://asciinema.org/a/o4FbuE38YUEl9vmqu8mGL3Iby.svg)](https://asciinema.org/a/o4FbuE38YUEl9vmqu8mGL3Iby)