fuzzy_pb2.py: fuzzy.proto
	protoc --python_out=. fuzzy.proto
test:
	nosetests -i *_test.py -v
clean:
	rm fuzzy_pb2.py
