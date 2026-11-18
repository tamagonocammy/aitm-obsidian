# AITM — Na'vi Name Audit
### Every Na'vi name in the project, checked against Na'vi sound rules and Reykunyu (October 2026)

> **What was checked.** 55 given names, 23 family names, 28 parent names (from the *te … 'ite/'itan* full names), 43 ikran names and 11 clan names, collected from the roster, the character database, the profiles and the MBTI reference. Each one was run through (1) a Forest Na'vi phonotactics checker and (2) Reykunyu's full dictionary for hidden meanings. The checker was first tested on all 3,254 Reykunyu entries and passed every one except nine known oddities (interjections like *oìsss*, and a few canon exceptions), so a name it flags really does break the usual rules.
>
> **The Na'vi sound rules in one paragraph.** A syllable is (onset) + vowel + (one final consonant). An onset is one consonant, or a cluster of **f / s / ts** + another consonant (*sk, fp, tsy, fr*…). The vowels are *a ä e i ì o u*, the diphthongs are only **aw ay ew ey**, and *ll*/*rr* count as vowels but always need a consonant before them. A syllable may end in *p t k px tx kx ' m n ng l r* — never *f s ts h v z*. No *b d g* (Forest Na'vi), no lone *x*, no two identical vowels in a row.

> **Decided (October 28, 2026).** **Eantu**, **Mawpay**, **Kxuryo**, **Awsun**, **Lokxtu**; Tswesya's parent is **Mawnä**; Sänume's ikran is **Payarä**; the accent reference title becomes ***Lì'fya Astikasyayä***. The exact find-and-replace list for the character docs is in `AITM_Name_Fixes.md`. Still open: whether the Flying Troupe's *Tswayona* should become *Tswusayona* (section 5).

---

## 1. Names that break the sound rules

| Name | Where | Problem | Closest valid spelling |
|---|---|---|---|
| **Ean'tu** (vs **Eantu**) | Tsu'ong & Ketxe's son | *n'* + *t* cannot split into valid syllables (a glottal stop cannot start a cluster). **Eantu** (e-an-tu) is valid. | **Eantu**, which the roster already uses |
| **Mowpay** | Txafwe & Rängay's daughter | *ow* is not a Na'vi diphthong (only *aw ay ew ey*), and *w* cannot end a syllable after *o* | **Mawpay** (closest sound) or **Mowapay** |
| **Kxurryo** | Syulang's mother (*Kxurryo'ite*) | *rr* needs a consonant before it; after *u* it has none | **Kxuryo** (kxur-yo), same sound with one *r* |
| **Äwsun** | Pxayu's ikran | *äw* is not a diphthong | **Awsun** or **Ewsun** |
| **Loxtu** | Tswesya's ikran | a lone *x* does not exist in Na'vi (only *px tx kx*) | **Lokxtu** (keeps the sound) or **Loktu** |

None of the suggested spellings collides with an existing Na'vi word. A fun footnote: the canon clan name **Mangkwan** breaks the same rule (*kw* is not a valid cluster), which is why Reykunyu also lists the Na'vi-proper spelling *Mangkuan*.

## 2. Inconsistencies between documents

**Ean'tu / Eantu.** The roster and the relationships quick reference have *Eantu*; the character database and the accent reference have *Ean'tu*. Section 1 suggests settling on **Eantu**.

**Tswesya's parent.** The roster and database say *Tswesya te Meitayä **Mawnä**'itu*; the MBTI reference says *Tswesya te Meitayä **Txayo**'itu*. (*Txayo* is a real word: "field, open terrain, plain.")

**Sänume's ikran.** Her profile says ***Payarä***; the database says ***Payri*** "(shares name with Atanvi's ikran)." One of the two needs to win.

**"Lì'fya Astikasyaä."** The accent reference's subtitle puts *Astikasya* in the genitive as *Astikasyaä*. Names ending in a vowel other than *o* or *u* take **-yä**, and the canon parallel is *lì'fya* → *lì'fyayä*, so it should be ***Lì'fya Astikasyayä***, "the language of the Astikasya."

**The *'itu* ending.** Tswesya's full name ends in *'itu*, while canon only has *'ite* "daughter" and *'itan* "son" (*'eveng* is "child"). Reykunyu has no *'itu*. If it is a deliberate gender-neutral form for Tswesya, it reads beautifully and the clan can own it as an Astikasya usage; just know it is an AITM invention, not a Frommer word.

