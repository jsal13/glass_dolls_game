import pytest

from glassdolls.puzzle_generation.ciphers import (
    substitution_cipher,
    translation_table_make_str_keys,
    TranslationTable,
    TranslationTableStrKey,
)


@pytest.fixture()
def text_with_spell() -> str:
    return """I SPENT THE FOLLOWING DAY ROAMING THROUGH THE VALLEY. I STOOD BESIDE THE SOURCES OF THE ARVEIRON, WHICH TAKE THEIR RISE IN A GLACIER, THAT WITH SLOW PACE IS ADVANCING DOWN FROM THE SUMMIT OF THE HILLS TO BARRICADE THE VALLEY. THE ABRUPT SIDES OF VAST MOUNTAINS WERE BEFORE ME; THE ICY WALL OF THE GLACIER OVERHUNG ME; A FEW SHATTERED PINES WERE SCATTERED AROUND; AND THE SOLEMN SILENCE OF THIS GLORIOUS PRESENCE-CHAMBER OF IMPERIAL NATURE WAS BROKEN ONLY BY THE BRAWLING WAVES OR THE FALL OF SOME VAST FRAGMENT, THE THUNDER SOUND OF THE AVALANCHE OR THE CRACKING, REVERBERATED ALONG THE MOUNTAINS, OF THE ACCUMULATED ICE, WHICH, THROUGH THE SILENT WORKING OF IMMUTABLE LAWS, WAS EVER AND ANON RENT AND TORN, AS IF IT HAD BEEN BUT A PLAYTHING IN THEIR HANDS. THESE SUBLIME AND MAGNIFICENT SCENES AFFORDED ME THE GREATEST CONSOLATION THAT I WAS CAPABLE OF RECEIVING. THEY ELEVATED ME FROM ALL LITTLENESS OF FEELING, AND ALTHOUGH THEY DID NOT REMOVE MY GRIEF, THEY SUBDUED AND TRANQUILLISED IT. IN SOME DEGREE, ALSO, THEY DIVERTED MY MIND FROM THE THOUGHTS OVER WHICH IT HAD BROODED FOR THE LAST MONTH. I RETIRED TO REST AT NIGHT; MY SLUMBERS, AS IT WERE, WAITED ON AND MINISTERED TO BY THE ASSEMBLANCE OF GRAND SHAPES WHICH I HAD CONTEMPLATED DURING THE DAY. THEY CONGREGATED ROUND ME; THE UNSTAINED SNOWY MOUNTAIN-TOP, THE GLITTERING PINNACLE, THE PINE WOODS, AND RAGGED BARE RAVINE, THE EAGLE, SOARING AMIDST THE CLOUDS—THEY ALL GATHERED ROUND ME AND BADE ME BE AT PEACE.

    FIREBALL: UM ULT VOS"""


