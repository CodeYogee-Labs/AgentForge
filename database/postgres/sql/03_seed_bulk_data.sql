-- 03_seed_bulk_data.sql
-- Additional bulk seed data for local testing
-- Adds 50 titles, 5 contracts, and proportional related records.

-- Titles (50)
INSERT INTO title (id, title_name, content_type, season_number, episode_number, genre, duration_minutes)
VALUES
    (1001, 'Neon Harbor S1', 'TV', 1, NULL, 'Sci-Fi', 460),
    (1002, 'Neon Harbor S2', 'TV', 2, NULL, 'Sci-Fi', 470),
    (1003, 'Iron Summit S1', 'TV', 1, NULL, 'Action', 440),
    (1004, 'Iron Summit S2', 'TV', 2, NULL, 'Action', 450),
    (1005, 'Velvet Code S1', 'TV', 1, NULL, 'Thriller', 430),
    (1006, 'Velvet Code S2', 'TV', 2, NULL, 'Thriller', 440),
    (1007, 'Riverstone S1', 'TV', 1, NULL, 'Drama', 420),
    (1008, 'Riverstone S2', 'TV', 2, NULL, 'Drama', 430),
    (1009, 'Skyline Unit S1', 'TV', 1, NULL, 'Crime', 410),
    (1010, 'Skyline Unit S2', 'TV', 2, NULL, 'Crime', 420),
    (1011, 'Polar Echo S1', 'TV', 1, NULL, 'Mystery', 460),
    (1012, 'Polar Echo S2', 'TV', 2, NULL, 'Mystery', 470),
    (1013, 'Midnight Relay S1', 'TV', 1, NULL, 'Thriller', 450),
    (1014, 'Midnight Relay S2', 'TV', 2, NULL, 'Thriller', 460),
    (1015, 'Glass Orbit S1', 'TV', 1, NULL, 'Sci-Fi', 440),
    (1016, 'Glass Orbit S2', 'TV', 2, NULL, 'Sci-Fi', 450),
    (1017, 'Cipher District S1', 'TV', 1, NULL, 'Crime', 430),
    (1018, 'Cipher District S2', 'TV', 2, NULL, 'Crime', 440),
    (1019, 'Northline S1', 'TV', 1, NULL, 'Drama', 420),
    (1020, 'Northline S2', 'TV', 2, NULL, 'Drama', 430),
    (1021, 'Golden Avenue S1', 'TV', 1, NULL, 'Comedy', 400),
    (1022, 'Golden Avenue S2', 'TV', 2, NULL, 'Comedy', 410),
    (1023, 'Signal House S1', 'TV', 1, NULL, 'Mystery', 425),
    (1024, 'Signal House S2', 'TV', 2, NULL, 'Mystery', 435),
    (1025, 'Red Meridian S1', 'TV', 1, NULL, 'Action', 445),
    (1026, 'Red Meridian S2', 'TV', 2, NULL, 'Action', 455),
    (1027, 'Quiet Engine S1', 'TV', 1, NULL, 'Drama', 415),
    (1028, 'Quiet Engine S2', 'TV', 2, NULL, 'Drama', 425),
    (1029, 'Blue Lantern S1', 'TV', 1, NULL, 'Fantasy', 435),
    (1030, 'Blue Lantern S2', 'TV', 2, NULL, 'Fantasy', 445),
    (1031, 'The Last Orchard', 'MOVIE', NULL, NULL, 'Drama', 118),
    (1032, 'Delta Run', 'MOVIE', NULL, NULL, 'Action', 126),
    (1033, 'Echoes of June', 'MOVIE', NULL, NULL, 'Romance', 112),
    (1034, 'Burn Line', 'MOVIE', NULL, NULL, 'Thriller', 121),
    (1035, 'Paper Skies', 'MOVIE', NULL, NULL, 'Drama', 109),
    (1036, 'Gilded Night', 'MOVIE', NULL, NULL, 'Mystery', 117),
    (1037, 'Cloudbreaker', 'MOVIE', NULL, NULL, 'Sci-Fi', 124),
    (1038, 'Wild Current', 'MOVIE', NULL, NULL, 'Adventure', 119),
    (1039, 'Orbit Lane', 'MOVIE', NULL, NULL, 'Sci-Fi', 122),
    (1040, 'Second Signal', 'MOVIE', NULL, NULL, 'Crime', 115),
    (1041, 'Ash and Snow', 'MOVIE', NULL, NULL, 'Drama', 111),
    (1042, 'Borrowed Light', 'MOVIE', NULL, NULL, 'Romance', 113),
    (1043, 'Fracture Point', 'MOVIE', NULL, NULL, 'Action', 127),
    (1044, 'Silver Thread', 'MOVIE', NULL, NULL, 'Fantasy', 116),
    (1045, 'North of Amber', 'MOVIE', NULL, NULL, 'Drama', 114),
    (1046, 'Crimson Transit', 'MOVIE', NULL, NULL, 'Thriller', 123),
    (1047, 'Harbor Zero', 'MOVIE', NULL, NULL, 'Crime', 120),
    (1048, 'The Fifth Window', 'MOVIE', NULL, NULL, 'Mystery', 118),
    (1049, 'Lumen Park', 'MOVIE', NULL, NULL, 'Comedy', 107),
    (1050, 'Monsoon Frame', 'MOVIE', NULL, NULL, 'Drama', 110)
