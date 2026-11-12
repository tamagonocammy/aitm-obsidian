---
type: "meta"
---
Your manual. Short on purpose.

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

## Where things live

- `10 Characters`: one note per person. Named by the Na'vi name alone.
- `20 Groups`: families, factions, the clan, and [[Relationship Lore]].
- `30 World`: places, customs, technology.
- `40 Story`: the [[Timeline]], then `Eras`, `Arcs` and `Scenes`.
- `50 Language`: the Na'vi references, kept whole.
- `60 Meta`: notes about the project itself.
- `99 Archive`: every original file, untouched. Hidden from search and the graph on purpose.
- `_inbox`: drop anything new here if you do not know where it goes yet.

## How to file a new scene

1. Create the note in `40 Story/Scenes`, named with the scene's title.
2. Insert the **Scene** template.
3. List who appears under `characters`, each as a quoted link: `"[[Sänrri]]"`. That one list is what makes the scene show up under "Appears in" on each of their notes.
4. Set `arc` and `era` the same way if you know them. If you do not, leave them empty and the scene appears under "Needs placing" on [[Home]].
5. For a translation, put the original in `translation_of` and set `language` to `es` or `en`.

Write the prose below the properties. You do not need to link names inside the prose.

## How to change a fact

Edit the property on the note. Every table that shows it updates by itself. If the change overrules something older, add a line under Notes saying what you ruled and when, so the reason survives.

## How to keep an old version

Put the old text in a folded box so it stays out of the way:

```
> [!quote]- Earlier version
> the old text here
```

## The daily habit

When an idea arrives and you do not know where it belongs, write it in `_inbox`. Filing can wait; losing it cannot.

