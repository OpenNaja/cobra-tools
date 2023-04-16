-- FDB Animals
--***********************

-- IF USING IN SQLITESTUDIO:
-- Open with Ctrl+O or the Folder icon in SQL Editor
-- Make sure Configuration > SQL Queries > "Execute only the query under the cursor" is UNCHECKED
-- Replace the 2 strings below Original/New with your base and modded species
-- NOTES:
--    Incomplete names ARE supported e.g. 'Grey' -> 'Harbor' will rename GreySeal to HarborSeal
--    Do NOT use incomplete strings that are too short or generic e.g. Giant, Red, Nile, which all have multiple species matched.

CREATE TEMP TABLE IF NOT EXISTS Replacement(Original TEXT PRIMARY KEY, New TEXT);
INSERT OR IGNORE INTO Replacement(Original,				New)
-- Replace the 2 strings below here.
VALUES                 ('ORIGINAL_SPECIES',				'NEW_SPECIES');

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
-- 1.11 Tables
CREATE TABLE IF NOT EXISTS IdleBehaviourWeights (AnimalType TEXT NOT NULL REFERENCES AnimalDefinitions (AnimalType) ON UPDATE CASCADE COLLATE NOCASE, AgeGroup TEXT REFERENCES AgeEnum (Age) ON UPDATE CASCADE COLLATE NOCASE, Gender TEXT REFERENCES Genders (Gender) ON UPDATE CASCADE COLLATE NOCASE, SnowExclusive BOOLEAN DEFAULT (0) NOT NULL, IdleActionType TEXT REFERENCES IdleActionTypes (IdleActionType) ON UPDATE CASCADE COLLATE NOCASE NOT NULL, ActionWeightOnLand DOUBLE NOT NULL CONSTRAINT "ActionWeightOnLand out of bounds" CHECK (ActionWeightOnLand <= 1 AND ActionWeightOnLand >= 0), ActionWeightInWater DOUBLE NOT NULL CONSTRAINT "ActionWeightInWater out of bounds" CHECK (ActionWeightInWater <= 1 AND ActionWeightInWater >= 0), ActionWeightClimbing DOUBLE NOT NULL CONSTRAINT "ActionWeightClimbing out of bounds" CHECK (ActionWeightClimbing <= 1 AND ActionWeightClimbing >= 0), ActionWeightWading DOUBLE NOT NULL DEFAULT (0.0) CONSTRAINT "ActionWeightWading out of bounds" CHECK (ActionWeightWading <= 1 AND ActionWeightWading >= 0), ActionWeightDeepSwim DOUBLE CHECK (ActionWeightDeepSwim >= 0 AND ActionWeightDeepSwim <= 1) NOT NULL DEFAULT (0.0), ActionWeightAnimalTalk DOUBLE DEFAULT (0.0) NOT NULL CHECK (ActionWeightAnimalTalk <= 1 AND ActionWeightAnimalTalk >= 0), ActionWeightInBurrow DOUBLE NOT NULL CHECK (ActionWeightInBurrow <= 1 AND ActionWeightInBurrow >= 0) DEFAULT (0.0), ActionWeightEscaped DOUBLE NOT NULL DEFAULT (0.0) CHECK (ActionWeightEscaped <= 1 AND ActionWeightEscaped >= 0), InfluencingSpecies TEXT COLLATE NOCASE, InfluencingAge TEXT REFERENCES AgeEnum (Age) ON UPDATE CASCADE COLLATE NOCASE, InfluencingGender TEXT REFERENCES Genders (Gender) ON UPDATE CASCADE COLLATE NOCASE, InfluencingActionType TEXT REFERENCES IdleActionTypes (IdleActionType) ON UPDATE CASCADE COLLATE NOCASE, InfluencingRange DOUBLE);
-- 1.12 Tables
CREATE TABLE IF NOT EXISTS GimmickMovementData (Species TEXT PRIMARY KEY REFERENCES AnimalDefinitions (AnimalType) NOT NULL, TranslationX DOUBLE NOT NULL DEFAULT (0.0), TranslationY DOUBLE NOT NULL DEFAULT (0.0), TranslationZ DOUBLE NOT NULL DEFAULT (0.0));
-- 1.13 Tables
CREATE TABLE IF NOT EXISTS LakeSurfaceFollowerData (AnimalType STRING REFERENCES AnimalDefinitions (AnimalType) ON UPDATE CASCADE PRIMARY KEY UNIQUE NOT NULL COLLATE NOCASE, MaleSwimHeightOffset REAL DEFAULT (0), MaleWadeHeightOffset REAL DEFAULT (0), MaleUseWadeDepth BOOLEAN DEFAULT (0), MaleWadeDepth REAL DEFAULT (0), FemaleSwimHeightOffset REAL DEFAULT (0), FemaleWadeHeightOffset REAL DEFAULT (0), FemaleUseWadeDepth BOOLEAN DEFAULT (0), FemaleWadeDepth REAL DEFAULT (0), JuvenileSwimHeightOffset REAL DEFAULT (0), JuvenileWadeHeightOffset REAL DEFAULT (0), JuvenileUseWadeDepth BOOLEAN DEFAULT (0), JuvenileWadeDepth REAL DEFAULT (0));
CREATE TABLE IF NOT EXISTS MaturationEnum (MaturationType TEXT PRIMARY KEY UNIQUE NOT NULL, EnumValue INTEGER UNIQUE NOT NULL);
CREATE TABLE IF NOT EXISTS SocialityData (AnimalType TEXT PRIMARY KEY REFERENCES AnimalDefinitions (AnimalType) ON UPDATE CASCADE UNIQUE NOT NULL, GroupNameLoc TEXT NOT NULL DEFAULT Generic, MaturationType TEXT REFERENCES MaturationEnum (MaturationType) NOT NULL, RelationsDecayTimer DOUBLE NOT NULL DEFAULT (0.0), ChanceToBondOnSocialTheatre DOUBLE DEFAULT (0.0) NOT NULL);

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
DELETE FROM GimmickMovementData WHERE Species NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND Species NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM GuestAnimalDesire WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM GuestStance WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM IdleBehaviourWeights WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM InterspeciesInteractionData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
DELETE FROM LakeSurfaceFollowerData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
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
DELETE FROM SocialityData WHERE AnimalType NOT LIKE ('%'||(SELECT Original FROM Replacement)||'%') AND AnimalType NOT LIKE ('%'||(SELECT New FROM Replacement)||'%');
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
    AdultMaleGamePrefab,
    AdultMaleVisualPrefab,
    AdultFemaleGamePrefab,
    AdultFemaleVisualPrefab,
    JuvenileGamePrefab,
    JuvenileVisualPrefab,
    ContentPack
