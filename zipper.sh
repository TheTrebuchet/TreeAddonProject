#!/bin/bash
rm CalmTree.zip;
zip -r CalmTree.zip CalmTree/;
blender -b -P enableaddon.py;
blender;
blender -b -P disableaddon.py