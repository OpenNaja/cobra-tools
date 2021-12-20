/*Copy the whole script below into SQLite’s SQL Editor; change ORIGINAL, NEW, and ORIGINAL into your original animal, its replacement, and the length of the animal’s name. USE THE FULL NAME OF THE ANIMAL even if you’re only replacing part of it. IE CuviersDwarfCaiman into NilecrcDwarfCaiman - I’d enter both full names, not only the part that changes*/

CREATE TEMP TABLE Replacement(Original TEXT PRIMARY KEY, New TEXT, Length INTEGER);

Insert Into Replacement(Original,New,Length) Values ('ORIGINAL','NEW',length('ORIGINAL'));

/*This clears out everything except our base creature.*/
delete from InfoBoardMaterials where ContentType not like ('%'||(select Original from Replacement)||'%');
delete from EducationResearchPacks where ContentType not like ('%'||(select Original from Replacement)||'%');
delete from EducationalContentTypes where Name not like ('%'||(select Original from Replacement)||'%');


/*This creates our new creature modeled off the base creature in the master table for this FDB*/
Insert into EducationalContentTypes (Name,Category,LocString) select ( (select New from Replacement)||(substr(Name,(select length+1 from Replacement)))),Category,('Animal_'||(select New from Replacement)||(Substr(Name,(select length+7 from Replacement))))LocString from EducationalContentTypes;

/*This updates all other tables to use your new species instead of the base creature*/
Update EducationResearchPacks set ContentType = ((select New from Replacement)||(substr(ContentType,(select length+1 from Replacement)))), Unlock1PackName = (select New from Replacement)||(substr(Unlock1PackName,(select length+1 from Replacement))), Unlock2PackName = (select New from Replacement)||(substr(Unlock2PackName,(select length+1 from Replacement))), Unlock3PackName = (select New from Replacement)||(substr(Unlock3PackName,(select length+1 from Replacement)));
Update InfoBoardMaterials set ContentType = ((select New from Replacement)||(substr(ContentType,(select length+1 from Replacement)))), MaterialName = 'ED_InfoBoard_Habitat_'||(select New from Replacement)||(substr(MaterialName,(select length+22 from Replacement)));

/*This deletes the base animal from the master table*/
delete from EducationalContentTypes where Name not like (select New from Replacement);


