docs: docs/*.rst docs/conf.py docs/Makefile awherepy/*.py *.rst examples/*.py ## generate html docs
	#rm -f docs/awherepy.rst
	#rm -f docs/modules.rst
	sphinx-apidoc -fMeET -o awherepy awherepy/tests awherepy/example-data
	$(MAKE) -C docs clean
	$(MAKE) -C docs doctest
	$(MAKE) -C docs html
	$(MAKE) -C docs linkcheck
