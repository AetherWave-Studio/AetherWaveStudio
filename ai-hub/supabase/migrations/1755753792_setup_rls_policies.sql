-- Migration: setup_rls_policies
-- Created at: 1755753792

-- Enable RLS on all tables
ALTER TABLE tools ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;

-- Public read access for tools and categories (everyone can view)
CREATE POLICY "Tools are viewable by everyone" ON tools FOR SELECT USING (true);
CREATE POLICY "Categories are viewable by everyone" ON categories FOR SELECT USING (true);

-- Profiles policies
CREATE POLICY "Users can view all profiles" ON profiles FOR SELECT USING (true);
CREATE POLICY "Users can insert their own profile" ON profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "Users can update their own profile" ON profiles FOR UPDATE USING (auth.uid() = id);

-- User submissions policies (authenticated users can submit, only submitter can view their own)
CREATE POLICY "Users can submit tools" ON user_submissions FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can view their own submissions" ON user_submissions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update their own submissions" ON user_submissions FOR UPDATE USING (auth.uid() = user_id);

-- User favorites policies (authenticated users can manage their own favorites)
CREATE POLICY "Users can view their own favorites" ON user_favorites FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can add favorites" ON user_favorites FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can remove their own favorites" ON user_favorites FOR DELETE USING (auth.uid() = user_id);;