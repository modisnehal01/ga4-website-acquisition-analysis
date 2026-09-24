# Data dictionary and KPI methodology

## Sources and grain

- `ga4_sessions.csv`: exactly one row per simulated `session_id`; acquisition dimensions are **session-scoped**.
- `ga4_events.csv`: exactly one row per recorded synthetic event, with events linked to session IDs.
- Currency: GBP. Transaction values are illustrative product totals excluding shipping, tax and refunds.
- Dates are generated for full 2024, full 2025 and January–August 2026; 2026 is not a full year.

## Core session fields

| Field | Description |
|---|---|
| `session_id` | Unique synthetic session identifier |
| `user_pseudo_id` | Synthetic pseudonymous user identifier, may occur in multiple sessions |
| `session_date` | Date of visit, ISO format |
| `year_month` | Session month, YYYY-MM |
| `session_default_channel_group` | Synthetic session acquisition channel |
| `session_source_medium` | Synthetic session traffic source/medium |
| `session_campaign` | Illustrative session campaign or `(not set)` |
| `device_category` | mobile, desktop or tablet |
| `region` | Broad geographic grouping |
| `landing_page` | First page of synthetic session |
| `page_views` | Number of page_view events recorded in session |
| `engagement_seconds` | Illustrative session engagement time |
| `engaged_session` | 1 if duration >10 seconds, key event, or >=2 pageviews |
| `has_purchase` | 1 if any purchase event occurred |
| `has_lead` | 1 if any generate_lead event occurred |
| `has_key_event` | 1 if purchase or generate_lead occurred |
| `purchase_revenue_gbp` | Sum of purchase events for the session |

## Core event fields

| Field | Description |
|---|---|
| `event_id` | Unique synthetic event ID |
| `event_name` | session_start, page_view, view_item, add_to_cart, begin_checkout, purchase, generate_lead |
| `event_timestamp` | Illustrative event timestamp, ISO datetime |
| `event_value_gbp` | Purchase-event transaction value; zero otherwise |
| `transaction_id` | Unique transaction ID for a purchase event |
| `is_key_event` | 1 for purchase and generate_lead |

## Notes on method

This is a **synthetic GA4-style case study** rather than an actual Google Analytics export. Real GA4 reporting can differ due to identity settings, thresholding, attribution, time zones, consent mode and event collection settings. The project intentionally avoids inferring causation from channel comparisons. A user may be active in more than one reporting year: annual unique-user counts are not additive. The simulated event funnel counts distinct sessions at each stage; it is not a strict GA4 sequence-funnel export.

**Official references:**
- https://support.google.com/analytics/answer/12195621
- https://developers.google.com/analytics/devguides/collection/ga4/reference/events