ON CONFLICT (id) DO NOTHING;

-- Contracts (5)
INSERT INTO contract (id, contract_number, licensor, license_start_date, license_end_date, currency, status)
VALUES
    (100, 'CN-2026-100', 'Orion Media Group', '2026-01-01', '2028-12-31', 'USD', 'ACTIVE'),
    (101, 'CN-2026-101', 'Summit Global Pictures', '2026-02-01', '2028-11-30', 'USD', 'ACTIVE'),
    (102, 'CN-2026-102', 'Blue Arc Studios', '2026-03-01', '2029-02-28', 'USD', 'ACTIVE'),
    (103, 'CN-2026-103', 'Horizon Reelworks', '2026-04-01', '2028-10-31', 'USD', 'ACTIVE'),
    (104, 'CN-2026-104', 'Harborline Entertainment', '2026-05-01', '2029-04-30', 'USD', 'ACTIVE')
ON CONFLICT (id) DO NOTHING;

-- Contract-Title Mapping (50; 10 titles per contract)
INSERT INTO contract_title (contract_id, title_id, territory, language_rights, platform_rights)
VALUES
    (100, 1001, 'US', 'EN', 'OTT'),
    (100, 1002, 'US', 'EN', 'OTT'),
    (100, 1003, 'US', 'EN', 'OTT'),
    (100, 1004, 'US', 'EN', 'OTT'),
    (100, 1005, 'US', 'EN', 'OTT'),
    (100, 1006, 'US', 'EN', 'OTT'),
    (100, 1007, 'US', 'EN', 'OTT'),
    (100, 1008, 'US', 'EN', 'OTT'),
    (100, 1009, 'US', 'EN', 'OTT'),
    (100, 1010, 'US', 'EN', 'OTT'),

    (101, 1011, 'LATAM', 'ES', 'TVOD'),
    (101, 1012, 'LATAM', 'ES', 'TVOD'),
    (101, 1013, 'LATAM', 'ES', 'TVOD'),
    (101, 1014, 'LATAM', 'ES', 'TVOD'),
    (101, 1015, 'LATAM', 'ES', 'TVOD'),
    (101, 1016, 'LATAM', 'ES', 'TVOD'),
    (101, 1017, 'LATAM', 'ES', 'TVOD'),
    (101, 1018, 'LATAM', 'ES', 'TVOD'),
    (101, 1019, 'LATAM', 'ES', 'TVOD'),
    (101, 1020, 'LATAM', 'ES', 'TVOD'),

    (102, 1021, 'EU', 'EN', 'AVOD'),
    (102, 1022, 'EU', 'EN', 'AVOD'),
    (102, 1023, 'EU', 'EN', 'AVOD'),
    (102, 1024, 'EU', 'EN', 'AVOD'),
    (102, 1025, 'EU', 'EN', 'AVOD'),
    (102, 1026, 'EU', 'EN', 'AVOD'),
    (102, 1027, 'EU', 'EN', 'AVOD'),
    (102, 1028, 'EU', 'EN', 'AVOD'),
    (102, 1029, 'EU', 'EN', 'AVOD'),
    (102, 1030, 'EU', 'EN', 'AVOD'),

    (103, 1031, 'APAC', 'EN', 'OTT'),
    (103, 1032, 'APAC', 'EN', 'OTT'),
    (103, 1033, 'APAC', 'EN', 'OTT'),
    (103, 1034, 'APAC', 'EN', 'OTT'),
    (103, 1035, 'APAC', 'EN', 'OTT'),
    (103, 1036, 'APAC', 'EN', 'OTT'),
    (103, 1037, 'APAC', 'EN', 'OTT'),
    (103, 1038, 'APAC', 'EN', 'OTT'),
    (103, 1039, 'APAC', 'EN', 'OTT'),
    (103, 1040, 'APAC', 'EN', 'OTT'),

    (104, 1041, 'GLOBAL', 'EN', 'SVOD'),
    (104, 1042, 'GLOBAL', 'EN', 'SVOD'),
    (104, 1043, 'GLOBAL', 'EN', 'SVOD'),
    (104, 1044, 'GLOBAL', 'EN', 'SVOD'),
    (104, 1045, 'GLOBAL', 'EN', 'SVOD'),
    (104, 1046, 'GLOBAL', 'EN', 'SVOD'),
    (104, 1047, 'GLOBAL', 'EN', 'SVOD'),
    (104, 1048, 'GLOBAL', 'EN', 'SVOD'),
    (104, 1049, 'GLOBAL', 'EN', 'SVOD'),
    (104, 1050, 'GLOBAL', 'EN', 'SVOD')
