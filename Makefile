src = $(shell find . -name '*index.md')
obj = $(src:.md=.html)

all: upload

html: $(obj)

upload: $(obj) posts/rss.xml
	rsync -avz ./ root@astrologer.cc:/var/www/html/

$(obj):%.html:%.md tmpl.html
	pandoc --template tmpl.html \
			--metadata title="$(shell cat $(shell dirname $<)/title)" $< \
			| sed "s/’/'/g" \
			| sed 's/”/\&quot;/g' \
			| sed 's/“/\&quot;/g'> $@

posts/rss.xml: posts/index.html
	./genrss.py
