# AstroCare AI — local demo checklist

This is a recording/review guide, not evidence of submission or scientific acceptance.

1. Open PowerShell in the project root and run:

   ```powershell
   .\.venv\Scripts\python.exe -m pytest -q
   .\.venv\Scripts\python.exe -m pip check
   .\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
   ```

   Use an available port if 8501 is occupied. The active Sprint 4 review session is
   [http://localhost:8502](http://localhost:8502); it is not publicly hosted.

2. Start with **Health dashboard → Generated demo**. Show the **DEMO — SIMULATED
   DATA** notice, fictional profile, daily cards, and Sleep / Resting heart rate /
   Activity charts using **Visible charts**. Select one, any two, or all three;
   multiple selections stack vertically. Explain the dashed 7-day mean and observation counts without
   describing the changes as good/bad health outcomes. Coverage bars show available
   numeric records out of 7 days, not progress toward a medical target. Keep the
   language selector on **English** for the final English recording; optionally
   demonstrate another supported language and show that filter choices persist.

3. Change the review date or chart range. Expand **How to read these charts** or
   **Compare two 7-day periods** only when explaining those details. Use **Evidence
   & methods** for linked research context and the distinction between observations,
   calculations, and prototype rules.

4. If demonstrating manual entry, use invented values only. A successful save
   persists locally and selects the separate **Manual demo** profile; duplicate
   dates are rejected. Avoid accidental duplicate submissions during recording.
   Do not enter personal health or identifying information.

5. Switch to **NASA Research Explorer**. Show the compact **Verified NASA-hosted
   data** indicator (local file integrity only), **Research only · Not clinical
   monitoring**, and the separation from synthetic telemetry. Scientific status
   **CORRECTIONS REQUIRED** remains in **Safety & Scientific Review**. Show the
   sample counts, participant/analyte controls, original units, and discrete
   pre-/post-flight comparison cards and the compact analyte/participant/available-count/unit
   summary. Each sample has a thin horizontal bar, a visit label on the left,
   and an exact numeric value on the right. Both cards share one zero-based scale;
   their lengths are not independently normalized. Desktop cards sit side by side
   and stack on narrow screens. Explain that L− is before launch and R+ is after
   return, relative to different events; visits are independent, not paired.
   A missing result has a label and dashed empty track, never an invented zero.
   No connecting lines, intermediate values, or clinical ranges are added.
   Open **View measurements** to inspect the source values and **Study Context & Limitations** for launch/return semantics. Fluctuations alone do not
   establish clinical significance.
   These are serum samples, not daily
   sleep/heart-rate/activity telemetry. No health source is merged with another.

6. Expand **Dataset Details · Source & License** for official links, acquisition
   time, checksums, license evidence, and sampling caveats. If local files are
   missing or fail validation, show the honest error state. Prepare them with
   the documented acquisition command only when needed; do not substitute demo
   data or include the raw snapshots in GitHub delivery.

7. End with the limits: scientific status **CORRECTIONS REQUIRED**, no clinical
   validation or NASA approval, unresolved official Resources eligibility, and
   no integrated AI inference model. Obtain Scrum Master approval before committing,
   pushing, or claiming final submission readiness.
