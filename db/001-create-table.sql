CREATE TABLE pours (
  id UUID UNIQUE NOT NULL,
  user_id UUID,
  pour_time_start TIMESTAMP,
  pour_time_end TIMESTAMP
);

ALTER TABLE pours ADD COLUMN beverage_id UUID NOT NULL;
ALTER TABLE pours ADD COLUMN amount TEXT NOT NULL;
