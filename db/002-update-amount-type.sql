ALTER TABLE pours RENAME COLUMN amount to amount_formatted;
ALTER TABLE pours ADD COLUMN amount INT;
ALTER TABLE pours ALTER COLUMN amount SET NOT NULL;
