import HAWC_Tools  
import pandas as pd


HAWC_Vocab = pd.read_excel("HAWC_Ontologies_14November2019.xlsx", sheet_name="Endpoints", usecols="A:C")
apikey_sk = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

HAWC_Vocab['endpoint-name-flipped'] = HAWC_Vocab['endpoint-name'].apply(HAWC_Tools.flipOnComma)


#TIER 1
tuis_1 = ["T053","T054","T055","T017","T018","T021","T022","T023","T024","T025","T026","T029","T030","T031","T109","T114","T116","T121","T123","T125","T126","T127","T129","T131","T192","T196","T079","T080","T081","T082","T102","T169","T185","T034","T038","T032","T039","T040","T041","T042","T043","T044","T045","T201","T019","T020","T033","T037","T046","T047","T048","T049","T050","T184","T190","T191"]
linker, nlp = HAWC_Tools.loadUMLSLinker(999, .98)
HAWC_Vocab["endpoint-name_Tier1"], HAWC_Vocab["endpoint-name_Tier1-Count"]  = zip(*HAWC_Vocab['endpoint-name-flipped'].apply(HAWC_Tools.breakIntoSpansAndUMLS, tuiFilter = tuis_1, RequireNonObsoleteDef=True, nlp=nlp, linker=linker))
print("Tier 1 Done")
HAWC_Vocab.to_csv("Tier1.csv")

#TIER 2
tuis_2 = ["T053","T054","T055","T017","T018","T021","T022","T023","T024","T025","T026","T029","T030","T031","T109","T114","T116","T121","T123","T125","T126","T127","T129","T131","T192","T196","T079","T080","T081","T082","T102","T169","T185","T034","T038","T032","T039","T040","T041","T042","T043","T044","T045","T201","T019","T020","T033","T037","T046","T047","T048","T049","T050","T184","T190","T191"]
linker, nlp = HAWC_Tools.loadUMLSLinker(999, .85)
HAWC_Vocab["endpoint-name_Tier2"], HAWC_Vocab["endpoint-name_Tier2-Count"]  = zip(*HAWC_Vocab['endpoint-name-flipped'].apply(HAWC_Tools.breakIntoSpansAndUMLS, tuiFilter = tuis_2, nlp=nlp , linker=linker))
print("Tier 2 Done")
HAWC_Vocab.to_csv("Tier2.csv")

#TIER 3
tuis_3 = ["T059","T053","T054","T055","T017","T018","T021","T022","T023","T024","T025","T026","T029","T030","T031","T109","T114","T116","T121","T123","T125","T126","T127","T129","T131","T192","T196","T079","T080","T081","T082","T102","T169","T185","T034","T038","T032","T039","T040","T041","T042","T043","T044","T045","T201","T019","T020","T033","T037","T046","T047","T048","T049","T050","T184","T190","T191"]
linker, nlp = HAWC_Tools.loadUMLSLinker(999, .5)
HAWC_Vocab["endpoint-name_Tier3"], HAWC_Vocab["endpoint-name_Tier3-Count"]  = zip(*HAWC_Vocab['endpoint-name-flipped'].apply(HAWC_Tools.breakIntoSpansAndUMLS, tuiFilter = tuis_3, nlp=nlp , linker=linker))
print("Tier 3 Done")
HAWC_Vocab.to_csv("Tier3.csv")

#TIER 4
tuis_4 = []
linker, nlp = HAWC_Tools.loadUMLSLinker(999, .5)
HAWC_Vocab["endpoint-name_Tier4"], HAWC_Vocab["endpoint-name_Tier4-Count"]  = zip(*HAWC_Vocab['endpoint-name-flipped'].apply(HAWC_Tools.breakIntoSpansAndUMLS, tuiFilter = tuis_4, nlp=nlp , linker=linker))
print("Tier 4 Done")
HAWC_Vocab.to_csv("Tier4.csv")

#TIER 5
HAWC_Vocab["endpoint-name_Tier5_REST"] = HAWC_Vocab['endpoint-name-flipped'].apply(HAWC_Tools.UMLS_RestLookup, apikey = apikey_sk )
HAWC_Vocab["endpoint-name_Tier5_REST_CLEANED"] = HAWC_Vocab["endpoint-name_Tier5_REST"].apply(HAWC_Tools.REST_JSON_to_Read)
HAWC_Vocab.to_csv("Tier5_REST.csv")

#TIER 6
tuis_6 = ["T053","T054","T055","T017","T018","T021","T022","T023","T024","T025","T026","T029","T030","T031","T109","T114","T116","T121","T123","T125","T126","T127","T129","T131","T192","T196","T079","T080","T081","T082","T102","T169","T185","T034","T038","T032","T039","T040","T041","T042","T043","T044","T045","T201","T019","T020","T033","T037","T046","T047","T048","T049","T050","T184","T190","T191"]
linker, nlp = HAWC_Tools.loadUMLSLinker(999, .85)
HAWC_Vocab["endpoint-name_Tier6_EntityBreaking"], HAWC_Vocab["endpoint-name_Tier6-Count"]  = zip(*HAWC_Vocab['endpoint-name-flipped'].apply(HAWC_Tools.breakIntoEntitiesAndUMLS, tuiFilter = tuis_6, nlp=nlp , linker=linker))
print("Tier 6 Done")
HAWC_Vocab.to_csv("Tier6_Ents.csv")

#Organs and Systems
tuis = ["T053","T054","T055","T017","T018","T021","T022","T023","T024","T025","T026","T029","T030","T031","T109","T114","T116","T121","T123","T125","T126","T127","T129","T131","T192","T196","T079","T080","T081","T082","T102","T169","T185","T034","T038","T032","T039","T040","T041","T042","T043","T044","T045","T201","T019","T020","T033","T037","T046","T047","T048","T049","T050","T184","T190","T191"]
linker, nlp = HAWC_Tools.loadUMLSLinker(999, .5)
HAWC_Vocab["endpoint-organ_UMLS"], HAWC_Vocab["endpoint-organ_UMLS_Count"]   = zip(*HAWC_Vocab['endpoint-organ'].apply(HAWC_Tools.breakIntoSpansAndUMLS, tuiFilter = tuis, nlp=nlp , linker=linker))
print("Organ Done")
HAWC_Vocab["endpoint-system_UMLS"], HAWC_Vocab["endpoint-system_UMLS_Count"]  = zip(*HAWC_Vocab['endpoint-system'].apply(HAWC_Tools.breakIntoSpansAndUMLS, tuiFilter = tuis, nlp=nlp , linker=linker))
print("System Done")

HAWC_Vocab.to_csv("Tiered_Approach_Results.csv")