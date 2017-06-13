#!/bin/sh

echo $2 | cut -d ':' -f 2 - > $(dirname $0)/is_button_pressed