---

## 3. Names that are real Na'vi words

Like *Flor* or *Luz* in Spanish, these names are ordinary words. Some look deliberate; all of them are worth knowing.

**Given names**
**Atanvi** — "ray" (of light). The Merciful.
**Rewon** — "morning."
**Lamaytxa** — "flood." Matches her profile's own explanation.
**Sänume** — "teaching, instruction" ('Ipxerey's finest student).
**Syulang** — "flower."
**Tswesya** — "current (of a body of water)"; as a si-verb, "flow." A bassist named Flow.
**Syayvi** — "luck, chance." The Penitent.
**Sìlpey** — "**hope**" (verb: *sìlpey* "to hope"). Syayvi's unborn child is named Hope.
**Txewì** — listed by Reykunyu as a male Na'vi name, from a LearnNavi forum list of names, not a canon character.

**Family and parent names**
**Hafyon** (Katirì, Waynhì, Oarä) — "wisdom." The storyteller's family is the House of Wisdom.
**Tìrol** (Eyfuwen's father) — "song." Eyfuwen is literally *the son of Song*.
**Txep** (Tsu'ong's father) — "**fire**." Tsu'ong is *the son of Fire*, which answers the open question about his *Tempered Spear*: **tukru txepä**, "the spear of fire," is now the obvious Na'vi name for it.
**Txayo** (Tswesya's parent, MBTI version) — "field, plain."
**Kamun** (Txolaw's father) — a canon male Na'vi name.
**Zeswa** (Tìfyaw's family) — "grass," and also the Zeswa clan of the Upper Plains (from *Frontiers of Pandora*, marked unconfirmed by Reykunyu).

**Ikran names**
**Telisi** (Rawìl) — "whirlwind."
**Tìrol** (Ketxe) — "song." Ketxe's ikran shares a name with Eyfuwen's father.
**Tìfnu** (Syayvi) — "quiet, silence."
**Fe'pey** (Tìmeyo) — "to feel dread, to expect something bad." Painfully fitting.
**Yawntu** (Yawyay) — "**loved one**."
**Ìley** (Nìla) — "war cry."

## 4. Clans

Canon clans that check out in Reykunyu: **Omatikaya**, **Metkayina**, **Tipani**, **Tawkami**, **Ta'unui** (Yawyay's), and from *Frontiers of Pandora*, **Kame'tire**, **Aranahe** and **Zeswa** (those three are marked unconfirmed by Frommer, which only matters if AITM wants strict film canon). **Tayrangi** (Txafwe's clan) is not in Reykunyu; **Astikasya** is AITM's own and passes every sound rule.

## 5. The Flying Troupe (*Aytepvi Tswayona Pongu*)

All 27 Troupe names pass the sound rules. Hidden meanings: **Layon** "black"; **Herwì** (Teysaw's family) "snow"; **Kxitx** (Seytu's father) "**death**," so Seytu is literally *the son of Death*; **Venu** (Roneyu's parent) "foot"; **Pongu** "group of people, party." Roneyu also uses the *'itu* ending (see section 2).

The troupe's own name parses as *ay-* + *txepvi* "spark" (lenited: **aytepvi** "sparks") and *pongu* "group," both correct. **Tswayona** is the one question: if it is meant as "flying," Na'vi cannot put the attributive *a* straight onto a verb; it needs the active participle, which Reykunyu's infix slot for *tswayon* (tsw.ay.on) gives as **tswusayon**: *Aytepvi Tswusayona Pongu*, "the Flying Troupe of Sparks." If *tswayona* was meant as something else, it stays.

## 6. Everything else

Every other name passed both checks cleanly, including the tricky ones: *Tsawtral* (tsawt-ral, like canon *Kelutral*), *Kll'i'a*, *Txoewll*, *Mowa'tal*, *Haykxa*, *Ìkìtä'*, *Txi'ra*, *Tsyokanì*, *Kerevi* and *Tswa'avä*.

*Checker and data: Reykunyu (reykunyu.lu) word list and parser; sound rules per the project's Na'vi reference and Kelutral. Part of the AITM project files.*
