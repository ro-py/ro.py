"""
Generates documentation for our Python modules.
"""

from pathlib import Path
import mkdocs_gen_files
nav = mkdocs_gen_files.Nav()

package_names = ["roblox"]

for package_name in package_names:
    for path in sorted(Path(package_name).glob("**/*.py")):
        module_path = path.with_suffix("")
        doc_path = path.with_suffix(".md")

        full_doc_path = Path("reference", doc_path)

        nav[module_path.parts] = str(doc_path)
        print(full_doc_path)
        with mkdocs_gen_files.open(full_doc_path, "w") as f:
            ident = ".".join(module_path.parts)
            data = "::: " + ident
            print(data, file=f)

        # mkdocs_gen_files.set_edit_path(full_doc_path, path)

generated_nav = nav.build_literate_nav()

nav_string = ""

for nav_piece in generated_nav:
    # Fix bugs with __init__ files. Why does this work? No idea.
    nav_piece = nav_piece.replace("[\\__init__]", "[\\_\\_init\\_\\_]")
    nav_piece = nav_piece.replace("__init__.md", "/__init__.md")
    nav_string += nav_piece


with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.write(nav_string)
