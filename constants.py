MIL_TRANS = [
    "C130", "C30J", "C17", "A400", "C5", "C390", "CN35", "C295", "AN12", "AN22", "AN24", "AN26",
    "AN30", "AN32", "AN72", "AN74", "AN124", "IL76", "IL18", "C27J", "C212", "CL60", "L100", "C160"
]

MIL_TANKER = ["K35R", "A332", "KC10", "K135", "KC130", "IL78", "V10"]

MIL_COMBAT = [
    "F15", "F16", "F18", "F22", "F35", "EUFI", "TORN", "RAFY", "M2K", "F4", "F5", "A10",
    "SU24", "SU25", "SU27", "SU30", "SU34", "SU35", "SU57", "MIG21", "MIG23", "MIG25", "MIG29", "MIG31",
    "B1", "B2", "B52", "TU95", "TU160", "TU22", "H6", "J10", "J11", "J15", "J16", "J20"
]

MIL_ISR = [
    "E3TF", "E3CF", "E6", "E8", "R135", "P8", "P3", "C135", "E2", "FA50", "GLF4", "GLF5",
    "GLEX", "B350", "B200", "BE20", "C208", "PC12", "F2TH", "F900", "L39", "L159", "M346"
]

MIL_VIP = [
    "A310", "A319", "A320", "A321", "A343", "A359", "B737", "B738", "B739", "B742", "B744",
    "B748", "B752", "B762", "B763", "B772", "B788", "B789", "IL62", "IL96", "TU134", "TU154", "TU204", "TU214"
]

MIL_HELO = [
    "H60", "H47", "WA64", "EH10", "NH90", "H53", "AS32", "EC35", "B06", "UH1", "MI8", "MI17", "MI24", "MI26", "MI28", "KA50", "KA52"
]

MIL_UAV = ["MQ9", "RQ4", "GLO6", "Q4", "HERO"]

TARGET_TYPES = MIL_TRANS + MIL_TANKER + MIL_COMBAT + MIL_ISR + MIL_VIP + MIL_HELO + MIL_UAV

KNOWN_ICAO_HEX: set[str] = {
    # E-6B Mercury
    "ae040d", "ae040e", "ae040f", "ae0410", "ae0411", "ae0412",
    "ae0413", "ae0414", "ae0415", "ae0416", "ae0417", "ae0418",
    "ae0419", "ae041a", "ae041b", "ae041c",
    # E-4B Nightwatch
    "adfeb7", "adfeb8", "adfeb9", "adfeba",
    # VC-25A
    "adfdf8", "adfdf9", "adfeb2", "adfeb3",
    # C-32A
    "ae01e6", "ae01e7", "ae0201", "ae0202",
    "ae4ae8", "ae4ae9", "ae4aea", "ae4aeb",
    # RC-135 Rivet Joint
    "ae01c5", "ae01c6", "ae01c7", "ae01c8", "ae01cb",
    "ae01cd", "ae01ce", "ae01d1", "ae01d2", "ae01d3",
    "ae01d4", "ae01d5",
    # E-3 Sentry
    "ae11e3", "ae11e4", "ae11e5", "ae11e6", "ae11e7", "ae11e8",
    # RQ-4 Global Hawk
    "ae5414", "ae54b6", "ae7813",
    # U-2 Dragon Lady
    "ae094d", "ae0950", "ae0955",
    # B-52 Stratofortress
    "ae586c", "ae586d", "ae586e", "ae5871", "ae5872", "ae5873",
    "ae5874", "ae5881", "ae5889", "ae588a", "ae5893", "ae5897",
    "ae58a2", "ae58a3",
    # B-1B Lancer
    "ae04a9", "ae04aa", "ae04ab", "ae04ac",
}

SPECIAL_TARGETS: dict[str, str] = {
    "adfdf8": "🇺🇸 AIR FORCE ONE",
    "adfdf9": "🇺🇸 AIR FORCE ONE",
    "adfeb2": "🇺🇸 AIR FORCE ONE",
    "adfeb3": "🇺🇸 AIR FORCE ONE",
    "ae01e6": "🇺🇸 AIR FORCE TWO",
    "ae01e7": "🇺🇸 AIR FORCE TWO",
    "ae0201": "🇺🇸 AIR FORCE TWO",
    "ae0202": "🇺🇸 AIR FORCE TWO",
    "ae4ae8": "🇺🇸 AIR FORCE TWO",
    "ae4ae9": "🇺🇸 AIR FORCE TWO",
    "ae4aea": "🇺🇸 AIR FORCE TWO",
    "ae4aeb": "🇺🇸 AIR FORCE TWO",
}