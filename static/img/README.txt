Place your app logo image here.

Expected filenames:
- logo.png  (used for navbar brand and favicon)
- Optional: favicon.ico (32x32 or 48x48) for legacy browsers

Recommended sizes:
- 256x256 PNG for logo.png (will be auto-resized in the navbar)
- 32x32 ICO for favicon.ico, or rely on logo.png (already linked as favicon)

Where it will be used:
- templates/base.html references:
  - <img src="{% static 'img/logo.png' %}" ...> (navbar)
  - <link rel="icon" href="{% static 'img/logo.png' %}"> (favicon)

Steps:
1) Save your provided image (the gears head with red hat inside olive wreath) as:
   c:/Users/knaou/OneDrive/Site 2026 Cordination Dgango/final222/kbtuneco_project_final/static/img/logo.png
2) Optionally generate a favicon.ico from the same image and place it here. If omitted, the PNG will be used as favicon.
3) Run the site and hard refresh (Ctrl+F5) to see the new logo and favicon.

Notes:
- Static settings are configured in kbtuneco/settings.py (STATICFILES_DIRS includes the "static" folder).
- If DEBUG=False in production, remember to collect static files (python manage.py collectstatic).
