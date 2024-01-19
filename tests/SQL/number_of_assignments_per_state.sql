-- Write query to get number of assignments for each state
-- Numbers will be increase with every new test because data for previous tests will be left in the database

SELECT state, COUNT(*) AS state_count
FROM assignments
GROUP BY state
ORDER BY state;