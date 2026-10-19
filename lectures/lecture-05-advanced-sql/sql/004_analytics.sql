-- Lecture 5: ანალიტიკური query-ები, views და ინდექსი

-- LAG(): დღიური ცვლილება
SELECT currency_code, rate_date, rate,
       ROUND(rate - LAG(rate) OVER (PARTITION BY currency_code ORDER BY rate_date), 4) AS daily_change
FROM currency.rates
WHERE currency_code IN ('USD', 'EUR')
ORDER BY currency_code, rate_date;

-- Moving average (3 საათი)
SELECT forecast_time, temperature_c,
       ROUND(AVG(temperature_c) OVER (ORDER BY forecast_time
             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3h
FROM weather.forecasts
WHERE city = 'Tbilisi'
ORDER BY forecast_time;

-- CTE: მნიშვნელოვანი ცვლილებები
WITH usd_changes AS (
    SELECT rate_date, rate,
           ROUND(rate - LAG(rate) OVER (ORDER BY rate_date), 4) AS daily_change
    FROM currency.rates
    WHERE currency_code = 'USD'
)
SELECT rate_date, rate, daily_change
FROM usd_changes
WHERE ABS(daily_change) > 0.002
ORDER BY rate_date;

-- JOIN + GROUP BY + HAVING
SELECT c.name, COUNT(*) AS days_recorded, ROUND(AVG(r.rate), 4) AS avg_rate
FROM currency.rates r
JOIN currency.currencies c ON c.code = r.currency_code
GROUP BY c.name
HAVING COUNT(*) >= 5
ORDER BY avg_rate DESC;

-- View
CREATE OR REPLACE VIEW currency.v_usd_eur_trend AS
SELECT currency_code, rate_date, rate,
       ROUND(rate - LAG(rate) OVER (PARTITION BY currency_code ORDER BY rate_date), 4) AS daily_change
FROM currency.rates
WHERE currency_code IN ('USD', 'EUR');

-- Materialized View
CREATE MATERIALIZED VIEW IF NOT EXISTS weather.mv_daily_summary AS
SELECT city,
       DATE(forecast_time) AS forecast_date,
       ROUND(AVG(temperature_c), 2) AS avg_temp,
       ROUND(MAX(temperature_c), 2) AS max_temp,
       ROUND(MIN(temperature_c), 2) AS min_temp
FROM weather.forecasts
GROUP BY city, DATE(forecast_time);

REFRESH MATERIALIZED VIEW weather.mv_daily_summary;

-- ინდექსი
CREATE INDEX IF NOT EXISTS idx_forecasts_city_time ON weather.forecasts (city, forecast_time);
