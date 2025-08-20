#!/bin/bash
# Simple script for converting .txt files to PROIEL XML using proiel-cli
for file in raw_texts/*.txt; do
  python3 -m proiel_cli convert --input "$file" --output "proiel_xml/$(basename "$file" .txt).xml"
done

