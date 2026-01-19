from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, List, Union
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


@dataclass
class AdItem:
    location_raw: Optional[str] = None   # z.B. "55116 Mainz" oder "59889"
    plz: Optional[str] = None            # z.B. "55116"
    ort: Optional[str] = None            # z.B. "Mainz"
    datum: Optional[str] = None          # z.B. "04.12.2025"
    titel: Optional[str] = None          # z.B. "Nova Mentor ..."
    link: Optional[str] = None           # z.B. URL zum Eintrag
    preis: Optional[str] = None          # z.B. "999 € VB"
    alter_preis: Optional[str] = None    # z.B. "1.100 €"
    versand: Optional[str] = None        # z.B. "Versand möglich"

def _read_html(source: str) -> str:
    """
    Lädt HTML entweder von einer URL (http/https) oder von einer lokalen Datei (Pfad oder file://...).
    """
    parsed = urlparse(source)

    # file://...
    if parsed.scheme == "file":
        path = Path(parsed.path)
        return path.read_text(encoding="utf-8", errors="replace")

    # http(s)...
    if parsed.scheme in ("http", "https"):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }
        resp = requests.get(source, headers=headers, timeout=30)
        resp.raise_for_status()
        # requests erkennt encoding meist korrekt; zur Sicherheit:
        if resp.encoding is None:
            resp.encoding = resp.apparent_encoding
        return resp.text

    # sonst: als lokaler Pfad interpretieren
    path = Path(source)
    return path.read_text(encoding="utf-8", errors="replace")


def _clean_text(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    s = re.sub(r"\s+", " ", s).strip()
    return s or None


def _extract_plz_ort(location_raw: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """
    Erwartet sowas wie "55116 Mainz" oder "59889" oder "36163 Poppenhausen".
    """
    if not location_raw:
        return None, None

    m = re.search(r"\b(\d{5})\b", location_raw)
    plz = m.group(1) if m else None

    ort = None
    if plz:
        # Alles nach der PLZ als Ort
        after = location_raw.split(plz, 1)[-1].strip()
        ort = after or None

    return plz, ort


def parse_ads(url_or_path: str) -> List[dict]:
    """
    Hauptfunktion: bekommt Website-URL oder lokalen Dateipfad und liefert Liste von Dicts.
    """
    html = _read_html(url_or_path)
    soup = BeautifulSoup(html, "lxml")

    results_div = soup.find("div", id="srchrslt-results")
    if not results_div:
        # Fallback: manchmal ist der Container anders benannt
        results_div = soup

    ads: List[dict] = []

    for art in results_div.select("article.aditem"):
        # Location + Datum
        location_raw = _clean_text(art.select_one(".aditem-main--top--left") and art.select_one(".aditem-main--top--left").get_text(" ", strip=True))
        datum = _clean_text(art.select_one(".aditem-main--top--right") and art.select_one(".aditem-main--top--right").get_text(" ", strip=True))

        # Oft stehen Icons + Text im selben Block; wir nehmen einfach den Text und säubern:
        # Beispiel aus Testdatei: "55116 Mainz" links und "16.02.2025" rechts :contentReference[oaicite:8]{index=8}
        plz, ort = _extract_plz_ort(location_raw)

        # Titel
        titel_el = art.select_one("h2 a.ellipsis")
        titel = _clean_text(titel_el.get_text(strip=True) if titel_el else None)
        
        # Link
        link = None
        if titel_el and titel_el.has_attr("href"):
            href = titel_el["href"].strip()
            # Kleinanzeigen nutzt oft relative Links -> absolut machen
            if href.startswith("http"):
                link = href
            else:
                link = "https://www.kleinanzeigen.de" + href
        

        # Preis + alter Preis
        preis_el = art.select_one(".aditem-main--middle--price-shipping--price")
        preis = _clean_text(preis_el.get_text(" ", strip=True) if preis_el else None)

        old_el = art.select_one(".aditem-main--middle--price-shipping--old-price")
        alter_preis = _clean_text(old_el.get_text(" ", strip=True) if old_el else None)

        # Versand-Tag
        versand_text = None
        for tag in art.select(".aditem-main--bottom .simpletag"):
            t = _clean_text(tag.get_text(" ", strip=True))
            if t and "versand" in t.lower():
                versand_text = t
                break

        item = AdItem(
            location_raw=location_raw,
            plz=plz,
            ort=ort,
            datum=datum,
            titel=titel,
            link=link,
            preis=preis,
            alter_preis=alter_preis,
            versand=versand_text,
        )
        ads.append(asdict(item))

    return ads


if __name__ == "__main__":
    # Lokal testen:
    # 1) Direkter Pfad:
    data = parse_ads("test.html")

    # 2) Oder file:// URL:
    # data = parse_ads("file:///mnt/data/test.html")

    for i, ad in enumerate(data[:3], start=1):
        print(f"\n--- Eintrag {i} ---")
        for k, v in ad.items():
            print(f"{k:12}: {v}")
    print(f"\nInsgesamt gefunden: {len(data)}")
