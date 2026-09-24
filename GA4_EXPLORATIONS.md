# GA4 reporting and exploration specification

## Traffic acquisition report
**Scope:** Session default channel group, with secondary dimensions session source/medium and session campaign.

**Metrics:** Sessions, engaged sessions, engagement rate, sessions with key events, session key-event rate, purchase revenue. **Comparison:** January–August of 2024, 2025 and 2026. **Question:** Which channels attract engaged, commercially useful visits rather than volume alone?

## Landing-page engagement
**Dimension:** Landing page. **Metrics:** Sessions, engaged sessions, engagement rate, sessions with key events, purchase revenue. **Segment:** Device category. **Question:** Which landing pages attract visits but underperform at conversion?

## Funnel exploration
**Illustrative event stages:** `session_start` → `view_item` → `add_to_cart` → `begin_checkout` → `purchase`.

The provided funnel CSV reports distinct sessions containing each event, regardless of precise sequence. A true GA4 closed funnel exploration would apply **ordered step definitions** and a chosen scope; its values can differ.

## Device comparison
**Dimension:** Device category. **Metrics:** Sessions, engagement rate, purchase-session rate, purchase revenue.

## Data quality and tagging
The source audit checks duplicate session IDs, missing session references, engagement-rule reconciliation, purchase and lead event alignment and purchase-revenue agreement. In a real implementation, purchase events should carry reliable unique transaction IDs to avoid duplicate revenue.

**GA4 product references:**
https://support.google.com/analytics/answer/12923437
https://developers.google.com/analytics/devguides/collection/ga4/reference/events
