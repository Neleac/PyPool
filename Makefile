PYTHON = python3

TEST = test_find_best_shot.py

DEMO = demo.py

test: $(TEST)
	$(PYTHON) $^ -v

demo: $(DEMO)
	$(PYTHON) $^
