# Data notes

The source snapshot contains 21,083 entry records. After trimming lookup-key edge whitespace and grouping identical headwords, the MDX has 19,831 keys; 1,147 keys contain multiple records. Record IDs and definitions are retained.

## Explicit correction

Source ID `6357914a7f1ba0e22236b65a` has a whitespace-only headword and heading, the POS `NOUN`, and gloss `brothers`. The maintainer requested `aħwa` as its lookup key and displayed heading. This is a local editorial correction, not a verified upstream correction. `--no-corrections` disables it and uses an explicit untitled placeholder.

## Retained source anomaly

Source ID `60e9b74509445f3399213e31` uses the complete text `lejliet; acc. to my dictionarues the form is: lejlet` as its headword. This appears to be a comment entered as lexical data, including the original typo. It is retained rather than silently edited or deleted. Separate ordinary entries for `lejlet` and `lejliet` are present.

## Index behavior

The base MDX writer sorted raw, case-sensitive keys while declaring case-insensitive lookup. In the earlier build there were 278 ordering inversions under lowercase/ASCII-punctuation-stripped comparison; a simulated lookup for `badbad` landed at `b'risq`.

The local adapter orders normalized keys before record offsets and blocks are finalized, and explicitly declares `StripKey="Yes"`. All keys pass a binary-search regression check. The exact Maltese spelling and all definitions remain intact; normalization affects ordering, not displayed headwords.

The MDX does not contain the native dictionary's inflected-form indexes or recreate its approximately 4.5 million word-form searches.
