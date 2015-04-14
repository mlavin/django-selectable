STATIC_DIR = ./selectable/static/selectable
QUNIT_TESTS = file://`pwd`/selectable/tests/qunit/index.html

test-js:
	# Run JS tests
	# Requires phantomjs
	phantomjs run-qunit.js ${QUNIT_TESTS}?jquery=1.11.2&ui=1.11.4
	phantomjs run-qunit.js ${QUNIT_TESTS}?jquery=1.11.2&ui=1.10.4
	phantomjs run-qunit.js ${QUNIT_TESTS}?jquery=1.10.2&ui=1.11.4
	phantomjs run-qunit.js ${QUNIT_TESTS}?jquery=1.10.2&ui=1.10.4
	phantomjs run-qunit.js ${QUNIT_TESTS}?jquery=1.9.1&ui=1.11.4
	phantomjs run-qunit.js ${QUNIT_TESTS}?jquery=1.9.1&ui=1.10.4


lint-js:
	# Check JS for any problems	
	# Requires jshint
	jshint ${STATIC_DIR}/js/jquery.dj.selectable.js


.PHONY: lint-js test-js
