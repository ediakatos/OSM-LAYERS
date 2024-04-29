.PHONY: run

run:
	@echo "Running main.py script..."
	@./venv/bin/python src/main.py

# .PHONY: setup run

# VENV := ./venv
# PYTHON := $(VENV)/bin/python
# PIP := $(VENV)/bin/pip

# # Target to create the virtual environment and install dependencies
# setup: $(VENV)/bin/activate
# 	$(PIP) install osmnx geopandas pandas
# 	@echo "Setup complete. Virtual environment and dependencies are ready."

# $(VENV)/bin/activate:
# 	python3 -m venv $(VENV)
# 	$(PIP) install --upgrade pip

# # Target to run the script
# run: setup
# 	@echo "Running main.py script..."
# 	@$(PYTHON) src/main.py

# .PHONY: setup run

# VENV := ./venv
# PYTHON := $(VENV)/bin/python
# PIP := $(VENV)/bin/pip

# # Target to create the virtual environment and install dependencies
# setup: $(VENV)/bin/activate

# $(VENV)/bin/activate:
# 	@test -d $(VENV) || python3 -m venv $(VENV)
# 	@$(PIP) install --upgrade pip
# 	@$(PIP) freeze | grep -qxF "osmnx" || $(PIP) install osmnx
# 	@$(PIP) freeze | grep -qxF "geopandas" || $(PIP) install geopandas
# 	@$(PIP) freeze | grep -qxF "pandas" || $(PIP) install pandas
# 	@echo "Setup complete. Virtual environment and dependencies are ready."

# # Target to run the script
# run: setup
# 	@echo "Running main.py script..."
# 	@$(PYTHON) src/main.py
