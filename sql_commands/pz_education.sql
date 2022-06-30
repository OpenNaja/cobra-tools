-- FDB EDUCATION
--***********************

-- IF USING IN SQLITESTUDIO:
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
DELETE FROM InfoBoardMaterials WHERE ContentType NOT LIKE '%'||(SELECT Original FROM Replacement)||'%' AND ContentType NOT LIKE '%'||(SELECT New FROM Replacement)||'%';
DELETE FROM EducationResearchPacks WHERE ContentType NOT LIKE '%'||(SELECT Original FROM Replacement)||'%' AND ContentType NOT LIKE '%'||(SELECT New FROM Replacement)||'%';
DELETE FROM EducationalContentTypes WHERE Name NOT LIKE '%'||(SELECT Original FROM Replacement)||'%' AND Name NOT LIKE '%'||(SELECT New FROM Replacement)||'%';
DELETE FROM AssetPackageOverrides;
DELETE FROM PrefabNamesToEducationSourceTypes;
DELETE FROM EducationSourceTypes;
DELETE FROM Tweakables;

/* This creates our new creature modeled off the base creature in the master table for this FDB */
INSERT OR IGNORE INTO EducationalContentTypes
SELECT
    replace(Name, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)),
    Category,
    replace(LocString, (SELECT Original FROM Replacement), (SELECT New FROM Replacement))
    FROM EducationalContentTypes;
UPDATE EducationResearchPacks SET
    ContentType = replace(ContentType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)),
    Unlock1PackName = replace(Unlock1PackName, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)),
    Unlock2PackName = replace(Unlock2PackName, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)),
    Unlock3PackName = replace(Unlock3PackName, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE InfoBoardMaterials SET
    ContentType = replace(ContentType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)),
    MaterialName = replace(MaterialName, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));

/* This deletes the base animal from the master table */
DELETE FROM InfoBoardMaterials WHERE ContentType LIKE '%'||(SELECT Original FROM Replacement)||'%';
DELETE FROM EducationResearchPacks WHERE ContentType LIKE '%'||(SELECT Original FROM Replacement)||'%';
DELETE FROM EducationalContentTypes WHERE Name like '%'||(SELECT Original FROM Replacement)||'%';

DROP TABLE Replacement;

VACUUM;
