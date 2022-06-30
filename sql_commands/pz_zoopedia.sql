-- FDB Zoopedia
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
DELETE FROM BarrierRequirements WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpeciesFunFactsUnitData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpeciesAverageStats WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpeciesZoopediaData WHERE Species NOT LIKE('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpeciesFunFacts WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpeciesZoopediaUnitData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM Species WHERE InternalName NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND InternalName NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');

/* This creates our new creature modeled off the base creature in the master table for this FDB */
INSERT OR IGNORE INTO Species(InternalName,EnclosureType,ContentPack)
SELECT replace(s.InternalName, r.Original, r.New), s.EnclosureType, s.ContentPack
FROM Replacement r, Species s WHERE r.Original = s.InternalName;

/* This updates all other tables to use your new species instead of the base creature */
UPDATE BarrierRequirements SET Species = (SELECT New FROM Replacement);
UPDATE SpeciesAverageStats SET Species = (SELECT New FROM Replacement);
UPDATE SpeciesZoopediaData SET Species = (SELECT New FROM Replacement);

INSERT OR IGNORE INTO SpeciesFunFacts (Species,FunFact,ResearchPackName)
SELECT (SELECT Original FROM Replacement),'dummy','dummy'
WHERE EXISTS (SELECT * FROM Species WHERE InternalName LIKE '%'||(SELECT Original FROM Replacement)||'%');

UPDATE SpeciesFunFactsUnitData SET FunFact = 'dummy'
WHERE EXISTS (SELECT * FROM Species WHERE InternalName LIKE '%'||(SELECT Original FROM Replacement)||'%');

UPDATE SpeciesFunFacts SET
    Species = (SELECT new FROM Replacement),
    FunFact = replace(FunFact, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)),
    ResearchPackName = replace(ResearchPackName, (SELECT Original FROM Replacement), (SELECT New FROM Replacement))
WHERE FunFact != 'dummy';

UPDATE SpeciesFunFactsUnitData SET 
    Species = (SELECT New FROM Replacement),
    FunFact = (SELECT FunFact FROM SpeciesFunFacts);
DELETE FROM SpeciesFunFacts WHERE FunFact = 'dummy';

UPDATE SpeciesZoopediaUnitData SET Species = (SELECT New FROM Replacement);

/* This deletes the base animal from the master table */
DELETE FROM Species WHERE InternalName NOT LIKE '%'||(SELECT New FROM Replacement)||'%';

DROP TABLE Replacement;

VACUUM;
