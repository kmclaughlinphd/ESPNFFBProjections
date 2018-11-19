#!/bin/bash

#tmpfile = $( mktemp )

# build file w/ 'name','scores'
sed 's|.*\s\([A-Z,a-z][A-Z,a-z]*\s[A-Z,a-z][A-Z,a-z]*\)\s\s*at\s.*[0-9])\s*\([A-Z,a-z]*\s[A-Z,a-z]*\).*\s\([0-9,\.]*\)-\([0-9,\.]*\)|\1,\3,\2,\4|' $1  |\
	grep -v WEEK |\
	grep -v AWAY |\
	grep [A-Z,a-z]  #> $tmpfile

