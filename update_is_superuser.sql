-- Update is_superuser column from boolean to varchar
-- First, add a temporary column
ALTER TABLE users ADD COLUMN is_superuser_temp VARCHAR(50) DEFAULT 'user';

-- Update the temporary column based on the boolean values
UPDATE users SET is_superuser_temp = CASE 
    WHEN is_superuser = true THEN 'admin'
    ELSE 'user'
END;

-- Drop the old boolean column
ALTER TABLE users DROP COLUMN is_superuser;

-- Rename the temporary column to is_superuser
ALTER TABLE users RENAME COLUMN is_superuser_temp TO is_superuser;

-- Verify the changes
SELECT id, email, full_name, role, is_superuser, is_active FROM users;
