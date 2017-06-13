#!/bin/sh

echo $2 | cut -d ':' -f 2 - > /home/gwuser/is_button_pressed
