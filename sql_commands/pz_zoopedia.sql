/*Copy the whole script below into SQLite’s SQL Editor; change ORIGINAL, NEW, and ORIGINAL into your original animal, its replacement, and the length of the animal’s name. USE THE FULL NAME OF THE ANIMAL even if you’re only replacing part of it. IE CuviersDwarfCaiman into NilecrcDwarfCaiman - I’d enter both full names, not only the part that changes*/

CREATE TEMP TABLE Replacement(Original TEXT PRIMARY KEY, New TEXT, Length INTEGER);

Insert Into Replacement(Original,New,Length) Values ('ORIGINAL','NEW',length('ORIGINAL'));


/*This clears out everything except our base creature.*/
delete from BarrierRequirements where Species not like ('%'||(select Original from Replacement)||'%');
delete from SpeciesFunFactsUnitData where Species not like ('%'||(select Original from Replacement)||'%');
delete from SpeciesAverageStats where Species not like ('%'||(select Original from Replacement)||'%');
delete from SpeciesZoopediaData where Species not like('%'||(select Original from Replacement)||'%');
delete from SpeciesFunFacts where Species not like ('%'||(select Original from Replacement)||'%');
delete from SpeciesZoopediaUnitData where Species not like ('%'||(select Original from Replacement)||'%');
delete from Species where InternalName not like ('%'||(select Original from Replacement)||'%');


/*This creates our new creature modeled off the base creature in the master table for this FDB*/
Insert Into Species(InternalName,EnclosureType,ContentPack)
select r.new, s.enclosuretype, s.contentpack from replacement r, species s where r.original = s.internalname;


/*This updates all other tables to use your new species instead of the base creature*/

Update BarrierRequirements set Species = (select New from Replacement);

Update SpeciesAverageStats set Species = (select New from Replacement);

Update SpeciesZoopediaData set Species = (select New from Replacement);

Insert into SpeciesFunFacts (Species,FunFact,ResearchPackName) values ((select original from replacement),'dummy','dummy');
Update SpeciesFunFactsUnitData set FunFact = 'dummy';

Update SpeciesFunFacts set species = (select new from replacement), FunFact = 'Zoopedia_FunFacts_'||(select New from Replacement)||(substr(FunFact,(select length+19 from replacement))), ResearchPackName = ((select New from Replacement)||(substr(ResearchPackName,(select length+1 from replacement)))) where FunFact != 'dummy';

Update SpeciesFunFactsUnitData set Species = (select New from Replacement), FunFact = (select FunFact from SpeciesFunFacts);
Delete from SpeciesFunFacts where FunFact = 'dummy';

Update SpeciesZoopediaUnitData set Species = (select New from Replacement);

/*This deletes the base animal from the master table*/
Delete from Species where InternalName not like (select New from Replacement);

