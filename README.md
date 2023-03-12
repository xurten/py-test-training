# py-test-training
This repository contains python automation tests written by using playwright with pytest(The **Fluent Page Object** pattern was used)

* Page objects are in pages folder
* Tests are in tests folder

# Run the tests
pip3 install requirements.txt
pytest --headed --slowmo 1000 -n 6 --html=report.html --self-contained-html --capture=tee-sys -m regression

For html report add:
--template=html1/index.html --report=report.html

# Example tests results
![image](https://user-images.githubusercontent.com/7273568/224503717-e861b105-7b73-4a5e-bae7-b3f43c22d72d.png)

