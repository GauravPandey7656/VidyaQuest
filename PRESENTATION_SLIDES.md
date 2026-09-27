# Presentation Slides (Task 40)

## 1) Problem Statement
- Traditional learning often feels repetitive and low-engagement.
- Students lose motivation without clear progress, feedback, or rewards.
- Teachers lack actionable insights into student learning and quiz performance.

## 2) Research Motivation
- Educational psychology shows motivation improves with immediate feedback, mastery goals, and achievement structures.
- Gamified systems can improve engagement by making learning goals visible.
- Data-driven dashboards help teachers intervene earlier when learning is at risk.

## 3) Existing Systems
- Most e-learning platforms focus on content delivery (videos/articles) without strong game mechanics.
- Quiz systems may exist, but rewards/progress are often generic or not personalized.
- Teacher dashboards, when present, frequently lack clear learning journey mapping.

## 4) Proposed Solution
- Build **VidyaQuest**: a gamified learning platform where every lesson and quiz contributes to student XP, levels, streaks, and badges.
- Add richer lesson content support using video/images to improve comprehension.
- Provide a teacher dashboard with student and lesson analytics.

## 5) Architecture
- Frontend: HTML templates + JavaScript (fetch calls to backend APIs).
- Backend: Flask app with REST-like routes.
- Database: SQLite storing users, subjects, chapters, lessons, quizzes, and progress.
- Flow:
  - Client requests lesson/quiz data from APIs.
  - Student completes lesson/quiz.
  - Backend records progress and updates XP/levels/badges.
  - Teacher dashboard reads analytics from stored progress.

## 6) Database Design
- Key tables:
  - `users`: role (student/teacher), XP, level, streak, progress metadata.
  - `subjects`, `chapters`: learning hierarchy.
  - `lessons`: lesson content and (upgraded) media fields.
    - `title`, `content`, `video_url`, `image_url`, `xp_reward`, `order_num`
  - `quizzes`: question bank linked to `lesson_id`.
  - `user_progress`: completion state, scores, XP earned per lesson.
  - `badges`, `user_badges`: achievement system.

## 7) Gamification Features
- XP rewards for lesson completion and quiz performance.
- Levels computed from total XP.
- Streak tracking based on daily logins/engagement.
- Badges:
  - First lesson completed
  - Perfect score
  - XP thresholds
  - Lesson completion milestones
  - Streak milestones
- Progress visibility: completion percentage per chapter.

## 8) Teacher Dashboard
- Student analytics:
  - XP, level, streak, average quiz score
  - lessons completed count
- Lesson analytics:
  - number of completions per lesson
  - listing latest created lessons
- Risk insights:
  - students with low average quiz scores (at-risk)

## 9) Student Journey
1. Explore subjects and chapters.
2. Open a lesson page.
3. Learn from structured content (text + optional video/image).
4. Mark lesson complete for XP.
5. Take the quiz linked to the lesson.
6. Receive score + XP confirmation.
7. Track progress on dashboards; unlock badges and progress through chapters.

## 10) Future Scope
- Add interactive lesson elements (drag/drop, short checks).
- Admin/teacher media uploads instead of URLs.
- Learning personalization:
  - recommend next lesson based on quiz weakness.
- Enhanced analytics:
  - per-topic breakdown and intervention suggestions.
- Mobile-first UI and offline support.

