import json, os
from common import *
out = json.load(open(os.path.join(BUILD, 'pilot_out.json')))
for d in ['00 Home','10 Characters','20 Groups','30 World','40 Story/Eras','40 Story/Arcs','40 Story/Scenes','50 Language','60 Meta','90 Sources','99 Archive','_templates']:
    os.makedirs(os.path.join(V,d), exist_ok=True)

write('00 Home/Cast.base', '''filters:
  and:
    - note.type == "character"
    - file.inFolder("10 Characters")
properties:
  file.name:
    displayName: Name
  note.navi_name:
    displayName: Full Na'vi name
  note.source_name:
    displayName: Source
  note.mbti:
    displayName: MBTI
views:
  - type: table
    name: Everyone
    order:
      - file.name
      - note.navi_name
      - note.family
      - note.role
      - note.ikran
      - note.birthday
      - note.mbti
  - type: table
    name: By family
    groupBy:
      property: note.family
      direction: ASC
    order:
      - file.name
      - note.role
      - note.source_name
      - note.source_series
  - type: table
    name: Nine Spears
    filters:
      and:
        - note.groups.contains(link("Nine Spears of the Mists"))
    order:
      - file.name
      - note.epithet
      - note.weapon
      - note.ikran
''')
write('00 Home/Rulings.base', '''filters:
  and:
    - note.canon == "tentative"
views:
  - type: table
    name: Waiting on a ruling
    order:
      - file.name
      - note.type
      - file.folder
''')
write('00 Home/Home.md', frontmatter({'type':'home'}) + '''# Avatar: Into the Mists

The front door. Everything in the vault is reachable from here.

## Cast

![[Cast.base]]

## Story

Timeline, eras, arcs and scenes arrive in phase 4.

## Rulings

Things waiting on a decision from you: [[Open Questions]]

![[Rulings.base]]

## Language

- [[Na'vi Name Case Forms]]
- [[Proverbs and Sayings of the Falls]]
- [[Astikasya Accent Reference]]

## About this vault

- [[How This Vault Works]]
- [[Vault Design]]
''')
q = '\n'.join(f'- [ ] {c}' for c in out['conflicts'])
write('00 Home/Open Questions.md', frontmatter({'type':'meta'}) + f'''Things only Millie can decide. Tick one off when it is ruled, and fix the note it points to.

## Conflicts between source files

{q}

## Missing facts

- [ ] **[[Lì'may]] — source series.** Her source name is Miyako Samaya-Takamatsu, and no file says which series Miyako comes from. `source_series` is empty on her note.
- [ ] **[[Rawìl]] and [[Notä]] — source series.** Left empty. They are fan characters by a friend of yours rather than Witch from Mercury canon; tell me how you want that written.

## Structure

- [ ] **Combined entries.** Tìmeyo and Kerevi, Nì'syu and 'Awll, Txewan and Txewì each become one note with the second name as an alias. Say so if any should be two notes.
''')
write('00 Home/How This Vault Works.md', frontmatter({'type':'meta'}) + '''Your manual. Short on purpose.

## The three tools

- **Folders** say what kind of thing a note is. A character lives in `10 Characters` no matter which family or faction they belong to.
- **Links** say what a note is connected to. Type two opening square brackets and start typing a name.
- **Properties** are the facts at the top of a note, between the `---` lines. Tables are built from them.

## Things you will see

- **A link in a faded color** points at a note that does not exist yet. Click it and Obsidian creates the note. During the migration many links look like this until their notes are built.
- **Aliases.** `[[Tomori]]` and `[[Sänrri]]` open the same note, because "Tomori" is listed under `aliases` on Sänrri's note.
- **A table inside a note** (like the member list on [[Samaya]]) is a Base. It is a live query over properties. You never edit the table; you edit the notes and the table follows.
- **Backlinks.** Open the right sidebar on any character to see every note that mentions them.

## How to add a character

1. Create a note in `10 Characters` named with the Na'vi name alone.
2. Run "Templates: Insert template" from the command palette (Cmd+P) and pick **Character**.
3. Fill in what you know. Leave the rest blank. Delete nothing; an empty property is fine.
4. Set `family` to a link in quotes, like `"[[Samaya]]"`. The character then appears on that family's table and in the Cast.

## How to mark something as not settled

Set `canon` to `tentative`. It shows up under Rulings on [[Home]]. Use `discarded` for an idea you replaced but want to keep.

More sections get added here as each phase lands.
''')

T = lambda d, body='': frontmatter(d).replace('""','') + body
def tmpl(keys, body):
    return '---\n' + '\n'.join(keys) + '\n---\n' + body
write('_templates/Character.md', tmpl(['type: character','aliases: []','navi_name:','source_name:','source_series:','family:','groups: []','epithet:','role:','weapon:','ikran:','birthday:','age:','mbti:','status:','canon: confirmed'],
 '\n## Profile\n\n\n## Relationships\n\n\n## Name forms\n\n\n## Notes\n'))
write('_templates/Group.md', tmpl(['type: group','kind:','aliases: []','source_series:'], '\n## Members\n\n\n## Notes\n'))
write('_templates/Place.md', tmpl(['type: place','aliases: []','region:','canon: confirmed'], '\n## Description\n\n\n## Customs\n\n\n## Notes\n'))
write('_templates/Arc.md', tmpl(['type: arc','era:','anthem:','status: outline','canon: confirmed'], '\n## Overview\n\n\n## Structure\n\n\n## Open threads\n'))
write('_templates/Scene.md', tmpl(['type: scene','title:','arc:','era:','characters: []','song:','language:','translation_of:','status: draft','canon: confirmed'], '\n'))
