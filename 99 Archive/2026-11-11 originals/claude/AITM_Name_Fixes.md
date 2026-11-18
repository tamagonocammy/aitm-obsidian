# AITM — Name Fixes to Apply
### Find-and-replace list for the character docs (decided October 28, 2026)

> These are the spelling decisions from the Na'vi name audit (`AITM_Navi_Name_Audit.md`). Claude's own reference docs (case sheet, Nine Spears, proverbs, study tool) already use the new spellings. The docs below are Millie's originals, so the replacements are listed here to apply in the master copies, then re-upload. The "Seen in" column lists where each spelling was found in the project copies; a whole-word search across every doc is still the safest way to catch them all.

| Find | Replace with | Why | Seen in |
|---|---|---|---|
| `Ean'tu` | `Eantu` | *n'* + *t* breaks Na'vi syllable rules; the roster already says Eantu | Astikasya_Character_Database, AITM_MBTI_Reference, AITM_Astikasya_Accent_Reference |
| `Mowpay` | `Mawpay` | *ow* is not a Na'vi diphthong | 01_Clan_Overview_and_Roster, Astikasya_Character_Database, AITM_MBTI_Reference, AITM_Relationships_QuickRef, AITM_Relationships_Lore, 04_Character_Profiles_Groups_and_Others, AITM_05_Factions_Profiles, AITM_Astikasya_Accent_Reference (and likely AITM_01_Clan_Overview_and_Groups) |
| `Kxurryo` | `Kxuryo` | *rr* cannot follow a vowel | 01_Clan_Overview_and_Roster, Astikasya_Character_Database, Syulang's profile (03 / AITM_04) |
| `Äwsun` | `Awsun` | *äw* is not a diphthong | 04_Character_Profiles_Groups_and_Others, AITM_05_Factions_Profiles, Astikasya_Character_Database (where it appears garbled as `Ã„wsun`, see below) |
| `Loxtu` | `Lokxtu` | a lone *x* does not exist in Na'vi | Astikasya_Character_Database (and Tswesya's profile, if it names the ikran) |
| `Txayo'itu` | `Mawnä'itu` | Tswesya's parent is Mawnä | AITM_MBTI_Reference |
| `Payri (shares name with Atanvi's ikran)` | `Payarä` | Sänume's ikran is Payarä | Astikasya_Character_Database (Sänume's entry only; Atanvi's ikran stays Payri) |
| `Lì'fya Astikasyaä` | `Lì'fya Astikasyayä` | genitive after *a* is *-yä* | AITM_Astikasya_Accent_Reference (subtitle) |

**One more thing in the database.** `Astikasya_Character_Database.md` has a text-encoding problem: every accented letter shows up garbled (*Mìreya* appears as `MÃ¬reya`, *Notä* as `NotÃ¤`, *Sänrri* as `SÃ¤nrri`). This happens when a UTF-8 file is opened as Latin-1 somewhere along the way. Re-saving the master copy as UTF-8 before uploading, or replacing `Ã¬` → `ì`, `Ã¤` → `ä`, `ÃŒ` → `Ì`, `Ã„` → `Ä`, `Å«` → `ū`, fixes it.

*Part of the AITM project files.*
