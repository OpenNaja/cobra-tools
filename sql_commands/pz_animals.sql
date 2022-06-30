-- FDB Animals
--***********************

-- IF USING IN SQLITESTUDIO:
-- Open with Ctrl+O or the Folder icon in SQL Editor
-- Make sure Configuration > SQL Queries > "Execute only the query under the cursor" is UNCHECKED
-- Replace the 4 strings below Original/New/OriginalPrefab/NewPrefab with your base and modded species
-- NOTES:
--    Incomplete names ARE supported e.g. 'Grey' -> 'Harbor' will rename GreySeal to HarborSeal
--    Do NOT use incomplete strings that are too short or generic e.g. Giant, Red, Nile, which all have multiple species matched.

CREATE TEMP TABLE IF NOT EXISTS Replacement(Original TEXT PRIMARY KEY, New TEXT, OriginalPrefab TEXT, NewPrefab TEXT);
INSERT OR IGNORE INTO Replacement(Original,				New,				OriginalPrefab,				NewPrefab)
-- Replace the 4 strings below here, 2 for species name, 2 for prefabs which contain an underscore in base game e.g. GreySeal -> Grey_Seal.
VALUES                 ('ORIGINAL_SPECIES',				'NEW_SPECIES',			'ORIGINAL_PREFAB',				'NEW_PREFAB');

-- Support older FDB versions by creating missing tables
-- 1.7-1.9 Tables
CREATE TABLE IF NOT EXISTS AnimalBurrowsData (AnimalType TEXT PRIMARY KEY REFERENCES AnimalDefinitions (AnimalType) ON UPDATE CASCADE NOT NULL COLLATE NOCASE UNIQUE, BurrowType TEXT NOT NULL, BabiesWaitForMother BOOLEAN NOT NULL DEFAULT (0), AfterbirthDuration REAL NOT NULL, MaleEnterOverOffset REAL NOT NULL, MaleEnterUnderOffset REAL NOT NULL, MaleExitUnderOffset REAL NOT NULL, MaleExitOverOffset REAL NOT NULL, FemaleEnterOverOffset REAL NOT NULL, FemaleEnterUnderOffset REAL NOT NULL, FemaleExitUnderOffset REAL NOT NULL, FemaleExitOverOffset REAL NOT NULL, JuvenileEnterOverOffset REAL NOT NULL, JuvenileEnterUnderOffset REAL NOT NULL, JuvenileExitUnderOffset REAL NOT NULL, JuvenileExitOverOffset REAL NOT NULL);
CREATE TABLE IF NOT EXISTS EscapeSpecificBarrierData (AnimalType TEXT REFERENCES AnimalDefinitions (AnimalType) ON UPDATE CASCADE NOT NULL, BarrierType TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS WaterStations (WaterStationPrefabName TEXT NOT NULL UNIQUE CHECK (WaterStationPrefabName NOT LIKE '% ') PRIMARY KEY);
CREATE TABLE IF NOT EXISTS WaterStationSuitabilityBlacklist (AnimalType TEXT REFERENCES AnimalDefinitions (AnimalType) ON UPDATE CASCADE NOT NULL, WaterStationPrefabName TEXT NOT NULL REFERENCES WaterStations (WaterStationPrefabName) ON UPDATE CASCADE, CONSTRAINT "Animal and Feeding Station Combination are not Unique" UNIQUE (AnimalType COLLATE NOCASE, WaterStationPrefabName COLLATE NOCASE));
-- 1.10 Tables
CREATE TABLE IF NOT EXISTS AnimalSingingData (AnimalType TEXT COLLATE NOCASE REFERENCES AnimalDefinitions (AnimalType) ON UPDATE CASCADE, MinCallsPerChorus INTEGER NOT NULL, MaxCallsPerChorus INTEGER NOT NULL, ProbabilityOfPartialCall DOUBLE NOT NULL DEFAULT (0.0), MinTimeBetweenCalls DOUBLE NOT NULL DEFAULT (0.0), MaxTimeBetweenCalls DOUBLE NOT NULL DEFAULT (0.0), PartialCallVariants INTEGER NOT NULL DEFAULT (0), PartialCallAndReplyStart DOUBLE DEFAULT (0.5) NOT NULL, PartialCallAndReplyDuration INTEGER NOT NULL DEFAULT (1), ForceInstantTransitionIdle INTEGER NOT NULL DEFAULT (0));
CREATE TABLE IF NOT EXISTS AnimalSingingPartialWeights (AnimalType TEXT REFERENCES AnimalDefinitions (AnimalType) ON UPDATE CASCADE NOT NULL COLLATE NOCASE, PartialName TEXT NOT NULL, PartialWeighting DOUBLE NOT NULL);
CREATE TABLE IF NOT EXISTS SpeciesSniffWeighting (AnimalType TEXT REFERENCES AnimalDefinitions (AnimalType) ON UPDATE CASCADE, SniffWeighting DOUBLE NOT NULL CHECK (SniffWeighting >= 0 AND SniffWeighting <= 1.0) DEFAULT (0.5));

/* This clears out everything except our base creature */
DELETE FROM ActionCalculationParameters WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalBiomePreferences WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalBurrowsData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalCameraData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalDiggingData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalContinentPreferences WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalEnrichmentItemSuitability WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalExchangeData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalFoodPreferences WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalHabitatRequirements WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalInterestRating WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ActionCalculationParameters WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalNameLanguages WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalPurchaseCosts WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalsReadyToBePlacedInGame WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalSingingData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%'); -- 1.10
DELETE FROM AnimalSingingPartialWeights WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%'); -- 1.10
DELETE FROM AnimalTaxonomicFamilies WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalTalkParticipantData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalTerrainRequirements WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalTestData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AnimalTheatreParameters WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM BeddingStationSuitability WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM BodyMass WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM BoxData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM CheatVariables WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ColourMorphData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM DeepSwimmingBehaviourWeights WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM DeepSwimmingParameters WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM DefecationData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM DesiredGenderRatios WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM DesiredPopulationSizes WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM EnrichmentOffsets WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM EnrichmentRequirements WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM EscapeData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM EscapeSpecificBarrierData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM FeedingStationSuitability WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM FertilityData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM FightAgeThresholds WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM GuestAnimalDesire WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM GuestStance WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM IdleBehaviourWeights WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM InterspeciesInteractionData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM LongevityData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM LocomotionSpeeds WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM MatingPairingRules WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM NavigationWorlds WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM FixRagdollMethodData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM NutritionData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM Offsets WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM PerformableAnimations WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM PersonalityWeights WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SizeData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SleepVariables WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SocialBehaviourSettings WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM PounceVariablesData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SocialInteractionsParameters WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpaceRequirements WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpeciesDiseaseValues WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpeciesEnum WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpeciesIdleExploreTypeWeights WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpeciesSniffWeighting WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%'); -- 1.10
DELETE FROM SpeciesSpecificNeedModifiers WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpeciesThatFight WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SpeciesWithAlpha WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM StressParameters WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM TheatreClearRadii WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM ViewingDistanceModifier WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM VisualVariation WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM EnrichmentPartialTypesToUse WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM AudioPerActionCallData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%'); 
DELETE FROM PounceVariablesData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%'); 
DELETE FROM TemporaryFoodVisualOffsetModifier WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM WaterStationSuitabilityBlacklist WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM SocialEnrichmentData;
DELETE FROM AnimalDefinitions WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');

/* This creates our new creature modeled off the base creature in the master table for this FDB */
INSERT OR IGNORE INTO AnimalDefinitions (AnimalType,AdultMaleGamePrefab,AdultMaleVisualPrefab,AdultFemaleGamePrefab,AdultFemaleVisualPrefab,JuvenileGamePrefab,JuvenileVisualPrefab,ContentPack)
SELECT
    replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)),
    replace(AdultMaleGamePrefab, (SELECT OriginalPrefab FROM Replacement), (SELECT NewPrefab FROM Replacement)),
    replace(AdultMaleVisualPrefab, (SELECT OriginalPrefab FROM Replacement), (SELECT NewPrefab FROM Replacement)),
    replace(AdultFemaleGamePrefab, (SELECT OriginalPrefab FROM Replacement), (SELECT NewPrefab FROM Replacement)),
    replace(AdultFemaleVisualPrefab, (SELECT OriginalPrefab FROM Replacement), (SELECT NewPrefab FROM Replacement)),
    replace(JuvenileGamePrefab, (SELECT OriginalPrefab FROM Replacement), (SELECT NewPrefab FROM Replacement)),
    replace(JuvenileVisualPrefab, (SELECT OriginalPrefab FROM Replacement), (SELECT NewPrefab FROM Replacement)),
    ContentPack
