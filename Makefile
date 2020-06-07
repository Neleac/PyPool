PYTHON = python3

TEST = test_find_best_shot.py

test: $(TEST)
	$(PYTHON) $^ -v
