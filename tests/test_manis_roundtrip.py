import os

import pytest

from source.formats.manis.roundtrip import check_extract

OVL = r"C:\Program Files (x86)\Steam\steamapps\common\Jurassic World Evolution 3\Win64\ovldata\Content0\Dinosaurs\Land\Indoraptor\Indoraptor.ovl"
NAME = "notmotionextracted.maniset45ad1411.manis"

pytestmark = pytest.mark.skipif(not os.path.isfile(OVL), reason="game OVL not present")


def test_freshly_extracted_manis_has_intact_bulk(tmp_path):
	ok, msg = check_extract(OVL, str(tmp_path), NAME)
	assert ok, msg
