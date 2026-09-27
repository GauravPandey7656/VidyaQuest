# PHASE 1C — Create Chapter API (Steps)

- [x] Inspect existing `app.py` to find where `/api/subjects` and lessons APIs are defined.
- [ ] Insert `GET /api/subjects/<sid>/chapters` API (STEP 10) below existing `api_subjects()`.
- [ ] Insert `GET /api/chapters/<cid>/lessons` API (STEP 11) immediately below the new chapters API.
- [ ] Save changes.
- [ ] Test APIs by running `python app.py` and visiting:
  - [ ] http://127.0.0.1:5000/api/subjects/1/chapters
  - [ ] http://127.0.0.1:5000/api/chapters/1/lessons

