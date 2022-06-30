-- FDB RESEARCH
--***********************

-- IF USING IN SQLITESTUDIO:
-- Install this function, named djb2 in the SQL Functions Editor (Fx icon) as Type: Scalar, Implementation Language: QtScript, leaving Inputs undefined:
-- Do not copy paste the /* */ lines
/*
    var str = arguments[0];
    var len = str.length;
    var h = 5381;
    for (var i = 0; i < len; i++) {
    h = h * 33 ^ str.charCodeAt(i);
    }
    return h >>> 0;
*/
-- Replace CALCULATED_HASH with:
--     djb2(replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)))
-- You can also replace CALCULATED_HASH with your own number instead.
-- Open with Ctrl+O or the Folder icon in SQL Editor
-- Make sure Configuration > SQL Queries > "Execute only the query under the cursor" is UNCHECKED
-- Replace the 2 strings below Original/New with your base and modded species
-- NOTES:
--    Incomplete names ARE supported e.g. 'Grey' -> 'Harbor' will rename GreySeal to HarborSeal
--    Do NOT use incomplete strings that are too short or generic e.g. Giant, Red, Nile, which all have multiple species matched.

CREATE TEMP TABLE IF NOT EXISTS Replacement(Original TEXT PRIMARY KEY, New TEXT);
INSERT OR IGNORE INTO Replacement	(Original,		New)
-- Replace the 2 strings below here
VALUES			('ORIGINAL_SPECIES',	'NEW_SPECIES');

/* This clears out everything except our base creature. */
DELETE FROM DiseasePackStatChanges;
DELETE FROM ResearchItemData WHERE ResearchCategory NOT LIKE '%VetLevel%';
DELETE FROM ResearchPackData WHERE AnimalType IS NULL;
DELETE FROM ResearchCategoryData WHERE ResearchCategory NOT LIKE '%VetLevel%';
DELETE FROM DiseaseData;
DELETE FROM BreedingPackStatChanges WHERE ResearchPack NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND ResearchPack NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM EducationPackStatChanges WHERE ResearchPack NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND ResearchPack NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ResearchItemData WHERE ResearchItem NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND ResearchItem NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ResearchPackData WHERE ResearchPack NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND ResearchPack NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalData WHERE AnimalSpecies NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalSpecies NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');

/* This creates our new creature modeled off the base creature in the master table for this FDB */
INSERT OR IGNORE INTO AnimalData (AnimalSpecies, AnimalType, NumberOfResearchLevels)
SELECT 
    replace(AnimalSpecies, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)),
    AnimalType,
    NumberOfResearchLevels
FROM AnimalData;

/* This updates all other tables to use your new species instead of the base creature */
UPDATE ResearchItemData SET
    ResearchItem = replace(ResearchItem, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)),
    ResearchItemID = ResearchItemID + CALCULATED_HASH,
    Icon = replace(Icon, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE ResearchPackData SET
    ResearchPack = replace(ResearchPack, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)),
    ResearchPackID = ResearchPackID + CALCULATED_HASH
WHERE AnimalType LIKE '%'||(SELECT Original FROM Replacement)||'%';
UPDATE ResearchPackData SET
    AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE BreedingPackStatChanges SET ResearchPack = replace(ResearchPack, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE EducationPackStatChanges SET ResearchPack = replace(ResearchPack, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));

/* This deletes the base animal from the master table */
DELETE FROM AnimalData WHERE AnimalSpecies LIKE ('%'||(SELECT Original FROM Replacement)||'%');

DROP TABLE Replacement;

VACUUM;
