DISTRIBS=fedora


$(DISTRIBS):
	cd $@ && $(MAKE)

.PHONY: $(DISTRIBS)
