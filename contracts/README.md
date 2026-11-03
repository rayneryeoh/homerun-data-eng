# Dataset conventions

These are starting conventions. Final schemas should follow inspection of the source datasets.

## Housing master

Use one row per block, with a stable internal `block_id`, original source identifiers, block/address fields, postal code, coordinates and year completed.

Store postal codes as strings to preserve leading zeros. Document the coordinate reference system and coordinate order.

If dwelling counts are supplied by flat type, use a related table with one row per `block_id + flat_type`, rather than repeating the block attributes.

## Resale transactions

Use one row per recorded transaction. Retain original source fields and the available transaction date precision. Do not invent a day if the source supplies only a month.

Map transactions to `block_id` and preserve unresolved or ambiguous address matches for review.

## Active resale listings

Use one record per source listing per observation when retaining history. Preserve source name, source listing ID, observation time, status and available listing dates.

Track when a listing was last observed. A listing missing from a later collection should not automatically be classified as sold. Multiple listings may describe the same property.

## Accessibility exports

Suggested CSV fields:

```text
block_id,schools_5min,schools_10min,schools_15min,feature_snapshot_id
```

Use one row per block per snapshot. Counts are nonnegative integers; missing results must remain distinguishable from zero. For cumulative counts, enforce `schools_5min <= schools_10min <= schools_15min`.

Record the school definition, travel mode, direction of travel and counting/deduplication rules. These affect the meaning of each feature.

For each snapshot, keep a manifest next to its exported CSV. Use `accessibility_manifest.example.json` as a starting point and replace all placeholders with actual run information. The manifest preserves provenance; it does not guarantee identical results if input data or the licensed execution environment cannot be recovered.

