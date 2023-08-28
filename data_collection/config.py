#!/usr/bin/env python3

from pathlib import Path

HOME_DIR = Path('.').resolve()
OUTPUT_DATA_DIR = HOME_DIR / 'out'

VLR_URL = 'https://vlr.gg'

VCT_URL = '/vct-{0}'

VLR_EVENT_URL = '/event/{0}'
VLR_EVENT_MATCHES_URL = '/event/matches/{0}'
