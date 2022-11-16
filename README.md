# py-test-training
This repository contains python automation tests written by using playwright with pytest

* Page objects are in pages folder
* Tests are in tests folder

# Run the tests
pip3 install requirements.txt
pytest --headed --slowmo 1000 -n 6 --html=report.html --self-contained-html --capture=tee-sys -m regression
