-- 02_seed_data.sql
-- Seed data for local testing

-- Titles
INSERT INTO title (id, title_name, content_type, season_number, episode_number, genre, duration_minutes)
VALUES
    (10, 'Space Saga S1', 'TV', 1, NULL, 'Sci-Fi', 480),
    (11, 'Space Saga S2', 'TV', 2, NULL, 'Sci-Fi', 500),
    (12, 'City Beats', 'MOVIE', NULL, NULL, 'Drama', 120)
ON CONFLICT (id) DO NOTHING;

-- Contracts
INSERT INTO contract (id, contract_number, licensor, license_start_date, license_end_date, currency, status)
VALUES
    (1, '123', 'Nova Studios', '2026-01-01', '2027-12-31', 'USD', 'ACTIVE'),
    (2, '456', 'Metro Pictures', '2026-03-01', '2028-02-28', 'USD', 'ACTIVE')
ON CONFLICT (id) DO NOTHING;

-- Contract-Title Mapping
INSERT INTO contract_title (contract_id, title_id, territory, language_rights, platform_rights)
VALUES
    (1, 10, 'US', 'EN', 'OTT'),
    (1, 11, 'US', 'EN', 'OTT'),
    (2, 12, 'GLOBAL', 'EN', 'TVOD')
ON CONFLICT DO NOTHING;

-- Contract Costs
INSERT INTO contract_cost (contract_id, cost_type, amount, currency, description)
VALUES
    (1, 'LICENSE', 150000.00, 'USD', 'Base license cost'),
    (1, 'SUBDUB', 25000.00, 'USD', 'Subtitling and dubbing package'),
    (1, 'OTHER', 10000.00, 'USD', 'Legal and metadata processing'),
    (2, 'LICENSE', 90000.00, 'USD', 'Movie license')
ON CONFLICT DO NOTHING;

-- Amortization Curve
INSERT INTO amort_curve (contract_id, title_id, period_start, period_end, amort_amount, basis, notes)
VALUES
    (1, 10, '2026-01-01', '2026-03-31', 50000.00, 'TIME', 'Q1 amort for S1'),
    (1, 11, '2026-04-01', '2026-06-30', 60000.00, 'TIME', 'Q2 amort for S2'),
    (2, 12, '2026-03-01', '2026-05-31', 30000.00, 'TIME', 'Initial amort for movie')
ON CONFLICT DO NOTHING;

-- Payment Schedule
INSERT INTO payment_schedule (contract_id, due_date, amount, currency, milestone, status)
VALUES
    (1, '2026-01-15', 75000.00, 'USD', 'Contract signing', 'PAID'),
    (1, '2026-04-15', 75000.00, 'USD', 'Season 2 delivery', 'PLANNED'),
    (2, '2026-03-15', 45000.00, 'USD', 'Movie ingest complete', 'PAID'),
    (2, '2026-07-15', 45000.00, 'USD', 'Platform launch', 'PLANNED')
ON CONFLICT DO NOTHING;

-- Closing Data
INSERT INTO closing_data (contract_id, close_date, close_reason, final_amort_amount, remarks)
VALUES
    (1, '2027-12-31', 'Term completed', 110000.00, 'Closed after full amort schedule completion')
ON CONFLICT (contract_id) DO NOTHING;
