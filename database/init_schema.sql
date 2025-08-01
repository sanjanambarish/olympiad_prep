-- Table for bookmarked questions
CREATE TABLE IF NOT EXISTS bookmarks (
    id SERIAL PRIMARY KEY,
    student_id UUID NOT NULL,
    question_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    bookmarked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table for discussion posts
CREATE TABLE IF NOT EXISTS discussion_posts (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL,
    student_id UUID NOT NULL,
    student_name TEXT NOT NULL,
    content TEXT NOT NULL,
    posted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table for student badges
CREATE TABLE IF NOT EXISTS badges (
    id SERIAL PRIMARY KEY,
    student_id UUID NOT NULL,
    badge_name TEXT NOT NULL,
    description TEXT NOT NULL,
    awarded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_bookmarks_student_id ON bookmarks(student_id);
CREATE INDEX IF NOT EXISTS idx_discussion_posts_question_id ON discussion_posts(question_id);
CREATE INDEX IF NOT EXISTS idx_badges_student_id ON badges(student_id);