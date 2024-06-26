import string

import pytest

from glassdolls._types import TranslationTable, TranslationTableStrKey
from glassdolls.puzzles.ciphers import (
    apply_substitution_cipher, cesaer_cipher,
    make_substitution_cipher_translation_table,
    translation_table_make_str_keys)


@pytest.fixture()
def text_with_mantra() -> str:
    return """I SPENT THE FOLLOWING DAY ROAMING THROUGH THE VALLEY. I STOOD BESIDE THE SOURCES OF THE ARVEIRON, WHICH TAKE THEIR RISE IN A GLACIER, THAT WITH SLOW PACE IS ADVANCING DOWN FROM THE SUMMIT OF THE HILLS TO BARRICADE THE VALLEY. THE ABRUPT SIDES OF VAST MOUNTAINS WERE BEFORE ME; THE ICY WALL OF THE GLACIER OVERHUNG ME; A FEW SHATTERED PINES WERE SCATTERED AROUND; AND THE SOLEMN SILENCE OF THIS GLORIOUS PRESENCE-CHAMBER OF IMPERIAL NATURE WAS BROKEN ONLY BY THE BRAWLING WAVES OR THE FALL OF SOME VAST FRAGMENT, THE THUNDER SOUND OF THE AVALANCHE OR THE CRACKING, REVERBERATED ALONG THE MOUNTAINS, OF THE ACCUMULATED ICE, WHICH, THROUGH THE SILENT WORKING OF IMMUTABLE LAWS, WAS EVER AND ANON RENT AND TORN, AS IF IT HAD BEEN BUT A PLAYTHING IN THEIR HANDS. THESE SUBLIME AND MAGNIFICENT SCENES AFFORDED ME THE GREATEST CONSOLATION THAT I WAS CAPABLE OF RECEIVING. THEY ELEVATED ME FROM ALL LITTLENESS OF FEELING, AND ALTHOUGH THEY DID NOT REMOVE MY GRIEF, THEY SUBDUED AND TRANQUILLISED IT. IN SOME DEGREE, ALSO, THEY DIVERTED MY MIND FROM THE THOUGHTS OVER WHICH IT HAD BROODED FOR THE LAST MONTH. I RETIRED TO REST AT NIGHT; MY SLUMBERS, AS IT WERE, WAITED ON AND MINISTERED TO BY THE ASSEMBLANCE OF GRAND SHAPES WHICH I HAD CONTEMPLATED DURING THE DAY. THEY CONGREGATED ROUND ME; THE UNSTAINED SNOWY MOUNTAIN-TOP, THE GLITTERING PINNACLE, THE PINE WOODS, AND RAGGED BARE RAVINE, THE EAGLE, SOARING AMIDST THE CLOUDS—THEY ALL GATHERED ROUND ME AND BADE ME BE AT PEACE.

    FIREBALL: UM ULT VOS"""


@pytest.fixture()
def text_with_mantra_ciphertext() -> str:
    return "A ROBYZ ZEB SWXXWVAYF DHT JWHKAYF ZEJWUFE ZEB MHXXBT. A RZWWD QBRADB ZEB RWUJCBR WS ZEB HJMBAJWY, VEACE ZHNB ZEBAJ JARB AY H FXHCABJ, ZEHZ VAZE RXWV OHCB AR HDMHYCAYF DWVY SJWK ZEB RUKKAZ WS ZEB EAXXR ZW QHJJACHDB ZEB MHXXBT. ZEB HQJUOZ RADBR WS MHRZ KWUYZHAYR VBJB QBSWJB KB; ZEB ACT VHXX WS ZEB FXHCABJ WMBJEUYF KB; H SBV REHZZBJBD OAYBR VBJB RCHZZBJBD HJWUYD; HYD ZEB RWXBKY RAXBYCB WS ZEAR FXWJAWUR OJBRBYCB-CEHKQBJ WS AKOBJAHX YHZUJB VHR QJWNBY WYXT QT ZEB QJHVXAYF VHMBR WJ ZEB SHXX WS RWKB MHRZ SJHFKBYZ, ZEB ZEUYDBJ RWUYD WS ZEB HMHXHYCEB WJ ZEB CJHCNAYF, JBMBJQBJHZBD HXWYF ZEB KWUYZHAYR, WS ZEB HCCUKUXHZBD ACB, VEACE, ZEJWUFE ZEB RAXBYZ VWJNAYF WS AKKUZHQXB XHVR, VHR BMBJ HYD HYWY JBYZ HYD ZWJY, HR AS AZ EHD QBBY QUZ H OXHTZEAYF AY ZEBAJ EHYDR. ZEBRB RUQXAKB HYD KHFYASACBYZ RCBYBR HSSWJDBD KB ZEB FJBHZBRZ CWYRWXHZAWY ZEHZ A VHR CHOHQXB WS JBCBAMAYF. ZEBT BXBMHZBD KB SJWK HXX XAZZXBYBRR WS SBBXAYF, HYD HXZEWUFE ZEBT DAD YWZ JBKWMB KT FJABS, ZEBT RUQDUBD HYD ZJHYLUAXXARBD AZ. AY RWKB DBFJBB, HXRW, ZEBT DAMBJZBD KT KAYD SJWK ZEB ZEWUFEZR WMBJ VEACE AZ EHD QJWWDBD SWJ ZEB XHRZ KWYZE. A JBZAJBD ZW JBRZ HZ YAFEZ; KT RXUKQBJR, HR AZ VBJB, VHAZBD WY HYD KAYARZBJBD ZW QT ZEB HRRBKQXHYCB WS FJHYD REHOBR VEACE A EHD CWYZBKOXHZBD DUJAYF ZEB DHT. ZEBT CWYFJBFHZBD JWUYD KB; ZEB UYRZHAYBD RYWVT KWUYZHAY-ZWO, ZEB FXAZZBJAYF OAYYHCXB, ZEB OAYB VWWDR, HYD JHFFBD QHJB JHMAYB, ZEB BHFXB, RWHJAYF HKADRZ ZEB CXWUDR—ZEBT HXX FHZEBJBD JWUYD KB HYD QHDB KB QB HZ OBHCB.\n\n    SAJBQHXX: UK UXZ MWR"


