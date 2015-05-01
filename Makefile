DESCRIPTION.rst: README.md
	pandoc -f markdown -t rst -o $@ $<
