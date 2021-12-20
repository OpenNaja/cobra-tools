/*Copy the whole script below into SQLite’s SQL Editor; change ORIGINAL, NEW, and ORIGINAL into your original animal, its replacement, and the length of the animal’s name. USE THE FULL NAME OF THE ANIMAL even if you’re only replacing part of it. IE CuviersDwarfCaiman into NilecrcDwarfCaiman - I’d enter both full names, not only the part that changes*/

CREATE TEMP TABLE Replacement(Original TEXT PRIMARY KEY, New TEXT, Length INTEGER);

Insert Into Replacement(Original,New,Length) Values ('ORIGINAL','NEW',length('ORIGINAL'));

/*This clears out everything except our base creature.*/

delete from ActionCalculationParameters where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalBiomePreferences where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalCameraData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalContinentPreferences where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalEnrichmentItemSuitability where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalExchangeData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalFoodPreferences where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalHabitatRequirements where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalInterestRating where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from ActionCalculationParameters where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalNameLanguages where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalPurchaseCosts where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalsReadyToBePlacedInGame where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalTaxonomicFamilies where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalTalkParticipantData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalTerrainRequirements where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalTestData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from AnimalTheatreParameters where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from BeddingStationSuitability where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from BodyMass where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from BoxData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from CheatVariables where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from ColourMorphData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from DeepSwimmingBehaviourWeights where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from DeepSwimmingParameters where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from DefecationData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from DesiredGenderRatios where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from DesiredPopulationSizes where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from EnrichmentOffsets where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from EnrichmentRequirements where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from EscapeData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from FeedingStationSuitability where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from FertilityData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from FightAgeThresholds where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from GuestAnimalDesire where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from GuestStance where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from IdleBehaviourWeights where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from InterspeciesInteractionData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from LongevityData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from LocomotionSpeeds where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from MatingPairingRules where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from NavigationWorlds where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from NutritionData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from Offsets where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from PerformableAnimations where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from SizeData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from SleepVariables where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from SocialBehaviourSettings where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from SocialInteractionsParameters where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from SpaceRequirements where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from SpeciesDiseaseValues where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from SpeciesEnum where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from SpeciesIdleExploreTypeWeights where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from SpeciesSpecificNeedModifiers where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from SpeciesThatFight where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from SpeciesWithAlpha where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from StressParameters where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from TheatreClearRadii where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from ViewingDistanceModifier where AnimalType not like('%'||(select Original from Replacement)||'%');
delete from VisualVariation where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from EnrichmentPartialTypesToUse where AnimalType not like ('%'||(select Original from Replacement)||'%');
Delete from AudioPerActionCallData where ifnull(AnimalType,(select original from replacement)) not like ('%'||(select Original from Replacement)||'%');
delete from FixRagdollMethodData where AnimalType not like ('%'||(select Original from Replacement)||'%');
delete from PounceVariablesData where AnimalType not like ('%'||(select Original from Replacement)||'%');
/*unfinished*/
/*Delete * from SocialEnrichmentData;*/

delete from AnimalDefinitions where AnimalType not like ('%'||(select Original from Replacement)||'%');



/*This creates our new creature modeled off the base creature in the master table for this FDB*/
Insert into AnimalDefinitions (AnimalType,AdultMaleGamePrefab,AdultMaleVisualPrefab,AdultFemaleGamePrefab,AdultFemaleVisualPrefab,JuvenileGamePrefab,JuvenileVisualPrefab,ContentPack) select (((select New from Replacement))||(substr(AnimalType,(select length+1 from Replacement)))),(((select New from Replacement))||(substr(AdultMaleGamePrefab,(select length+1 from Replacement)))),(((select New from Replacement))||(substr(AdultMaleVisualPrefab,(select length+1 from Replacement)))),(((select New from Replacement))||(substr(AdultFemaleGamePrefab,(select length+1 from Replacement)))),(((select New from Replacement))||(substr(AdultFemaleVisualPrefab,(select length+1 from Replacement)))),(((select New from Replacement))||(substr(JuvenileGamePrefab,(select length+1 from Replacement)))),(((select New from Replacement))||(substr(JuvenileVisualPrefab,(select length+1 from Replacement)))),ContentPack from AnimalDefinitions;


/*This updates all other tables to use your new species instead of the base creature*/
Update ActionCalculationParameters set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalBiomePreferences set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalCameraData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalContinentPreferences set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalEnrichmentItemSuitability set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalExchangeData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalFoodPreferences set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalHabitatRequirements set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalInterestRating set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update ActionCalculationParameters set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalNameLanguages set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalPurchaseCosts set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalsReadyToBePlacedInGame set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalTaxonomicFamilies set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalTalkParticipantData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalTerrainRequirements set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalTestData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalTheatreParameters set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update BeddingStationSuitability set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update BodyMass set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update BoxData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update CheatVariables set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update ColourMorphData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update DeepSwimmingBehaviourWeights set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update DeepSwimmingParameters set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update DefecationData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update DesiredGenderRatios set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update DesiredPopulationSizes set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update EnrichmentOffsets set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update EnrichmentRequirements set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update EscapeData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update FeedingStationSuitability set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update FertilityData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update FightAgeThresholds set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update GuestAnimalDesire set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update GuestStance set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update IdleBehaviourWeights set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update InterspeciesInteractionData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update LongevityData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update LocomotionSpeeds set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update MatingPairingRules set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update NavigationWorlds set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update NutritionData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update Offsets set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update PerformableAnimations set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update SizeData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update SleepVariables set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update SocialBehaviourSettings set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update SocialInteractionsParameters set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update SpaceRequirements set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update SpeciesDiseaseValues set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update SpeciesEnum set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AnimalsReadyToBePlacedInGame set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update SpeciesIdleExploreTypeWeights set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update SpeciesSpecificNeedModifiers set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update SpeciesThatFight set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update SpeciesWithAlpha set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update StressParameters set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update TheatreClearRadii set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update ViewingDistanceModifier set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update VisualVariation set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update EnrichmentPartialTypesToUse set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update FixRagdollMethodData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement))));
Update AudioPerActionCallData set AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from replacement)))) where AnimalType is not null;


/*This clears out everything except our base creature.*/
delete from AnimalDefinitions where AnimalType not like (select New from Replacement);
