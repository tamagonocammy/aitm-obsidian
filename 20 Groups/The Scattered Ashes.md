---
type: "group"
kind: "faction"
aliases:
  - "Scattered Ashes"
source_series: "BanG Dream! Ave Mujica"
---

> [!info] Synopsis written 2026-11-12 from the notes in this vault. Nothing in it is new canon; gaps are listed under Still open.

The Scattered Ashes are the exiles Syayvi gathered from inside the Mangkwan, after she and her twin Tìmeyo took shelter there and saw the heresy *(Blurryface era)*. The Relationship Lore calls them "an exile's found family", built around shared exclusion. They came home with the Lost Cohort and the warning "They are coming", proved themselves in the Siege, and then began to separate. Syayvi and Nì'syu stay at the Falls with Sìlpey on the way, and Tìmeyo and Yawyay leave for the Ta'unui reef *(Siege of the Falls)*.
### Who they are
- [[Syayvi]]: leader; The Penitent, Ninth of the Nine Spears with the Ashen Spear; twin of Tìmeyo, formerly named Tswa'avä in exile; mate of Nì'syu, pregnant with Sìlpey.
- [[Tìmeyo]]: twin of Syayvi; Tìmeyo and Kerevi are a DID system who share one note. Once destined to be tsakarem and Kaymi's mate. Leaves with Yawyay for the reef after the Siege.
- [[Nì'syu]]: also 'Awll, who took Nì'syu's name herself and knows who she is; mate of Syayvi.
- [[Txafwe]]: Tayrangi rhythm-keeper from the Eastern Sea; mate of [[Rängay]], father of Nìla and Mawpay; captured with the Cohort.
- [[Yawyay]]: from the Ta'unui coastal clan; a drummer who sought the Mangkwan willingly and lost faith in them; Tìmeyo's mate after the Siege.
### What defines them
Their shared ground is exclusion: the twins' exile for killing their father, the Mangkwan's corruption, and the slow work of being taken back in *(Relationship Lore)*. Kaymi watched them closely from their arrival, especially Syayvi *(Kaymi's profile)*. Kerevi knows the Mangkwan technique and would never use it on the clan, because of Syayvi *(Rulings Log)*. Their loyalty to each other held through the Siege *(Relationship Lore)*. The Ashes "proved themselves during the siege despite being exiles" *(Siege of the Falls)*.
### Still open
- [ ] Why the group is called the Scattered Ashes. No note explains it.
- [x] Nì'syu's own note still says 'Awll was forced into her sister's identity. The Rulings Log says she took the name herself *(Rulings Log, Nì'syu's note)*. **Ruled 2026-11-12:** fixed on her note; she took the name herself.
- [ ] Whether 'Awll went into exile with Syayvi and Tìmeyo. The summary of Scattered Ashes, Burning Hearts says yes; the Prologue era names only the twins *(Open Questions)*.
- [ ] Txafwe is not an exile in his own story. He joined the Astikasya for Rängay, so how he came to be an Ash is not told.
- [ ] Whether Yawyay's burned village is the Ta'unui reef she returns to. Her note says Quaritch burned her village; the Rulings Log says the reef is her home.
- [x] The order of the twins' tragedy: the Prologue says their father's neglect led to Luey's death and then they killed him, while Tìmeyo's note says Kerevi formed after killing him "to spare dying mother". **Ruled 2026-11-12:** Luey dies. The Prologue's order stands.

## Members

```base
filters:
  and:
    - note.type == "character"
    - file.inFolder("10 Characters")
    - note.groups.contains(link("The Scattered Ashes"))
views:
  - type: table
    name: Members
    order:
      - file.name
      - note.epithet
      - note.role
      - note.ikran
      - note.status
      - note.mbti
```
