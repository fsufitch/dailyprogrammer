CREATE TABLE ip_ranges (startip numeric(10), endip numeric(10), name text);
CREATE INDEX ip_ranges_index ON ip_ranges (startip, endip, name);

