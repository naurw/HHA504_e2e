/* 
Create a trigger that pushes an error message to the user when a new row is inserted that has h1n1_concern greater than a value of 3. 
The trigger should be called h1n1_concern_trigger and should have the following error message: “H1N1 concern should be a numerical value between 0 and 3. Please try again.”
*/

SELECT * FROM H1N1_Flu_Vaccines LIMIT 15;
DELIMITER $$
CREATE TRIGGER H1N1_concern_trigger BEFORE INSERT ON H1N1_Flu_Vaccines
FOR EACH ROW 
BEGIN IF NEW.alert >=3 THEN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'H1N1 concern should be a numerical value between 0 and 3. Please try again.'
;END IF;
END; $$