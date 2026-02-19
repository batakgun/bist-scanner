"""
BIST 100 Teknik Analiz Tarayici - Backend
==========================================
Kurulum:
    pip install yfinance pandas ta flask flask-cors requests

Calistirma:
    python scanner.py
"""

import yfinance as yf
import pandas as pd
import ta
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Yahoo Finance engelini asmak icin session ayarlari
def get_yf_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    })
    return session

TICKERS = {
    "AEFES.IS":  "Icecek",
    "AGHOL.IS":  "Holding",
    "AKBNK.IS":  "Banka",
    "AKSA.IS":   "Kimya",
    "AKSEN.IS":  "Enerji",
    "ALARK.IS":  "Holding",
    "ALTNY.IS":  "Altin",
    "ANSGR.IS":  "Sigorta",
    "ARCLK.IS":  "Beyaz Esya",
    "ASELS.IS":  "Savunma",
    "ASTOR.IS":  "Enerji",
    "BALSU.IS":  "Gida",
    "BIMAS.IS":  "Perakende",
    "BRSAN.IS":  "Demir/Celik",
    "BRYAT.IS":  "Turizm",
    "BSOKE.IS":  "Cimento",
    "BTCIM.IS":  "Cimento",
    "CANTE.IS":  "Gida",
    "CCOLA.IS":  "Icecek",
    "CIMSA.IS":  "Cimento",
    "CWENE.IS":  "Enerji",
    "DAPGM.IS":  "GYO",
    "DOAS.IS":   "Otomotiv",
    "DOHOL.IS":  "Holding",
    "DSTKF.IS":  "Teknoloji",
    "ECILC.IS":  "Holding",
    "EFOR.IS":   "Enerji",
    "EGEEN.IS":  "Enerji",
    "EKGYO.IS":  "GYO",
    "ENERY.IS":  "Enerji",
    "ENJSA.IS":  "Enerji",
    "ENKAI.IS":  "Insaat",
    "EREGL.IS":  "Demir/Celik",
    "EUPWR.IS":  "Enerji",
    "FENER.IS":  "Spor",
    "FROTO.IS":  "Otomotiv",
    "GARAN.IS":  "Banka",
    "GENIL.IS":  "Enerji",
    "GESAN.IS":  "Otomotiv",
    "GLRMK.IS":  "Insaat",
    "GRSEL.IS":  "Lojistik",
    "GRTHO.IS":  "Saglik",
    "GSRAY.IS":  "Spor",
    "GUBRF.IS":  "Gubre",
    "HALKB.IS":  "Banka",
    "HEKTS.IS":  "Kimya",
    "ISCTR.IS":  "Banka",
    "ISMEN.IS":  "Finans",
    "IZENR.IS":  "Enerji",
    "KCAER.IS":  "Enerji",
    "KCHOL.IS":  "Holding",
    "KLRHO.IS":  "Cam",
    "KONTR.IS":  "Insaat",
    "KRDMD.IS":  "Demir/Celik",
    "KTLEV.IS":  "Finans",
    "KUYAS.IS":  "Insaat",
    "MAGEN.IS":  "Enerji",
    "MAVI.IS":   "Tekstil",
    "MGROS.IS":  "Perakende",
    "MIATK.IS":  "Teknoloji",
    "MPARK.IS":  "Saglik",
    "OBAMS.IS":  "Finans",
    "ODAS.IS":   "Enerji",
    "OTKAR.IS":  "Otomotiv",
    "OYAKC.IS":  "Cimento",
    "PASEU.IS":  "Enerji",
    "PATEK.IS":  "Teknoloji",
    "PETKM.IS":  "Kimya",
    "PGSUS.IS":  "Havacilik",
    "QUAGR.IS":  "Tarim",
    "RALYH.IS":  "Holding",
    "REEDR.IS":  "Enerji",
    "SAHOL.IS":  "Holding",
    "SASA.IS":   "Kimya",
    "SISE.IS":   "Cam",
    "SKBNK.IS":  "Banka",
    "SOKM.IS":   "Perakende",
    "TABGD.IS":  "Gida",
    "TAVHL.IS":  "Turizm",
    "TCELL.IS":  "Telecom",
    "THYAO.IS":  "Havacilik",
    "TKFEN.IS":  "Holding",
    "TOASO.IS":  "Otomotiv",
    "TRALT.IS":  "Metal",
    "TRENJ.IS":  "Enerji",
    "TRMET.IS":  "Metal",
    "TSKB.IS":   "Banka",
    "TSPOR.IS":  "Spor",
    "TTKOM.IS":  "Telecom",
    "TTRAK.IS":  "Tarim Mak.",
    "TUKAS.IS":  "Gida",
    "TUPRS.IS":  "Enerji",
    "TUREX.IS":  "Tekstil",
    "TURSG.IS":  "Turizm",
    "ULKER.IS":  "Gida",
    "VAKBN.IS":  "Banka",
    "VESTL.IS":  "Teknoloji",
    "YEOTK.IS":  "Enerji",
    "YKBNK.IS":  "Banka",
    "ZOREN.IS":  "Enerji",
}


