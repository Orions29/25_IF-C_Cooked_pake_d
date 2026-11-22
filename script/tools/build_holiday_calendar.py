
from pathlib import Path
import pandas as pd


# ==========================================
# 1. PROJECT PATH
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_PATH = (
    PROJECT_ROOT
    / "datasets"
    / "processed"
    / "nyc_holiday_event_calendar_2026.csv"
)


# ==========================================
# 2. EVENT DATA
# ==========================================

events = [
    {
        "name": "New Year's Day",
        "start": "2026-01-01",
        "end": "2026-01-01",
        "category": "Federal Holiday",
    },
    {
        "name": "Martin Luther King Jr. Day",
        "start": "2026-01-19",
        "end": "2026-01-19",
        "category": "Federal Holiday",
    },
    {
        "name": "NYC Restaurant Week (Winter)",
        "start": "2026-01-20",
        "end": "2026-02-08",
        "category": "Major NYC Event",
    },
    {
        "name": "Black History Month",
        "start": "2026-02-01",
        "end": "2026-02-28",
        "category": "Cultural Observance",
    },
    {
        "name": "Valentine's Day",
        "start": "2026-02-14",
        "end": "2026-02-14",
        "category": "Event / Observance",
    },
    {
        "name": "Presidents' Day",
        "start": "2026-02-16",
        "end": "2026-02-16",
        "category": "Federal Holiday",
    },
    {
        "name": "Women's History Month",
        "start": "2026-03-01",
        "end": "2026-03-31",
        "category": "Cultural Observance",
    },
    {
        "name": "St. Patrick's Day",
        "start": "2026-03-17",
        "end": "2026-03-17",
        "category": "Major NYC Event",
    },
    {
        "name": "Easter Sunday",
        "start": "2026-04-05",
        "end": "2026-04-05",
        "category": "Religious Observance",
    },
    {
        "name": "Earth Day",
        "start": "2026-04-22",
        "end": "2026-04-22",
        "category": "Observance",
    },
    {
        "name": "Tribeca Film Festival",
        "start": "2026-04-15",
        "end": "2026-04-26",
        "category": "Major NYC Event",
    },
    {
        "name": "Cinco de Mayo",
        "start": "2026-05-05",
        "end": "2026-05-05",
        "category": "Cultural Observance",
    },
    {
        "name": "Mother's Day",
        "start": "2026-05-10",
        "end": "2026-05-10",
        "category": "Event / Observance",
    },
    {
        "name": "Fleet Week NYC",
        "start": "2026-05-20",
        "end": "2026-05-26",
        "category": "Major NYC Event",
    },
    {
        "name": "Memorial Day",
        "start": "2026-05-25",
        "end": "2026-05-25",
        "category": "Federal Holiday",
    },
    {
        "name": "LGBTQ+ Pride Month",
        "start": "2026-06-01",
        "end": "2026-06-30",
        "category": "Cultural Observance",
    },
    {
        "name": "Juneteenth",
        "start": "2026-06-19",
        "end": "2026-06-19",
        "category": "Federal Holiday",
    },
    {
        "name": "Father's Day",
        "start": "2026-06-21",
        "end": "2026-06-21",
        "category": "Event / Observance",
    },
    {
        "name": "NYC Pride March",
        "start": "2026-06-28",
        "end": "2026-06-28",
        "category": "Major NYC Event",
    },
]


# ==========================================
# 3. GENERATE DAILY CALENDAR
# ==========================================

calendar_dates = pd.date_range(
    start="2026-01-01",
    end="2026-06-30",
    freq="D",
)

rows = []

for date in calendar_dates:

    active_events = []

    for event in events:
        start_date = pd.Timestamp(event["start"])
        end_date = pd.Timestamp(event["end"])

        if start_date <= date <= end_date:
            active_events.append(event)

    # Identify federal holidays
    holiday_events = [
        event for event in active_events
        if event["category"] == "Federal Holiday"
    ]

    # Collect unique active categories
    active_categories = {
        event["category"] for event in active_events
    }

    # Build daily record
    rows.append({
        "date": date.strftime("%Y-%m-%d"),

        "event_names": "; ".join(
            event["name"] for event in active_events
        ),

        "categories": "; ".join(
            dict.fromkeys(
                event["category"] for event in active_events
            )
        ),

        # General calendar features
        "is_holiday": int(len(holiday_events) > 0),

        "is_event": int(
            any(
                event["category"] != "Federal Holiday"
                for event in active_events
            )
        ),

        # Category-based features for machine learning
        "is_major_nyc_event": int(
            "Major NYC Event" in active_categories
        ),

        "is_cultural_observance": int(
            "Cultural Observance" in active_categories
        ),

        "is_religious_observance": int(
            "Religious Observance" in active_categories
        ),

        "is_general_observance": int(
            "Observance" in active_categories
        ),

        "is_event_observance": int(
            "Event / Observance" in active_categories
        ),

        # Non-federal event categories
        "event_categories": "; ".join(
            dict.fromkeys(
                event["category"]
                for event in active_events
                if event["category"] != "Federal Holiday"
            )
        ),
    })


# ==========================================
# 4. CREATE DATAFRAME & EXPORT CSV
# ==========================================

df = pd.DataFrame(rows)

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==========================================
# 5. OUTPUT SUMMARY
# ==========================================

print("Holiday calendar successfully generated!")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Output: {OUTPUT_PATH}")

print("\nCalendar preview:")
print(df.head(10).to_string(index=False))

print("\nFeature totals:")
feature_columns = [
    "is_holiday",
    "is_event",
    "is_major_nyc_event",
    "is_cultural_observance",
    "is_religious_observance",
    "is_general_observance",
    "is_event_observance",
]

print(df[feature_columns].sum())
