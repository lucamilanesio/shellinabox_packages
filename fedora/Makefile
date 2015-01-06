SOURCES=SOURCES/shellinabox-2.14-88822c1.tar.gz
SOURCES_URL=https://github.com/pythonanywhere/shellinabox_fork/archive/88822c1f4c030d5f05ced097eb7b6668ff3d7c6f/shellinabox-2.14-88822c1.tar.gz
TARGET=RPMS/x86_64/shellinabox-2.14-28.git88822c1.el6.x86_64.rpm

all: $(TARGET)

$(SOURCES):
	wget $(SOURCES_URL) -O $@

$(TARGET): $(SOURCES)
	PWD=`pwd` && pushd ~ && ln -s $(PWD) rpmbuild && popd
	rpmbuild -ba SPECS/shellinabox.spec

clean:
	rm -f $(SOURCES) 
	rm -Rf RPMS SRPMS BUILD BUILDROOT

.PHONY: clean
