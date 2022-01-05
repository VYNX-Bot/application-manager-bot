run:
	python3 main.py
install-dep:
	pip3 install -r requirements.txt
venv: 
	python3 -m venv .
activate-win:
	.\Scripts\activate.bat
activate-linux:
	source ./bin/activate
deactivate-win:
	.\Scripts\deactivate.bat
deactivate-linux:
	deactivate
install-dep-venv-windows:
	.\Scripts\pip.exe install -r requirements.txt
install-dep-venv-linux:
	./bin/pip3 install -r requirements.txt