ON CONFLICT DO NOTHING;

-- Contract Costs (15; 3 per contract)
INSERT INTO contract_cost (contract_id, cost_type, amount, currency, description)
VALUES
    (100, 'LICENSE', 320000.00, 'USD', 'Primary license fee for 10 titles'),
    (100, 'SUBDUB', 45000.00, 'USD', 'Localization package EN variants'),
    (100, 'OTHER', 18000.00, 'USD', 'Legal and delivery fees'),

    (101, 'LICENSE', 295000.00, 'USD', 'Primary license fee for 10 titles'),
    (101, 'SUBDUB', 52000.00, 'USD', 'Localization package ES variants'),
    (101, 'OTHER', 20000.00, 'USD', 'Metadata and QC costs'),

    (102, 'LICENSE', 310000.00, 'USD', 'Primary license fee for 10 titles'),
    (102, 'SUBDUB', 40000.00, 'USD', 'Localization package EN/EU variants'),
    (102, 'OTHER', 22000.00, 'USD', 'Compliance and ingest charges'),

    (103, 'LICENSE', 280000.00, 'USD', 'Primary license fee for 10 titles'),
    (103, 'SUBDUB', 38000.00, 'USD', 'Localization package APAC EN variants'),
    (103, 'OTHER', 16000.00, 'USD', 'Archival and processing'),

    (104, 'LICENSE', 340000.00, 'USD', 'Primary license fee for 10 titles'),
    (104, 'SUBDUB', 60000.00, 'USD', 'Global language prep and dubbing'),
    (104, 'OTHER', 25000.00, 'USD', 'Legal and operations')
ON CONFLICT DO NOTHING;

