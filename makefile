ifeq ($(origin .RECIPEPREFIX), undefined)
	$(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >
.ONESHELL: #

device?=tty.usbserial-537A0032211
remote_qa_path=../qa/qa.py

upload_%:
> ampy --port /dev/$(device) put $*

reset:
> ampy --port /dev/$(device) run reset.py

upload: upload_main.py upload_memo.py upload_questioner.py upload_qa.py

upload_other_qa: 
> ampy --port /dev/$(device) put $(remote_qa_path)

test:
> python3 test_memo.py
> python3 test_questioner.py

format:
> black .

lint:
> proselint README.md