# DocuSound
---

`DocuSound` is an App/project that turns recording speech/audio into text, which can be used for efficient documentation and storage for written communications.

## Getting started

You can install this repo in the following way(s) provided you're in the root of this repo where the `pyproject.toml` is located 

First create a vritual environment & install latest version of pip 

```bash
$ python -m venv venv && pip install --upgrade pip
```
Then install as a package via 

```bash
$ pip install pyproject.toml .
```
You can also keep synced up with latest development changes via 

```bash
$ pip install -e .
```
To sync up with latest development changes and if you want to contribute to the project 

```bash
$ pip install -e ".[ci]"
```