-- Amortization Curve (50; one row per title mapping)
INSERT INTO amort_curve (contract_id, title_id, period_start, period_end, amort_amount, basis, notes)
VALUES
    (100, 1001, '2026-01-01', '2026-03-31', 32000.00, 'TIME', 'Q1 amortization'),
    (100, 1002, '2026-04-01', '2026-06-30', 32000.00, 'TIME', 'Q2 amortization'),
    (100, 1003, '2026-07-01', '2026-09-30', 32000.00, 'TIME', 'Q3 amortization'),
    (100, 1004, '2026-10-01', '2026-12-31', 32000.00, 'TIME', 'Q4 amortization'),
    (100, 1005, '2027-01-01', '2027-03-31', 32000.00, 'TIME', 'Q1 amortization'),
    (100, 1006, '2027-04-01', '2027-06-30', 32000.00, 'TIME', 'Q2 amortization'),
    (100, 1007, '2027-07-01', '2027-09-30', 32000.00, 'TIME', 'Q3 amortization'),
    (100, 1008, '2027-10-01', '2027-12-31', 32000.00, 'TIME', 'Q4 amortization'),
    (100, 1009, '2028-01-01', '2028-03-31', 32000.00, 'TIME', 'Q1 amortization'),
    (100, 1010, '2028-04-01', '2028-06-30', 32000.00, 'TIME', 'Q2 amortization'),

    (101, 1011, '2026-02-01', '2026-04-30', 29500.00, 'TIME', 'Period 1 amortization'),
    (101, 1012, '2026-05-01', '2026-07-31', 29500.00, 'TIME', 'Period 2 amortization'),
    (101, 1013, '2026-08-01', '2026-10-31', 29500.00, 'TIME', 'Period 3 amortization'),
    (101, 1014, '2026-11-01', '2027-01-31', 29500.00, 'TIME', 'Period 4 amortization'),
    (101, 1015, '2027-02-01', '2027-04-30', 29500.00, 'TIME', 'Period 5 amortization'),
    (101, 1016, '2027-05-01', '2027-07-31', 29500.00, 'TIME', 'Period 6 amortization'),
    (101, 1017, '2027-08-01', '2027-10-31', 29500.00, 'TIME', 'Period 7 amortization'),
    (101, 1018, '2027-11-01', '2028-01-31', 29500.00, 'TIME', 'Period 8 amortization'),
    (101, 1019, '2028-02-01', '2028-04-30', 29500.00, 'TIME', 'Period 9 amortization'),
    (101, 1020, '2028-05-01', '2028-07-31', 29500.00, 'TIME', 'Period 10 amortization'),

    (102, 1021, '2026-03-01', '2026-05-31', 31000.00, 'TIME', 'Period 1 amortization'),
    (102, 1022, '2026-06-01', '2026-08-31', 31000.00, 'TIME', 'Period 2 amortization'),
    (102, 1023, '2026-09-01', '2026-11-30', 31000.00, 'TIME', 'Period 3 amortization'),
    (102, 1024, '2026-12-01', '2027-02-28', 31000.00, 'TIME', 'Period 4 amortization'),
    (102, 1025, '2027-03-01', '2027-05-31', 31000.00, 'TIME', 'Period 5 amortization'),
    (102, 1026, '2027-06-01', '2027-08-31', 31000.00, 'TIME', 'Period 6 amortization'),
    (102, 1027, '2027-09-01', '2027-11-30', 31000.00, 'TIME', 'Period 7 amortization'),
    (102, 1028, '2027-12-01', '2028-02-29', 31000.00, 'TIME', 'Period 8 amortization'),
    (102, 1029, '2028-03-01', '2028-05-31', 31000.00, 'TIME', 'Period 9 amortization'),
    (102, 1030, '2028-06-01', '2028-08-31', 31000.00, 'TIME', 'Period 10 amortization'),

    (103, 1031, '2026-04-01', '2026-06-30', 28000.00, 'TIME', 'Period 1 amortization'),
    (103, 1032, '2026-07-01', '2026-09-30', 28000.00, 'TIME', 'Period 2 amortization'),
    (103, 1033, '2026-10-01', '2026-12-31', 28000.00, 'TIME', 'Period 3 amortization'),
    (103, 1034, '2027-01-01', '2027-03-31', 28000.00, 'TIME', 'Period 4 amortization'),
    (103, 1035, '2027-04-01', '2027-06-30', 28000.00, 'TIME', 'Period 5 amortization'),
    (103, 1036, '2027-07-01', '2027-09-30', 28000.00, 'TIME', 'Period 6 amortization'),
    (103, 1037, '2027-10-01', '2027-12-31', 28000.00, 'TIME', 'Period 7 amortization'),
    (103, 1038, '2028-01-01', '2028-03-31', 28000.00, 'TIME', 'Period 8 amortization'),
    (103, 1039, '2028-04-01', '2028-06-30', 28000.00, 'TIME', 'Period 9 amortization'),
    (103, 1040, '2028-07-01', '2028-09-30', 28000.00, 'TIME', 'Period 10 amortization'),

    (104, 1041, '2026-05-01', '2026-07-31', 34000.00, 'TIME', 'Period 1 amortization'),
    (104, 1042, '2026-08-01', '2026-10-31', 34000.00, 'TIME', 'Period 2 amortization'),
    (104, 1043, '2026-11-01', '2027-01-31', 34000.00, 'TIME', 'Period 3 amortization'),
    (104, 1044, '2027-02-01', '2027-04-30', 34000.00, 'TIME', 'Period 4 amortization'),
    (104, 1045, '2027-05-01', '2027-07-31', 34000.00, 'TIME', 'Period 5 amortization'),
    (104, 1046, '2027-08-01', '2027-10-31', 34000.00, 'TIME', 'Period 6 amortization'),
    (104, 1047, '2027-11-01', '2028-01-31', 34000.00, 'TIME', 'Period 7 amortization'),
    (104, 1048, '2028-02-01', '2028-04-30', 34000.00, 'TIME', 'Period 8 amortization'),
    (104, 1049, '2028-05-01', '2028-07-31', 34000.00, 'TIME', 'Period 9 amortization'),
    (104, 1050, '2028-08-01', '2028-10-31', 34000.00, 'TIME', 'Period 10 amortization')
