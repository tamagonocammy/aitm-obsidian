---
type: "group"
kind: "faction"
aliases:
  - "Lost Cohort"
source_series: "BanG Dream! It's MyGO!!!!!"
---

> [!info] Synopsis written 2026-11-12 from the notes in this vault. Nothing in it is new canon; gaps are listed under Still open.

The Lost Cohort is the circle that formed around Sänrri while she trained as tsakarem under 'Ipxerey, after she arrived on Pandora as the dreamwalker Dr. Tomori Takamatsu *(The Dreamwalker Years)*. Each member came with a different wound and a different reason. The Mangkwan captured Sänrri, the Cohort and Txafwe and held them for months *(Rulings Log)*. They came home with Sänrri carrying the warning "They are coming" *(Scaled and Icy)*.
### Who they are
- [[Sänrri]]: the circle's center; tsakarem; the Relationship Lore counts her as a member, but her own note does not carry the group tag.
- [[Rängay]]: "Spiritual Musician"; stern ritualist; mate of [[Txafwe]], mother of [[Nìla]] and [[Mawpay]]; once at odds with Kaymi over Sänrri.
- [[Pxayu]]: "Nurturer"; mate and co-parent with Apayì, mother of [[Lawarey]]; afraid of being abandoned.
- [[Apayì]]: "Social Perceptive"; co-parent of Lawarey with Pxayu; posed as Mangkwan to get a message to [[Tsu'lan]].
- [[Pamyaw]]: "Wandering Spirit"; no mate or family given; joined because Sänrri "made things interesting".
### What defines them
They were formed around Sänrri's spiritual training under 'Ipxerey, and each member's profile calls them the "Original Sänrri Cohort" *(Relationship Lore, member profiles)*. They survived the captivity as a unit and, after the Siege, their bonds were "tested and deepened" *(Relationship Lore)*. In captivity they watched sacred rhythms twisted into heresy *(Scaled and Icy)*. Pxayu caught herself mimicking Mangkwan ceremonies, Pamyaw lost her instruments, and Apayì kept spirits up *(member profiles)*. Pamyaw's way of belonging is to come and go and trust she will be understood *(Relationship Lore)*.
### Still open
- [x] Whether Sänrri is a member or the center. Her note has no Cohort tag, so the member table shows only four. **Ruled 2026-11-12:** Sänrri is part of the Cohort. Her note now carries the tag.
- [ ] Whether Txafwe belongs here. He was captured with the Cohort and is Rängay's mate, but his note tags him as Scattered Ashes.
- [ ] Why the group is called "Lost". No note explains the name.
- [ ] How Syayvi relates to the Cohort. The arc summary of Scattered Ashes, Burning Hearts mentions her "friendship with the Cohort" and nothing else says more.

## Members

```base
filters:
  and:
    - note.type == "character"
    - file.inFolder("10 Characters")
    - note.groups.contains(link("The Lost Cohort"))
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
