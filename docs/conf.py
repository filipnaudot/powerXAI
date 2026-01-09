project = "powerXAI"
extensions = ["sphinx.design"]
html_theme = "sphinx_book_theme"

extensions = [
    "sphinx.ext.autodoc",     # Pull docstrings from code.
    "sphinx.ext.napoleon",    # Google/NumPy style docstrings.
    "sphinx.ext.viewcode",    # Link to highlighted source.
    "sphinx.ext.autosummary", # Optional summaries.
    "sphinx_design",          # Allow for nicer documentation. 
]


autodoc_mock_imports = []
autodoc_typehints = "description"
autosummary_generate = False

################################################
import os
import sys
sys.path.insert(0, os.path.abspath("../src"))

# html_logo = "..."
html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/filipnaudot/powerXAI",
    "repository_branch": "main",
    "path_to_docs": "docs",

    "use_repository_button": True,
    "use_source_button": False,
    "use_edit_page_button": False,
    "use_download_button": False,
    "use_fullscreen_button": False,

    "logo": {
        "image_light": "_static/logo-powerxai.png",
        "image_dark": "_static/logo-powerxai.png",
        "text": "powerXAI",
        "alt_text": "powerXAI documentation",
    }
}
html_static_path = ["_static"]

# Don not crash on minor nitpicks.
nitpicky = False