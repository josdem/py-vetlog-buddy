#  Copyright 2026 Jose Morales contact@josdem.io
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License
from importlib.metadata import version

"""
Python convention:
- project name is the human-readable name using dashes: "vetlog-buddy"
- package name is the importable name using underscores: "vetlog_buddy"
"""
# Get project info from pyproject.toml
__project__ = "vetlog-buddy"
__version__ = version(__project__)
