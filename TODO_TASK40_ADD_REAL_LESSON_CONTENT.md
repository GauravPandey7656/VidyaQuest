# TODO — Add Real Lesson Content (Task 39/40 Step Implementation)

## Step A — Update seeded lesson content + media
- [x] Edit `app.py` seed data for `lessons`:
  - [x] Lesson 1: "Introduction to Fractions" tuple updated with content + image_url + video_url + xp_reward + order_num
  - [x] Lesson 2: "Adding Fractions" tuple updated with content + image_url + video_url + xp_reward + order_num

## Step B — Update `templates/lesson.html` rendering
- [x] Replace `lessonContent.innerText` with `lessonContent.innerHTML` using the provided markup snippet
- [x] Remove/disable existing `#lessonMedia` image/video injection JS to avoid duplicates


## Step C — Rebuild DB
- [x] Delete `database/vidyaquest.db`
- [x] Run `python app.py` and verify `/lesson/1`


