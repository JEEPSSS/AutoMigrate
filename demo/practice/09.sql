-- Technicians with sessions who never worked outside their specialisation.
-- Require at least one session so an unused technician does not qualify vacuously.
SELECT t.Technician_ID, t.Name, t.Primary_Specialisation,
       COUNT(*) AS Sessions
FROM TECHNICIAN t
JOIN WORK_SESSION ws ON ws.Technician_ID = t.Technician_ID
JOIN REPAIR_PROCEDURE rp ON rp.Procedure_ID = ws.Procedure_ID
GROUP BY t.Technician_ID, t.Name, t.Primary_Specialisation
HAVING SUM(CASE WHEN t.Primary_Specialisation <> rp.Procedure_Type
                THEN 1 ELSE 0 END) = 0
ORDER BY t.Technician_ID;

/*
Verified on 10.96.189.36 / tel3g3 at 2026-10-24T21:13:46.933140+08:00
+-----------------+---------------+--------------------------+------------+
| Technician_ID   | Name          | Primary_Specialisation   | Sessions   |
+=================+===============+==========================+============+
| 2               | Bernice Yeo   | Display                  | 9          |
+-----------------+---------------+--------------------------+------------+
| 4               | Dinesh Nair   | Battery                  | 11         |
+-----------------+---------------+--------------------------+------------+
| 6               | Farhan Ismail | Audio                    | 4          |
+-----------------+---------------+--------------------------+------------+
| 7               | Grace Tham    | Audio                    | 4          |
+-----------------+---------------+--------------------------+------------+
| 8               | Henry Low     | Logic Board              | 8          |
+-----------------+---------------+--------------------------+------------+
| 9               | Ivy Sim       | Logic Board              | 4          |
+-----------------+---------------+--------------------------+------------+
6 row(s).
*/
