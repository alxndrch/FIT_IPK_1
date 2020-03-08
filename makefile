.PHONY: run

INTERP = python3

run:
	$(INTERP) src/server.py $(PORT)