FROM AnimalDefinitions;

/* This updates all other tables to use your new species instead of the base creature */
UPDATE ActionCalculationParameters SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalBiomePreferences SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalCameraData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalContinentPreferences SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalEnrichmentItemSuitability SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalExchangeData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalFoodPreferences SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalHabitatRequirements SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalInterestRating SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE ActionCalculationParameters SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalNameLanguages SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalPurchaseCosts SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalsReadyToBePlacedInGame SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalSingingData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)); -- 1.10
UPDATE AnimalSingingPartialWeights SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)); -- 1.10
UPDATE AnimalTaxonomicFamilies SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalTalkParticipantData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalTerrainRequirements SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalTestData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalTheatreParameters SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE BeddingStationSuitability SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE BodyMass SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE BoxData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE CheatVariables SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE ColourMorphData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE DeepSwimmingBehaviourWeights SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE DeepSwimmingParameters SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE DefecationData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE DesiredGenderRatios SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE DesiredPopulationSizes SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE EnrichmentOffsets SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE EnrichmentRequirements SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE EscapeData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE FeedingStationSuitability SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE FertilityData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE FightAgeThresholds SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE GuestAnimalDesire SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE GuestStance SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE IdleBehaviourWeights SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE InterspeciesInteractionData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE LongevityData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE LocomotionSpeeds SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE MatingPairingRules SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE NavigationWorlds SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE NutritionData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE Offsets SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE PerformableAnimations SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE SizeData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE SleepVariables SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE SocialBehaviourSettings SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE PounceVariablesData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE SocialInteractionsParameters SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE SpaceRequirements SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE SpeciesDiseaseValues SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE SpeciesEnum SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AnimalsReadyToBePlacedInGame SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE SpeciesIdleExploreTypeWeights SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE SpeciesSniffWeighting SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)); -- 1.10
UPDATE SpeciesSpecificNeedModifiers SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE SpeciesThatFight SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE SpeciesWithAlpha SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE StressParameters SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE TheatreClearRadii SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE ViewingDistanceModifier SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE VisualVariation SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE EnrichmentPartialTypesToUse SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE FixRagdollMethodData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));
UPDATE AudioPerActionCallData SET AnimalType = replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement)) WHERE AnimalType is not null;

/* This clears out the base creature. */
DELETE FROM AnimalDefinitions WHERE AnimalType NOT LIKE replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));

DROP TABLE Replacement;

VACUUM;