def analyze(ticker, sector, period="3mo", interval="1d"):
    try:
        session = get_yf_session()
        t = yf.Ticker(ticker, session=session)
        df = t.history(period=period, interval=interval, auto_adjust=True)

        if df.empty or len(df) < 50:
            print(f"  [ATLA] {ticker}: yeterli veri yok")
            return None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        close = df["Close"]
        high  = df["High"]
        low   = df["Low"]
        vol   = df["Volume"]

        df["RSI"]   = ta.momentum.RSIIndicator(close, window=14).rsi()

        macd_ind          = ta.trend.MACD(close, window_slow=26, window_fast=12, window_sign=9)
        df["MACD"]        = macd_ind.macd()
        df["MACD_signal"] = macd_ind.macd_signal()

        df["EMA20"] = ta.trend.EMAIndicator(close, window=20).ema_indicator()
        df["EMA50"] = ta.trend.EMAIndicator(close, window=50).ema_indicator()

        df["ADX"] = ta.trend.ADXIndicator(high, low, close, window=14).adx()

        bb_ind         = ta.volatility.BollingerBands(close, window=20, window_dev=2)
        df["BB_upper"] = bb_ind.bollinger_hband()
        df["BB_lower"] = bb_ind.bollinger_lband()
        df["BB_width"] = bb_ind.bollinger_wband()

        latest  = df.iloc[-1]
        prev    = df.iloc[-2]
        avg_vol = vol.rolling(20).mean().iloc[-1]

        signals = []
        score   = 50

        rsi = float(latest["RSI"]) if not pd.isna(latest["RSI"]) else 50

        if rsi < 30:
            signals.append("RSI_ASIRI_SATIS"); score += 15
        elif rsi > 70:
            signals.append("RSI_ASIRI_ALIM"); score -= 15

        m_now, m_prev = latest["MACD"], prev["MACD"]
        s_now, s_prev = latest["MACD_signal"], prev["MACD_signal"]
        if not any(pd.isna([m_now, m_prev, s_now, s_prev])):
            if m_now > s_now and m_prev <= s_prev:
                signals.append("MACD_KESIS_YUKARI"); score += 20
            elif m_now < s_now and m_prev >= s_prev:
                signals.append("MACD_KESIS_ASAGI"); score -= 20

        e20n, e50n = latest["EMA20"], latest["EMA50"]
        e20p, e50p = prev["EMA20"],   prev["EMA50"]
        if not any(pd.isna([e20n, e50n, e20p, e50p])):
            if e20n > e50n and e20p <= e50p:
                signals.append("EMA_GOLDEN_CROSS"); score += 25
            elif e20n < e50n and e20p >= e50p:
                signals.append("EMA_DEATH_CROSS"); score -= 25

        adx = float(latest["ADX"]) if not pd.isna(latest["ADX"]) else 0
        if adx > 25:
            signals.append(f"GUCLU_TREND_{adx:.0f}"); score += 10

        bbu = float(latest["BB_upper"])
        bbl = float(latest["BB_lower"])
        price_now = float(latest["Close"])
        bb_pos = round((price_now - bbl) / (bbu - bbl) * 100, 1) if (bbu - bbl) > 0 else 50

        bw_now = float(latest["BB_width"]) if not pd.isna(latest["BB_width"]) else 0
        bw_avg = df["BB_width"].rolling(20).mean().iloc[-1]
        if not pd.isna(bw_avg) and bw_avg > 0 and bw_now < bw_avg * 0.7:
            signals.append("BB_SQUEEZE"); score += 10

        vol_ratio = float(vol.iloc[-1]) / float(avg_vol) if avg_vol > 0 else 1
        if vol_ratio > 1.5:
            signals.append(f"HACIM_{vol_ratio:.1f}X"); score += 10

        support    = round(float(low.rolling(20).min().iloc[-1]), 2)
        resistance = round(float(high.rolling(20).max().iloc[-1]), 2)

        prev_close = float(prev["Close"])
        change     = round((price_now - prev_close) / prev_close * 100, 2)

        score     = min(100, max(0, score))
        direction = "BUY" if score >= 65 else "SELL" if score <= 35 else "NEUTRAL"

        return {
            "ticker":     ticker.replace(".IS", ""),
            "sector":     sector,
            "price":      round(price_now, 2),
            "change":     change,
            "rsi":        round(rsi, 1),
            "macd":       round(float(m_now), 3) if not pd.isna(m_now) else 0,
            "adx":        round(adx, 1),
            "bb_pos":     bb_pos,
            "vol_ratio":  round(vol_ratio, 2),
            "support":    support,
            "resistance": resistance,
            "signals":    signals,
            "score":      score,
            "direction":  direction,
        }

    except Exception as e:
        print(f"  [HATA] {ticker}: {e}")
        return None


@app.route("/scan")
def scan():
    print(f"\n>>> Tarama basladi — {len(TICKERS)} hisse...\n")
    results = []
    for i, (ticker, sector) in enumerate(TICKERS.items(), 1):
        print(f"  [{i:03d}/{len(TICKERS)}] {ticker}")
        r = analyze(ticker, sector)
        if r:
            results.append(r)
    print(f"\n>>> Tamamlandi — {len(results)} hisse analiz edildi.\n")
    return jsonify(results)


@app.route("/detail/<ticker>")
def detail(ticker):
    sector = TICKERS.get(ticker + ".IS", "BIST")
    return jsonify(analyze(ticker + ".IS", sector, period="6mo"))


@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "BIST 100 Scanner API calisıyor"})


if __name__ == "__main__":
    print("=" * 55)
    print(f"  BIST 100 Scanner ({len(TICKERS)} hisse) — http://localhost:5000")
    print("=" * 55)
    app.run(port=5000, debug=False)
