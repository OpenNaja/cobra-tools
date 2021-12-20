/*Copy the whole script below into SQLite’s SQL Editor; change ORIGINAL, NEW, and ORIGINAL into your original animal, its replacement, and the length of the animal’s name. USE THE FULL NAME OF THE ANIMAL even if you’re only replacing part of it. IE CuviersDwarfCaiman into NilecrcDwarfCaiman - I’d enter both full names, not only the part that changes*/

CREATE TEMP TABLE Replacement(Original TEXT PRIMARY KEY, New TEXT, Length INTEGER);

Insert Into Replacement(Original,New,Length) Values ('ORIGINAL','NEW',length('ORIGINAL'));

/*This clears out everything except our base creature.*/
delete from BreedingPackStatChanges where ResearchPack not like ('%'||(select Original from Replacement)||'%');
delete from EducationPackStatChanges where ResearchPack not like ('%'||(select Original from Replacement)||'%');
delete from ResearchItemData where ResearchItem not like ('%'||(select Original from Replacement)||'%');
delete from ResearchPackData where ResearchPack not like ('%'||(select Original from Replacement)||'%');
delete from AnimalData where AnimalSpecies not like ('%'||(select Original from Replacement)||'%');

/*This creates our new creature modeled off the base creature in the master table for this FDB*/
Insert into AnimalData (AnimalSpecies,AnimalType,NumberOfResearchLevels) select ((select New from Replacement)||(substr(AnimalSpecies,(Select Length+1 from Replacement)))),AnimalType,NumberOfResearchLevels from AnimalData;

/*This updates all other tables to use your new species instead of the base creature*/
Update ResearchItemData set ResearchItem = ((select New from Replacement)||(substr(ResearchItem,(select length+1 from Replacement)))), Icon = 'speciesImage_'||(select New from Replacement);
Update ResearchPackData set ResearchPack = ((select New from Replacement)||(substr(ResearchPack,(select length+1 from Replacement)))), AnimalType = ((select New from Replacement)||(substr(AnimalType,(select length+1 from Replacement))));
Update BreedingPackStatChanges set ResearchPack = ((select New from Replacement)||(substr(ResearchPack,(select length+1 from Replacement))));
Update EducationPackStatChanges set ResearchPack = ((select New from Replacement)||(substr(ResearchPack,(select length+1 from Replacement))));

/*This deletes the base animal from the master table*/
delete from AnimalData where AnimalSpecies not like (select New from Replacement);

