# Python Pytest Playwright Training
This is a training repository for automated web testing using Python, Pytest, and Playwright.

# Prerequisites
To use this repository, you need to have the following software installed on your machine:

- Python 3.7 or higher
- Node.js (required by Playwright)
- Pytest (pip install pytest)
- Playwright (pip install pytest-playwright)

# Installation
1. Clone the repository: git clone https://github.com/xurten/python-pytest-playwright-training.git
2. Install the dependencies: pip install -r requirements.txt
3. Download the correct version of the browser executable for your system (see here for details)
4. Update the conftest.py file with the path to your browser executable.

# Structure
This repository contains the following directories:

- **pages**: This directory contains the Page Object Model (POM) classes that represent the pages of the tested website. Each file in this directory corresponds to a single web page, and defines a POM class for that page.
- **tests**: This directory contains the test files. Each file in this directory corresponds to a single feature or scenario, and contains one or more test cases.
- **utils**: This directory contains utility functions used by the tests.


# Run the tests
```python
pytest --headed --slowmo 1000 -n 6 --html=report.html --self-contained-html --capture=tee-sys -m regression
```
For html report add:
```python
--template=html1/index.html --report=report.html
```

# Example tests results
![image](https://user-images.githubusercontent.com/7273568/224503717-e861b105-7b73-4a5e-bae7-b3f43c22d72d.png)

# Contributing
If you would like to contribute to this project, feel free to open a pull request or an issue. All contributions are welcome!