FROM AnimalDefinitions;

/* This updates all other tables to use your new species instead of the base creature */
UPDATE ActionCalculationParameters SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalBiomePreferences SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalBurrowsData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalCameraData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalContinentPreferences SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalDiggingData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalEnrichmentItemSuitability SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalExchangeData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalFoodPreferences SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalHabitatRequirements SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalInterestRating SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalNameLanguages SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalPurchaseCosts SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalsReadyToBePlacedInGame SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalSingingData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%'; -- 1.10
UPDATE AnimalSingingPartialWeights SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%'; -- 1.10
UPDATE AnimalTaxonomicFamilies SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalTalkParticipantData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalTerrainRequirements SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalTestData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AnimalTheatreParameters SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE BeddingStationSuitability SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE BodyMass SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE BoxData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE CheatVariables SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ColourMorphData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE DeepSwimmingBehaviourWeights SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE DeepSwimmingParameters SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE DefecationData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE DesiredGenderRatios SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE DesiredPopulationSizes SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE EnrichmentOffsets SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE EnrichmentRequirements SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE EscapeData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE EscapeSpecificBarrierData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE FeedingStationSuitability SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE FertilityData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE FightAgeThresholds SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE GimmickMovementData SET Species = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE Species LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE GuestAnimalDesire SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE GuestStance SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE IdleBehaviourWeights SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE InterspeciesInteractionData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE LakeSurfaceFollowerData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE LongevityData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE LocomotionSpeeds SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE MatingPairingRules SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE NavigationWorlds SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE NutritionData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE Offsets SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE PerformableAnimations SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE PersonalityWeights SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SizeData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SleepVariables SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SocialBehaviourSettings SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SocialityData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE PounceVariablesData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SocialInteractionsParameters SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SpaceRequirements SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SpeciesDiseaseValues SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SpeciesEnum SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SpeciesIdleExploreTypeWeights SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SpeciesSniffWeighting SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%'; -- 1.10
UPDATE SpeciesSpecificNeedModifiers SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SpeciesThatFight SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE SpeciesWithAlpha SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE StressParameters SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE TheatreClearRadii SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE ViewingDistanceModifier SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE VisualVariation SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE EnrichmentPartialTypesToUse SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE FixRagdollMethodData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE AudioPerActionCallData SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE TemporaryFoodVisualOffsetModifier SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';
UPDATE WaterStationSuitabilityBlacklist SET AnimalType = (SELECT AnimalType FROM AnimalDefinitions WHERE AnimalType LIKE '%'||(SELECT New FROM Replacement)||'%') WHERE AnimalType LIKE '%'|| (SELECT Original FROM Replacement) ||'%';

/* This clears out the base creature. */
DELETE FROM AnimalDefinitions WHERE AnimalType NOT LIKE replace(AnimalType, (SELECT Original FROM Replacement), (SELECT New FROM Replacement));

DROP TABLE Replacement;

VACUUM;