@pytest.fixture()
def text_with_mantra_trans_table() -> TranslationTable:
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
def text_with_mantra_trans_table_str_key() -> TranslationTableStrKey:
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


@pytest.fixture()
def text_with_mantra_casaer_cipher_amt_24() -> str:
    return "G QNCLR RFC DMJJMUGLE BYW PMYKGLE RFPMSEF RFC TYJJCW. G QRMMB ZCQGBC RFC QMSPACQ MD RFC YPTCGPML, UFGAF RYIC RFCGP PGQC GL Y EJYAGCP, RFYR UGRF QJMU NYAC GQ YBTYLAGLE BMUL DPMK RFC QSKKGR MD RFC FGJJQ RM ZYPPGAYBC RFC TYJJCW. RFC YZPSNR QGBCQ MD TYQR KMSLRYGLQ UCPC ZCDMPC KC; RFC GAW UYJJ MD RFC EJYAGCP MTCPFSLE KC; Y DCU QFYRRCPCB NGLCQ UCPC QAYRRCPCB YPMSLB; YLB RFC QMJCKL QGJCLAC MD RFGQ EJMPGMSQ NPCQCLAC-AFYKZCP MD GKNCPGYJ LYRSPC UYQ ZPMICL MLJW ZW RFC ZPYUJGLE UYTCQ MP RFC DYJJ MD QMKC TYQR DPYEKCLR, RFC RFSLBCP QMSLB MD RFC YTYJYLAFC MP RFC APYAIGLE, PCTCPZCPYRCB YJMLE RFC KMSLRYGLQ, MD RFC YAASKSJYRCB GAC, UFGAF, RFPMSEF RFC QGJCLR UMPIGLE MD GKKSRYZJC JYUQ, UYQ CTCP YLB YLML PCLR YLB RMPL, YQ GD GR FYB ZCCL ZSR Y NJYWRFGLE GL RFCGP FYLBQ. RFCQC QSZJGKC YLB KYELGDGACLR QACLCQ YDDMPBCB KC RFC EPCYRCQR AMLQMJYRGML RFYR G UYQ AYNYZJC MD PCACGTGLE. RFCW CJCTYRCB KC DPMK YJJ JGRRJCLCQQ MD DCCJGLE, YLB YJRFMSEF RFCW BGB LMR PCKMTC KW EPGCD, RFCW QSZBSCB YLB RPYLOSGJJGQCB GR. GL QMKC BCEPCC, YJQM, RFCW BGTCPRCB KW KGLB DPMK RFC RFMSEFRQ MTCP UFGAF GR FYB ZPMMBCB DMP RFC JYQR KMLRF. G PCRGPCB RM PCQR YR LGEFR; KW QJSKZCPQ, YQ GR UCPC, UYGRCB ML YLB KGLGQRCPCB RM ZW RFC YQQCKZJYLAC MD EPYLB QFYNCQ UFGAF G FYB AMLRCKNJYRCB BSPGLE RFC BYW. RFCW AMLEPCEYRCB PMSLB KC; RFC SLQRYGLCB QLMUW KMSLRYGL-RMN, RFC EJGRRCPGLE NGLLYAJC, RFC NGLC UMMBQ, YLB PYEECB ZYPC PYTGLC, RFC CYEJC, QMYPGLE YKGBQR RFC AJMSBQ—RFCW YJJ EYRFCPCB PMSLB KC YLB ZYBC KC ZC YR NCYAC.\n\n    DGPCZYJJ: SK SJR TMQ"


def test_substitution_cipher(
    text_with_mantra: str,
    text_with_mantra_ciphertext: str,
    text_with_mantra_trans_table: TranslationTable,
) -> None:
    ciphertext = apply_substitution_cipher(
        text=text_with_mantra, translation_table=text_with_mantra_trans_table
    )
    assert ciphertext == text_with_mantra_ciphertext


def test_make_substitution_cipher_translation_table_runs() -> None:
    table = make_substitution_cipher_translation_table()
    set_of_upper_alpha = set(string.ascii_uppercase)
    assert set(chr(i) for i in table.keys()) == set_of_upper_alpha
    assert set(table.values()) == set_of_upper_alpha


def test_translation_table_make_str_keys_outputs_correctly(
    text_with_mantra_trans_table: TranslationTable,
    text_with_mantra_trans_table_str_key: TranslationTableStrKey,
) -> None:
    trans_table_str_key = translation_table_make_str_keys(
        translation_table=text_with_mantra_trans_table
    )
    assert trans_table_str_key == text_with_mantra_trans_table_str_key


def test_cesaer_cipher_amt_24_outputs_correctly(
    text_with_mantra: str, text_with_mantra_casaer_cipher_amt_24: str
) -> None:
    SHIFT_AMOUNT = 24
    ciphertext = cesaer_cipher(text=text_with_mantra, shift_amount=SHIFT_AMOUNT)
    assert ciphertext == text_with_mantra_casaer_cipher_amt_24
