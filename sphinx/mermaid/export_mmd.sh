#!/bin/sh -e

FILES="ast_node_hierarchy a_plus_b"

for F in $FILES; do
   npx mmdc --scale 2 -i ../source/ast_img/${F}.mmd -o ../../paper_diagrams/mmd/${F}.png
done

