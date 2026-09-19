# Johnny Index System Specification

The Johnny Indexer implements a hierarchical indexing system based on the Johnny Decimal methodology. Files are organized into a nested directory structure with specific index formats at each level.

## Hierarchy Format Strategy

The system defines seven types of organization across 4 levels:

1. **Area** (Level 0) - Groups broad organizational divisions of your life or expertise.
    - Format: `X0-X9` (e.g., `10-19`, `20-29`)
    - Parent: System Root
    - Max: 10 areas per system

1. **Category** (Level 1) - Groups related items within an area by a subject matter.
    - Format: `XY` (e.g., `11`, `12`, `23`)
    - Parent: Area
    - Max: 10 categories per area

1. **Topic** (Level 2) - Main unit of a note in which you keep your actual materials (documents, notes, files). These are topical containers with descriptive names (e.g., `12.21 Electricity, gas, & water`)
    - Format: `XX.YY` (e.g., `11.01`, `11.05`, `12.03`)
    - Parent: Category
    - Max: 100 topics per category

1. **Extension** (Level 3) - Groups Topics further into specialized subdivisions
    - Format: `XX.XX+SUFF` (e.g., `11.05+DOCS`, `12.03+CODE`)
    - Parent: Topic
    - Max: Unlimited, but < 5 is preferred

1. **Subtopic Type 1** (Level 3) - Splits up a topic into smaller pieces of notes
    - Format: `XX.XX-Y*` (e.g., `11.05-1`, `11.05-10`, `12.03-5`)
    - Parent: Topic
    - Max: 100 subtopics per topic

1. **Subtopic Type 2** (Level 4) - Splits up a topic into smaller pieces of notes
    - Format: `XX.XX+SUFF-Y*` (e.g., `11.05+DOCS-1`, `12.03+CODE-15`)
    - Parent: Extension
    - Max: 100 subtopics per extension

1. **The Rest** (Level 4+) - The system has given up. Existence of these files indicates you need to re-organize
    - Format: `Y*` (e.g., `1`, `25`, `100`)
    - Parent: Subtopic Type 1 or Subtopic Type 2
    - Max: Unlimited
