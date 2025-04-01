SELECT 
    TO_CHAR(visit_date, 'YYYY-MM') AS month, 
    COUNT(*) AS num_visits
FROM visits
GROUP BY TO_CHAR(visit_date, 'YYYY-MM')
ORDER BY month;