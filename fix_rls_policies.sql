-- Fix RLS policies to allow user registration
-- Run this in your Supabase SQL editor

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view own profile" ON users;
DROP POLICY IF EXISTS "Users can update own profile" ON users;
DROP POLICY IF EXISTS "Users can delete own profile" ON users;
DROP POLICY IF EXISTS "Allow user registration" ON users;

-- Create new policies that allow registration
-- Allow anyone to register (insert) new users
CREATE POLICY "Allow user registration" ON users
    FOR INSERT WITH CHECK (true);

-- Users can only see their own data
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

-- Only allow users to delete their own profile (optional)
CREATE POLICY "Users can delete own profile" ON users
    FOR DELETE USING (auth.uid() = id);

-- Also update other table policies to be more permissive for service role
-- Allow service role to manage all data (for API operations)

-- For customers table
DROP POLICY IF EXISTS "Users can manage own customers" ON customers;
CREATE POLICY "Users can manage own customers" ON customers
    FOR ALL USING (
        created_by = auth.uid() OR 
        auth.jwt() ->> 'role' = 'service_role'
    );

-- For quotes table  
DROP POLICY IF EXISTS "Users can manage own quotes" ON quotes;
CREATE POLICY "Users can manage own quotes" ON quotes
    FOR ALL USING (
        created_by = auth.uid() OR 
        auth.jwt() ->> 'role' = 'service_role'
    );

-- For invoices table
DROP POLICY IF EXISTS "Users can manage own invoices" ON invoices;
CREATE POLICY "Users can manage own invoices" ON invoices
    FOR ALL USING (
        created_by = auth.uid() OR 
        auth.jwt() ->> 'role' = 'service_role'
    );

-- For payments table
DROP POLICY IF EXISTS "Users can manage own payments" ON payments;
CREATE POLICY "Users can manage own payments" ON payments
    FOR ALL USING (
        created_by = auth.uid() OR 
        auth.jwt() ->> 'role' = 'service_role'
    );
