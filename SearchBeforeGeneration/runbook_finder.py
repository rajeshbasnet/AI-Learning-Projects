"""
There is handbook. Each handbook has 5 pages {backup, billing, login, exports, exports_archive}.md
Each page has short heading and policy which is given in problem

fixtures/handbook_manifest.json - a manifest file containing pages links (path, version, active)
exports_archive should be inactive since it's old
"""

"""
load_chunks(manifest_file_path) - if manifest malformed, report filename and underlying error
Read markdown file line by line - heading, text. Markdown containing two sections should contain
                                two records. Skip sections that contain empty body
Section  - id(<markdown_file_name>#<lowercase_heading_replaced_by_hyphens>)
        - parent_id
        - path
        - version
        - active
        - heading (Repeating headings for one file will collide id) - use order (-2, -3 depending on order)
        - text
"""
