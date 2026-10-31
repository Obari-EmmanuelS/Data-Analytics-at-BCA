# Upload this project to your GitHub repository (Mac)

Target repository: https://github.com/Obari-EmmanuelS/Data-Analytics-at-BCA

## Browser upload (beginner-friendly)

1. Download the GitHub-ready ZIP from ChatGPT and **double-click** it in Finder to extract the contents.
2. Open your empty GitHub repository in Chrome.
3. In the **Quick setup** box, select **uploading an existing file**.
4. In Finder, open the extracted project folder. Select its contents (Command + A), then drag the selected files and folders into the GitHub upload area. Keep the folders intact.
5. Confirm the preview shows `README.md`, `Light-and-Love-House-Analytics.xlsx`, `data/`, `dashboard/`, `scripts/`, `outputs/`, `docs/`, `tests/` and `sql/`. GitHub may display nested paths after upload.
6. Set the commit message to `Add original Light and Love House analytics project`, then select **Commit changes**.
7. Refresh the repository page. Verify both PNG images render inside the README and that the workbook link opens.
8. Open the repository in an Incognito window (Command + Shift + N) to confirm it is publicly accessible.

**Important:** Do not upload the ZIP alone as a single GitHub file: extract and upload the *contents* so visitors can open the README, workbook, scripts and dashboard images individually. If Chrome won't accept folder dragging, use GitHub Desktop or the command line instead.

## Terminal upload (alternative; requires Git installed)

Navigate into the extracted folder in Terminal, then run:

```bash
git init
git branch -M main
git add .
git commit -m "Add original Light and Love House analytics project"
git remote add origin https://github.com/Obari-EmmanuelS/Data-Analytics-at-BCA.git
git push -u origin main
```

GitHub may prompt you to authenticate. Do not share passwords, access tokens or recovery codes in chat.

## Verify before submitting

- Check the workbook opens, including Executive Dashboard and the 90D Repurchase sheet.
- Open the two dashboard images and confirm they are legible on a phone.
- Confirm the README clearly identifies the dataset as simulated, never as real company data.
- Ensure the data and charts agree, and the `outputs/validation.json` checks are all true.
- Do not add the source repositories' workbooks or images; this package uses new data and project assets.
