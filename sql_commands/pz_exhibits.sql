-- FDB Exhibits
--***********************

-- IF USING IN SQLITESTUDIO:
-- Open with Ctrl+O or the Folder icon in SQL Editor
-- Make sure Configuration > SQL Queries > "Execute only the query under the cursor" is UNCHECKED
-- Replace the 2 strings below Original/New with your base and modded species
-- NOTES:
--    Incomplete names ARE supported e.g. 'Grey' -> 'Harbor' will rename GreySeal to HarborSeal
--    Do NOT use incomplete strings that are too short or generic e.g. Giant, Red, Nile, which all have multiple species matched.
--    Due to the exhibit extra info per species, in this version of the script you have to manually fix the 
--      ExhibitBanis, ExhibitAnimalPoses and ExhibitAnimalPresentationData tables.


CREATE TEMP TABLE IF NOT EXISTS Replacement(Original TEXT PRIMARY KEY, New TEXT);
INSERT OR IGNORE INTO Replacement(Original,				New)
-- Replace the 2 strings below here.
VALUES                 ('ORIGINAL_SPECIES',				'NEW_SPECIES');

-- Support older FDB versions by creating missing tables


/* This clears out everything except our base creature */
DELETE FROM ExhibitAnimalBiomePreferences WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalCameraData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalColourMorphData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalContinentPreferences WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalDefecationData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalExchangeData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalHumidityData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalInterestRating WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalLerping WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalLongevityData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalMatingData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalNameLanguages WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalNutritionData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalPopulationData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalPresentationData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalPoses WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalSizeData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalTemperatureData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalUIData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalWeightData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitBackdropPrefabs WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitBases WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitEnrichmentLevelNames WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitEnrichmentResearchPacks WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitEnrichments WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitInterspeciesData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitLightingRigs WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM GuestExhibitAnimalDesire WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ExhibitAnimalDefinitions WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');

/* This creates our new creature modeled off the base creature in the master table for this FDB */
INSERT OR IGNORE INTO ExhibitAnimalDefinitions (Species,GamePrefab,VisualPrefab,FemaleVisualPrefab,ContentPack,ExhibitType)
SELECT
    replace(Species, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)),
    GamePrefab,
    VisualPrefab,
    FemaleVisualPrefab,
    ContentPack,
    ExhibitType
FROM ExhibitAnimalDefinitions;

/* This updates all other tables to use your new species instead of the base creature */

UPDATE ExhibitAnimalBiomePreferences SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalCameraData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalColourMorphData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalContinentPreferences SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalDefecationData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalExchangeData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalHumidityData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalInterestRating SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalLerping SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalLongevityData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalMatingData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalNameLanguages SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalNutritionData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalPopulationData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalPresentationData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalPoses SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalSizeData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalTemperatureData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalUIData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitAnimalWeightData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitBackdropPrefabs SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitBases SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitEnrichmentLevelNames SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitEnrichmentResearchPacks SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitEnrichments SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitInterspeciesData SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ExhibitLightingRigs SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE GuestExhibitAnimalDesire SET Species = (SELECT Species FROM ExhibitAnimalDefinitions WHERE Species LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';

/* This clears out the base creature. */
DELETE FROM ExhibitAnimalDefinitions WHERE Species NOT LIKE replace(Species, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));

DROP TABLE Replacement;

VACUUM;
