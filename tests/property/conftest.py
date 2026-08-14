"""hypothesis-Profile ``schnell`` / ``voll``, Umschaltung über ``MAR_HYPOTHESIS``."""

from __future__ import annotations

import os

from hypothesis import settings

settings.register_profile("schnell", max_examples=10, deadline=None)
settings.register_profile("voll", max_examples=300, deadline=None)
settings.load_profile(os.environ.get("MAR_HYPOTHESIS", "schnell"))
