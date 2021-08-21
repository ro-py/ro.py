#!/usr/bin/env python

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

for path in sorted(Path("roblox").glob("**/*.py")):
    module_path = path.with_suffix("")
    doc_path = path.with_suffix(".md")

    """
    if module_path.name == "__init__":
        full_doc_path = Path("reference", doc_path.parent, "index").with_suffix(".md")
    else:
        full_doc_path = Path("reference", doc_path)
    """

    full_doc_path = Path("reference", doc_path)

    print("PATH", path)
    print("MODPATH", module_path)
    print("DOCPATH", doc_path)
    print("FULLDOCPATH", full_doc_path)

    nav[module_path.parts] = doc_path

    with mkdocs_gen_files.open(full_doc_path, "w") as f:
        ident = ".".join(module_path.parts)
        data = "::: " + ident
        print(data)
        print(data, file=f)

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

print(nav)
# nav["mkdocs_autorefs", "references"] = "autorefs/references.md"
# nav["mkdocs_autorefs", "plugin"] = "autorefs/plugin.md"

generated_nav = nav.build_literate_nav()
print(str(generated_nav))

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(generated_nav)
