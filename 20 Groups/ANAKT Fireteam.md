---
type: "group"
kind: "unit"
aliases:
  - "ANAKT"
  - "The ANAKT Fireteam"
  - "Recombinant Unit-09"
source_series: "Alien Stage"
---

Born from the ashes of the RDA's Phoenix Project, the **ANAKT Fireteam** were six Recombinant soldiers: hybrid beings of human memory and Na'vi flesh, neither alive nor truly dead. Created in the Gardens, an experimental facility masquerading as a training paradise, they were conditioned through psychological warfare that weaponized emotion into obedience and twisted loyalty into obsession. These soldiers were not linked to human pilots like avatars; they were their own resurrected copies, minds transplanted into engineered Na'vi bodies built for speed and strength. Deployed as the unholy blade of Recom Miles Quaritch's alliance with Varang's Mangkwan clan, they became the RDA's perfect instrument of terror in Pandora's Western Frontier.

  

Where the Astikasya's Nine Spears fought to protect life through harmony, the ANAKT moved to a hollow rhythm, their violence a choreographed replay of the ghosts they once were. Each bore a callsign drawn from myth and biology, a name that captured their cursed function: **Ivan, The Scolopendra**, the tactician who turned strategy into a cage; **Sua, The Clematis**, whose silent kills were intimate searches for a connection she could no longer feel; **Mizi, The Witch**, a protector whose empathy became a weapon against her; **Till, The Thornbriar**, chaos raging against the cage of his rebirth; **Hyuna, The Nightshade**, who found a terrible joy in the purity of combat; and **Luka, The Strangler Fig**, the patient manipulator who clothed himself in the Mangkwan's ash-stained faith.

  

Their systematic occupation of Sheltering Falls during the Siege turned sacred ground into a killing field. The clash that followed became legend: hollow ghosts against living souls. Sua fell to Txewan's knife in the mist. Till was drowned in darkness, his kuru severed by Tsa'rawm's spear. Hyuna met a warrior's end in glorious combat with Kaymi. Mizi, broken by truth, vanished into the Spires. Ivan was unmade by the unpredictable love of a family he could not strategize against. Only Luka escaped, wounded and vowing vengeance from the shadows, after a great battle against the combined efforts of the Nine Spears and Syayvi's Scattered Ashes.

> [!note] Since ruled (2026-11-12)
> Till fell to Tsa'rawm and Ketxe, his kuru severed with the AMP suit chainsaw Tsa'rawm stole and made his own. Mizi was burned, blinded and fell from a cliff; she lives, almost a ghost, guiding lost children in the mist. Hyuna fought Sänrri and Kaymi, then Kaymi alone. Luka escaped the Siege and dies at the end of [[The Wild Hunt]].

  

In their end, the ANAKT Fireteam became the ultimate symbol of the RDA's blasphemy: humans reborn without souls, memories walking in sacred skin. The Astikasya whisper that the Great Mother Herself recoils from their touch, finding no pulse of life within them. Their existence is the dark mirror to the Na'vi's deepest fear: the horror of perfect form devoid of spirit. They leave behind a question that haunts the forests and mists of Pandora: *if a being remembers love but can no longer feel its truth, does Eywa still hear its song?*

## Members

```base
filters:
  and:
    - note.type == "character"
    - file.inFolder("10 Characters")
    - note.groups.contains(link("ANAKT Fireteam"))
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

## Notes

- **Ruled 2026-11-16:** The ANAKT is General Ardmore's own unit, built because Quaritch's vendetta made him persona non grata to her. She put them in Mangkwan colors with carte blanche to win the clan away from Varang, with Luka's reprintable body as the selling point. When Ardmore dies in *Fire and Ash* they lose their leash. This supersedes "the unholy blade of Recom Miles Quaritch's alliance" in the paragraph above. See `_inbox/2026-11-16 Why the ANAKT Exists.md`.