@pytest.fixture()
def text_with_spell_ciphertext() -> str:
    return "A ROBYZ ZEB SWXXWVAYF DHT JWHKAYF ZEJWUFE ZEB MHXXBT. A RZWWD QBRADB ZEB RWUJCBR WS ZEB HJMBAJWY, VEACE ZHNB ZEBAJ JARB AY H FXHCABJ, ZEHZ VAZE RXWV OHCB AR HDMHYCAYF DWVY SJWK ZEB RUKKAZ WS ZEB EAXXR ZW QHJJACHDB ZEB MHXXBT. ZEB HQJUOZ RADBR WS MHRZ KWUYZHAYR VBJB QBSWJB KB; ZEB ACT VHXX WS ZEB FXHCABJ WMBJEUYF KB; H SBV REHZZBJBD OAYBR VBJB RCHZZBJBD HJWUYD; HYD ZEB RWXBKY RAXBYCB WS ZEAR FXWJAWUR OJBRBYCB-CEHKQBJ WS AKOBJAHX YHZUJB VHR QJWNBY WYXT QT ZEB QJHVXAYF VHMBR WJ ZEB SHXX WS RWKB MHRZ SJHFKBYZ, ZEB ZEUYDBJ RWUYD WS ZEB HMHXHYCEB WJ ZEB CJHCNAYF, JBMBJQBJHZBD HXWYF ZEB KWUYZHAYR, WS ZEB HCCUKUXHZBD ACB, VEACE, ZEJWUFE ZEB RAXBYZ VWJNAYF WS AKKUZHQXB XHVR, VHR BMBJ HYD HYWY JBYZ HYD ZWJY, HR AS AZ EHD QBBY QUZ H OXHTZEAYF AY ZEBAJ EHYDR. ZEBRB RUQXAKB HYD KHFYASACBYZ RCBYBR HSSWJDBD KB ZEB FJBHZBRZ CWYRWXHZAWY ZEHZ A VHR CHOHQXB WS JBCBAMAYF. ZEBT BXBMHZBD KB SJWK HXX XAZZXBYBRR WS SBBXAYF, HYD HXZEWUFE ZEBT DAD YWZ JBKWMB KT FJABS, ZEBT RUQDUBD HYD ZJHYLUAXXARBD AZ. AY RWKB DBFJBB, HXRW, ZEBT DAMBJZBD KT KAYD SJWK ZEB ZEWUFEZR WMBJ VEACE AZ EHD QJWWDBD SWJ ZEB XHRZ KWYZE. A JBZAJBD ZW JBRZ HZ YAFEZ; KT RXUKQBJR, HR AZ VBJB, VHAZBD WY HYD KAYARZBJBD ZW QT ZEB HRRBKQXHYCB WS FJHYD REHOBR VEACE A EHD CWYZBKOXHZBD DUJAYF ZEB DHT. ZEBT CWYFJBFHZBD JWUYD KB; ZEB UYRZHAYBD RYWVT KWUYZHAY-ZWO, ZEB FXAZZBJAYF OAYYHCXB, ZEB OAYB VWWDR, HYD JHFFBD QHJB JHMAYB, ZEB BHFXB, RWHJAYF HKADRZ ZEB CXWUDR—ZEBT HXX FHZEBJBD JWUYD KB HYD QHDB KB QB HZ OBHCB.\n\n    SAJBQHXX: UK UXZ MWR"


@pytest.fixture()
def text_with_spell_trans_table() -> TranslationTable:
    return {
        65: "H",
        66: "Q",
        67: "C",
        68: "D",
        69: "B",
        70: "S",
        71: "F",
        72: "E",
        73: "A",
        74: "I",
        75: "N",
        76: "X",
        77: "K",
        78: "Y",
        79: "W",
        80: "O",
        81: "L",
        82: "J",
        83: "R",
        84: "Z",
        85: "U",
        86: "M",
        87: "V",
        88: "G",
        89: "T",
        90: "P",
    }


@pytest.fixture()
def text_with_spell_trans_table_str_key() -> TranslationTableStrKey:
    return {
        "A": "H",
        "B": "Q",
        "C": "C",
        "D": "D",
        "E": "B",
        "F": "S",
        "G": "F",
        "H": "E",
        "I": "A",
        "J": "I",
        "K": "N",
        "L": "X",
        "M": "K",
        "N": "Y",
        "O": "W",
        "P": "O",
        "Q": "L",
        "R": "J",
        "S": "R",
        "T": "Z",
        "U": "U",
        "V": "M",
        "W": "V",
        "X": "G",
        "Y": "T",
        "Z": "P",
    }


def test_substitution_cipher(
    text_with_spell: str,
    text_with_spell_ciphertext: str,
    text_with_spell_trans_table: TranslationTable,
) -> None:
    ciphertext, trans_table = substitution_cipher(text=text_with_spell)
    assert ciphertext == text_with_spell_ciphertext
    assert trans_table == text_with_spell_trans_table


def test_translation_table_make_str_keys_outputs_correctly(
    text_with_spell_trans_table: TranslationTable,
    text_with_spell_trans_table_str_key: TranslationTableStrKey,
) -> None:
    trans_table_str_key = translation_table_make_str_keys(
        translation_table=text_with_spell_trans_table
    )
    assert trans_table_str_key == text_with_spell_trans_table_str_key
