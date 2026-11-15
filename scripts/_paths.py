"""_paths.py - where the toolkit ends and the instance begins.

The toolkit is this repository: scripts, templates, docs, plugins. The instance is
a workspace directory that never enters the toolkit's git:

    <repo>/workspace/memory      the memory system the digest reads
    <repo>/workspace/specs       mirror of Projects/**/spec.md

Environment overrides, for an install outside the portfolio layout:

    ABAP_WORKSPACE        instance directory       default <repo>/workspace
    ABAP_PROJECTS_ROOT    program folders          default <repo>.parent/Projects
    ABAP_INDEX            portfolio index file     default <projects root>.parent
                                                   .parent/INDEX.md

A missing directory is not an error here: the checks report it with a readable
message instead of a traceback.
"""

import os
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _path(env, default):
    value = os.environ.get(env)
    if not value:
        return default
    path = Path(value).expanduser()
    return path if path.is_absolute() else (Path.cwd() / path)


WORKSPACE = _path("ABAP_WORKSPACE", REPO / "workspace")
MEM = WORKSPACE / "memory"
SPECS = WORKSPACE / "specs"
PROJECTS = _path("ABAP_PROJECTS_ROOT", REPO.parent / "Projects")
INDEX = _path("ABAP_INDEX", PROJECTS.parent.parent / "INDEX.md")
