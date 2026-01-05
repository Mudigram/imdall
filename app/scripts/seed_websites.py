from app.db.session import SessionLocal
from app.models.website import Website

SEED_WEBSITES = [
    "https://google.com",
    "https://github.com",
    "https://cloudflare.com",
    "https://fastapi.tiangolo.com",
    "https://www.wikipedia.org",
    "https://medium.com",
    "https://vercel.com",
    "https://stripe.com",
    "https://render.com",
    "https://openai.com",
    "http://example.invalid",
    "http://does-not-exist-12345.com",
    "http://gugggu.com",
    "https://httpstat.us/200?sleep=3000",
    "https://httpstat.us/200?sleep=5000",
    "https://httpstat.us/500",
    "https://httpstat.us/503",
]

def run():
    db = SessionLocal()

    for url in SEED_WEBSITES:
        exists = db.query(Website).filter(Website.url == url).first()
        if exists:
            continue

        site = Website(
            name=url,
            url=url,
            is_active=True
        )
        db.add(site)

    db.commit()
    db.close()
    print("Seeding complete")


if __name__ == "__main__":
    run()