ON CONFLICT DO NOTHING;

-- Payment Schedule (10; 2 per contract)
INSERT INTO payment_schedule (contract_id, due_date, amount, currency, milestone, status)
VALUES
    (100, '2026-01-15', 191500.00, 'USD', 'Contract signature and delivery setup', 'PAID'),
    (100, '2026-07-15', 191500.00, 'USD', 'Mid-term content delivery', 'PLANNED'),

    (101, '2026-02-15', 183500.00, 'USD', 'Contract signature and localization start', 'PAID'),
    (101, '2026-08-15', 183500.00, 'USD', 'Mid-term content delivery', 'PLANNED'),

    (102, '2026-03-15', 186000.00, 'USD', 'Contract signature and ingest', 'PAID'),
    (102, '2026-09-15', 186000.00, 'USD', 'Mid-term content delivery', 'PLANNED'),

    (103, '2026-04-15', 167000.00, 'USD', 'Contract signature and ingest', 'PAID'),
    (103, '2026-10-15', 167000.00, 'USD', 'Mid-term content delivery', 'PLANNED'),

    (104, '2026-05-15', 212500.00, 'USD', 'Contract signature and localization start', 'PAID'),
    (104, '2026-11-15', 212500.00, 'USD', 'Mid-term content delivery', 'PLANNED')
ON CONFLICT DO NOTHING;

-- Closing Data (3 of 5 contracts closed)
INSERT INTO closing_data (contract_id, close_date, close_reason, final_amort_amount, remarks)
VALUES
    (100, '2028-12-31', 'Term completed', 320000.00, 'Closed after planned amortization completion'),
    (101, '2028-11-30', 'Term completed', 295000.00, 'Closed after planned amortization completion'),
    (103, '2028-10-31', 'Term completed', 280000.00, 'Closed after planned amortization completion')
ON CONFLICT (contract_id) DO NOTHING;
