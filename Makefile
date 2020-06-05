PYTHON = python3

TEST = test_hit_finder.py

test: $(TEST)
	$(PYTHON) $^ -v
