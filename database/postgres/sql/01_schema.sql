-- 01_schema.sql
-- PostgreSQL schema for local media-rights sample database

CREATE TABLE IF NOT EXISTS title (
    id BIGSERIAL PRIMARY KEY,
    title_name VARCHAR(255) NOT NULL,
    content_type VARCHAR(20) NOT NULL CHECK (content_type IN ('MOVIE', 'TV')),
    season_number INTEGER,
    episode_number INTEGER,
    genre VARCHAR(100),
    duration_minutes INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contract (
    id BIGSERIAL PRIMARY KEY,
    contract_number VARCHAR(50) NOT NULL UNIQUE,
    licensor VARCHAR(255) NOT NULL,
    license_start_date DATE NOT NULL,
    license_end_date DATE NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_contract_contract_number ON contract(contract_number);

CREATE TABLE IF NOT EXISTS contract_title (
    id BIGSERIAL PRIMARY KEY,
    contract_id BIGINT NOT NULL REFERENCES contract(id) ON DELETE CASCADE,
    title_id BIGINT NOT NULL REFERENCES title(id) ON DELETE CASCADE,
    territory VARCHAR(100) NOT NULL,
    language_rights VARCHAR(100) NOT NULL,
    platform_rights VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (contract_id, title_id, territory, language_rights, platform_rights)
);

CREATE INDEX IF NOT EXISTS idx_contract_title_contract_id ON contract_title(contract_id);
CREATE INDEX IF NOT EXISTS idx_contract_title_title_id ON contract_title(title_id);

CREATE TABLE IF NOT EXISTS contract_cost (
    id BIGSERIAL PRIMARY KEY,
    contract_id BIGINT NOT NULL REFERENCES contract(id) ON DELETE CASCADE,
    cost_type VARCHAR(20) NOT NULL CHECK (cost_type IN ('LICENSE', 'SUBDUB', 'OTHER')),
    amount NUMERIC(14,2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_contract_cost_contract_id ON contract_cost(contract_id);
CREATE INDEX IF NOT EXISTS idx_contract_cost_cost_type ON contract_cost(cost_type);

CREATE TABLE IF NOT EXISTS amort_curve (
    id BIGSERIAL PRIMARY KEY,
    contract_id BIGINT NOT NULL REFERENCES contract(id) ON DELETE CASCADE,
    title_id BIGINT REFERENCES title(id) ON DELETE SET NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    amort_amount NUMERIC(14,2) NOT NULL,
    basis VARCHAR(20) NOT NULL CHECK (basis IN ('TIME', 'USAGE')),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_amort_curve_contract_id ON amort_curve(contract_id);
CREATE INDEX IF NOT EXISTS idx_amort_curve_title_id ON amort_curve(title_id);

CREATE TABLE IF NOT EXISTS payment_schedule (
    id BIGSERIAL PRIMARY KEY,
    contract_id BIGINT NOT NULL REFERENCES contract(id) ON DELETE CASCADE,
    due_date DATE NOT NULL,
    amount NUMERIC(14,2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    milestone VARCHAR(255),
    status VARCHAR(20) NOT NULL CHECK (status IN ('PLANNED', 'PAID', 'OVERDUE')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_payment_schedule_contract_id ON payment_schedule(contract_id);
CREATE INDEX IF NOT EXISTS idx_payment_schedule_due_date ON payment_schedule(due_date);

CREATE TABLE IF NOT EXISTS closing_data (
    id BIGSERIAL PRIMARY KEY,
    contract_id BIGINT NOT NULL REFERENCES contract(id) ON DELETE CASCADE,
    close_date DATE NOT NULL,
    close_reason VARCHAR(255) NOT NULL,
    final_amort_amount NUMERIC(14,2),
    remarks TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (contract_id)
);

CREATE INDEX IF NOT EXISTS idx_closing_data_contract_id ON closing_data(contract_id);

-- Optional read-heavy views
CREATE OR REPLACE VIEW v_contract_overview AS
SELECT
    c.id AS contract_id,
    c.contract_number,
    c.licensor,
    c.license_start_date,
    c.license_end_date,
    c.currency,
    c.status,
    COUNT(DISTINCT ct.title_id) AS title_count,
    COALESCE(SUM(cc.amount), 0)::NUMERIC(14,2) AS total_cost
FROM contract c
LEFT JOIN contract_title ct ON c.id = ct.contract_id
LEFT JOIN contract_cost cc ON c.id = cc.contract_id
GROUP BY c.id;

CREATE OR REPLACE VIEW v_contract_cost_summary AS
SELECT
    c.contract_number,
    cc.cost_type,
    COALESCE(SUM(cc.amount), 0)::NUMERIC(14,2) AS total_amount,
    MAX(cc.currency) AS currency
FROM contract c
JOIN contract_cost cc ON c.id = cc.contract_id
GROUP BY c.contract_number, cc.cost_type;

CREATE OR REPLACE VIEW v_contract_amort_summary AS
SELECT
    c.contract_number,
    ac.period_start,
    ac.period_end,
    COALESCE(SUM(ac.amort_amount), 0)::NUMERIC(14,2) AS amort_amount
FROM contract c
JOIN amort_curve ac ON c.id = ac.contract_id
GROUP BY c.contract_number, ac.period_start, ac.period_end
ORDER BY c.contract_number, ac.period_start;
