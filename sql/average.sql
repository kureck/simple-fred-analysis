-- Average rate of unemployment for each year starting in 1980 and going up to 2015

SELECT year, ROUND(avg_year, 3) FROM (
SELECT DISTINCT(EXTRACT(year FROM observation_date)) AS year, AVG(value) OVER(PARTITION BY date_trunc('year', observation_date)) AS avg_year
FROM unrate
WHERE observation_date BETWEEN '1980-01-01' AND '2015-12-31') yearly
ORDER BY yearly.year;
