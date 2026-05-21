# Johnny Decimal System: Technical Specification & Capabilities

## Executive Summary

Johnny Decimal is a hierarchical organizational system designed to help users "find things, quickly, with more confidence, and less stress." It applies universally across personal and professional contexts by imposing deliberate constraints that reduce cognitive load and decision-making friction.

The core principle: assign unique numerical IDs to everything, organized through a three-tier structure with forced limitations that maintain simplicity while scaling to complex needs.

---

## 1. Core Architecture

### 1.1 Three-Tier Hierarchical Structure

Johnny Decimal organizes information through three nested levels, analogous to physical storage:

#### **Areas (Shelves)**
- Represent broad "areas of your life" or expertise
- Numbered in ranges of 10: `10-19`, `20-29`, `30-39`, etc.
- Examples: `10-19 Life admin`, `20-29 Home business`, `30-39 Tennis club`
- Maximum of 10 areas per system
- Should be expansive enough to accommodate growth within that domain

#### **Categories (Boxes)**
- Sub-divisions within each area
- Numbered individually: `11`, `12`, `13`, etc. (within their area range)
- Contain related collections: "travel documents," "marketing material," "facilities maintenance"
- Maximum of 10 categories per area (100 categories total)
- **Most important Johnny Decimal concept** — where actual work and decisions happen
- Preference for breadth over depth: compress similar items into single categories rather than creating granular subdivisions

#### **IDs (Folders)**
- Numbered with format `XX.XX` (two digits, decimal, two digits)
- Example: `15.23 Trip to NYC`
- Range: 00-99 per category (up to 100 possible IDs per category)
- Represent specific projects, items, or topics
- Function as "manila folders" containing all related materials regardless of format

### 1.2 ID Numbering Scheme

**Standard Format:** `AC.ID`
- **First two digits (AC):** Area and Category identifier
  - First digit: Area (0-9)
  - Second digit: Category within that area (0-9)
- **Last two digits (ID):** Sequential identifier within category (00-99)
- **Example:** `15.23` = Area 1, Category 5, ID 23

**Total capacity:** 10 areas × 10 categories × 100 IDs = 10,000 unique identifiers per system

### 1.3 Design Philosophy

**Four Core Principles:**

1. **Limit Your Choices**
   - Maximum 10 folders at area and category levels
   - Prevents sprawling directory structures
   - Reduces decision-making paralysis
   - Helps users identify correct locations confidently

2. **Embrace Beneficial Friction**
   - Creating new categories requires deliberate effort
   - Numbering assignments prevent casual expansion
   - Once at ID level, folder creation is unrestricted
   - Friction forces thoughtful organization at structural levels

3. **Flexibility Over Dogmatism**
   - Adapt the system to individual needs
   - Core principle: does it help you find things?
   - System serves users, not vice versa

4. **Time Investment Yields Dividends**
   - Setup and maintenance require upfront effort
   - Returns multiply through reduced retrieval friction
   - Prevents long-term organizational chaos

---

## 2. Core Components & Implementation

### 2.1 The Index (JDex)

**Purpose:** "The master record of every ID in a system"

**Critical Functions:**
- Prevents duplicate ID creation across multiple storage locations
- Unified tracking for items stored in file systems, email, cloud services, and physical locations
- System memory documenting organizational decisions
- Acts as the primary reference point, not the file system

**Implementation:**
- Store in notes application (Bear, Obsidian, Simplenote, etc.)
- Create new note for each ID before creating corresponding folders/files
- Each entry includes:
  - ID (required)
  - Title (required)
  - Description (optional) — clarifies purpose for future reference
  - Location (optional) — where physical/digital item exists
  - Relates to (optional) — links to connected notes
  - Keywords (optional) — improves searchability

**Key Principle:** "Your filesystem is not your JDex." The index is your system's truth source.

**Searchability Enhancement:**
- Typing category number + period filters to that section
- Keywords enable instant retrieval
- Full-text search across centralized repository

### 2.2 File Organization & Naming

**Directory Structure:**
```
[Area]
├── [Area][Category]
│   ├── [Area][Category][ID] [Title]
│   │   ├── [YYYY-MM-DD] [Description]
│   │   └── ...
│   └── ...
└── ...
```

**File Naming Convention:**
- Prefix files with date: `YYYY-MM-DD Description`
- Organize into subfolders by claim date or event date
- Example: Travel insurance folder (`15.23 Travel insurance`) contains `2024-08-08 NYC lost bag` subfolder with relevant PDFs

**Subfolder Guidelines:**
- One additional organizational level makes sense
- If getting too busy, split into multiple IDs rather than creating deep hierarchies
- Balance between structure and simplicity

### 2.3 Notes Management

**Philosophy:**
"There's already a note for each ID. Just type more words in it."

**Advantages:**
- Efficiency: open notes app, search ID, type
- Eliminates "mental heaviness" of traditional document creation
- Centralizes related details that don't fit traditional files

**Examples of Note Content:**
- Real estate category: agent phone numbers, deposit references, task lists alongside lease PDF
- Travel category: agent contact info, booking confirmations, research notes

**Metadata Strategy:**
- Description: clarifies note's purpose
- Location: indicates where physical/digital item exists
- Relates to: links connected notes
- Keywords: ensures discoverability

**Searchability:**
- Typing category number and period filters notes to that section
- Keywords create instant retrieval paths

---

## 3. System Expansion Techniques

### 3.1 Multiple Systems (SYS.AC.ID Format)

**Purpose:** Manage two or more separate Johnny Decimal systems

**Format:** `SYS.AC.ID`
- System identifier: three characters `[A-Z][0-9][0-9]`
- Range: A00 to Z99
- Total capacity: 2,600 distinct systems
- Example: `H01.11.11` (Home system) vs `W01.11.11` (Work system)

**When to Use:**
- Distinct systems that do not overlap
- Separate personal and work domains
- Independent organizational needs without shared tools

**JDex Considerations:**
- If all indexes share same tool, use full `SYS.AC.ID` identifier
- If separate tools used (different apps), simpler naming may suffice
- Full identifier essential when distributing files externally

**File System Organization:**
- Store each system in dedicated folder: `D85 Johnny.Decimal`
- Within folder, typically don't repeat system identifier in subfolder names
- Use complete identifier for external file references

**Best Practice:**
Avoid creating multiple systems unnecessarily. "Always prefer to 'fill up' an existing system. More systems equals more complexity." Consider other expansion methods first.

### 3.2 Expand an Area

**Purpose:** Add organizational depth to one area that requires more than 10 categories

**Applicable Scenarios:**
- Students managing numerous classes across years/semesters
- Freelancers handling many clients with multiple projects each
- Areas requiring complex hierarchical structures

**Core Rules:**
1. All IDs must start with expanded area number
2. Expand only one area — keep rest of system standard
3. Use format within area range (e.g., 70000-79999 for area 70-79)

**Implementation Guidelines:**
- Use alphabetical ordering where applicable (client names)
- Leverage dates in yyyy-mm-dd format for chronological organization
- Stop using numbers when burdensome; use natural hierarchies
- Create templates for repetitive processes (numbered 10, 20, 30)
- Adopt existing codes rather than inventing new ones
- Document custom scheme in JDex

**What Changes:**
- Items may lack sequential numerical IDs
- JDex becomes less critical if hierarchy is naturally discoverable
- Documentation of scheme remains valuable

### 3.3 Extend the End (AC.ID+SUB Format)

**Purpose:** Handle categories exceeding 100 IDs or IDs requiring repetition

**Format:** `AC.ID+SUB`
- Add sub-identifier after main ID with plus sign
- Sub-identifier uses short code (initials preferred over abbreviations)

**Use Cases:**
- Family tracking: `11.24+JEM` (Jemima's dental/vision visits)
- Project locations: `72.02+X01` (specific data centers)
- Repeating items: `22.00+0001` through `22.00+9999` (sequential blog posts)

**JDex Recording:**
- Include full sub-ID in note title: `11.24+JEM Jemima's eyes, ears, & teeth`
- Allows searching by `+JEM` to find all related entries
- Can create additional notes with `+` if single note becomes unwieldy

**File System Flexibility:**
- Store items directly in ID folder with coded subfolders per sub-ID
- Alternative: keep everything in subfolders for cleaner appearance
- Choose consistent approach and apply uniformly

**Code Selection:**
- Select short, memorable code (initials over abbreviations)
- Example: `+JMD` for Jemima Matilda Decimal
- Use consistently across system

**Constraints:**
- Cannot combine with "expand an area" technique
- Optional to record sub-IDs in JDex
- Frequent use suggests system design needs revision
- If extending end becomes common, consider multiple systems or expanding entire area

---

## 4. Design Approaches

### 4.1 Top-Down Design

Start with major areas, then subdivide into categories:
1. Define 10 broad areas of life/work
2. Within each area, create up to 10 categories
3. Create IDs within categories as needed

**Advantage:** Overall structural clarity before implementation

### 4.2 Bottom-Up Design

Create categories organically, then group into areas:
1. List all categories you need
2. Group related categories into areas
3. Assign area numbers

**Advantage:** Reflects actual needs rather than theoretical structure

---

## 5. Best Practices

### 5.1 Category Design

**Breadth Over Depth:**
- Compress similar items into single categories
- Instead of separate `investments`, `budget`, `savings` categories, use `money`
- Reduces decision-making friction

**Descriptive Naming:**
- Use clarity: "Electricity, gas, & water" vs generic terms
- Helps future self understand category purpose
- Aids in memory and retrieval

### 5.2 ID Naming

**Specificity:**
- Example: `15.52 Trip to NYC` (specific) vs `15.52 Travel` (generic)
- Immediately conveys content and context

**Scalability:**
- Won't exhaust 99 available IDs per category unless definitions too broad
- If approaching limits, redesign category structure

### 5.3 Folder Depth Management

**Minimal Subfolder Structure:**
- One additional level beyond ID reasonable
- If too complex, split into multiple IDs
- Avoid nested folder hierarchies

### 5.4 System Maintenance

**The Librarian Role:**
Oversee system maintenance and updates. Investment in this role "repaid many times over" in organizational benefits.

**Maintenance Tasks:**
- Review and update JDex regularly
- Ensure ID assignments remain consistent
- Prevent folder drift and reorganization
- Document system decisions and standards

---

## 6. Content Types & Storage

### 6.1 Supported Content

Johnny Decimal accommodates all content types equally:
- **Files:** Documents, spreadsheets, presentations
- **Emails:** References to email messages or email-based content
- **Notes:** Centralized note storage with JDex links
- **Physical items:** References to physical storage locations
- **Metadata:** Descriptions, locations, relationships, keywords

### 6.2 Storage Locations

Single ID can reference items across multiple storage locations:
- File system folders
- Email services
- Cloud storage (Google Drive, Dropbox, etc.)
- Physical locations (desk drawers, filing cabinets)
- Note applications

JDex solves the problem of not knowing where items exist across platforms.

---

## 7. System Capacity

### 7.1 Single System Limits

- **Theoretical maximum:** 10,000 unique IDs (10 areas × 10 categories × 100 IDs)
- **Practical capacity:** Much smaller due to deliberate constraints
- **Actual usage:** Most systems use 1,000-3,000 IDs

### 7.2 Scaling Beyond Single System

**When to Expand:**
- When system reaches capacity across multiple categories
- When true separate domains exist (home/work)
- When isolation prevents confusion

**Expansion Options (in order of preference):**
1. Extend the end (simplest)
2. Expand an area (moderate)
3. Create multiple systems (most complex)

---

## 8. Integration & Interoperability

### 8.1 Command-Line Integration

Johnny Decimal supports command-line workflows through consistent naming and numbering schemes that enable automation.

### 8.2 Email Integration

Email management strategies exist for integrating email-based content into Johnny Decimal structure, with IDs serving as reference points in email archives.

### 8.3 Note Applications

Compatible with multiple note applications:
- Bear
- Obsidian
- Simplenote
- Standard markdown files
- Custom database implementations

### 8.4 Database Implementations

Alternative JDex implementations:
- Single notes
- Note database formats
- Spreadsheet-based indexes

---

## 9. System Success Metrics

**Primary Goal:** "Find things, quickly, with more confidence, and less stress"

**Measurable Improvements:**
- Reduced search time for specific items
- Decreased anxiety about file locations
- Improved consistency in file organization
- Better decision-making at category level

**System Health Indicators:**
- JDex maintained and current
- ID assignments consistent with definitions
- Minimal folder reorganization needed
- Easy retrieval of past items

---

## 10. Key Design Constraints

### 10.1 Why 10-Item Limits Matter

**Cognitive Load:**
- 10 items is manageable decision threshold
- Prevents option paralysis
- Makes all choices memorable

**Stability:**
- Prevents folder shifting when new items created
- Maintains predictable locations
- Enables memorization of common paths

**Standardization:**
- Consistent structure across all levels
- Easy to explain and teach
- Facilitates cross-system compatibility

### 10.2 No Deeper Than Three Levels

**Why:**
- Reduces file system complexity
- Maintains searchability through JDex
- Forces deliberate categorization at ID level
- Prevents sprawling hierarchies

---

## 11. Terminology & Notation Summary

| Term | Format | Example | Purpose |
|------|--------|---------|---------|
| Area | `[0-9]0-[0-9]9` | `10-19` | Broad organizational domains |
| Category | `[0-9][0-9]` | `11` | Subdivisions within areas |
| ID | `AC.ID` | `11.23` | Specific items/projects |
| Sub-ID | `AC.ID+SUB` | `11.24+JEM` | Repeating or overflow items |
| System ID | `SYS.AC.ID` | `H01.11.23` | Multiple independent systems |
| JDex | Index | Note app | Master record of all IDs |

---

## 12. Implementation Workflow

### Getting Started

1. **Design your areas** (top-down or bottom-up)
2. **Identify categories** within each area
3. **Set up storage** (folder structure or files)
4. **Create JDex** (notes app or database)
5. **Assign IDs** before creating folders
6. **Document decisions** in system notes
7. **Maintain regularly** through Librarian role

### Adding New Items

1. Identify applicable category
2. Check JDex for available ID
3. Create new note in JDex
4. Create folder/file with proper naming
5. Add metadata (location, keywords, relates-to)
6. Search and retrieve as needed

---

## Conclusion

Johnny Decimal provides a scalable, constraint-based organizational system applicable to personal life, business operations, or any information management context. By deliberately limiting choices at structural levels and maintaining centralized indexes, it reduces cognitive load while enabling rapid, confident retrieval.

The system's power derives from its simplicity: three-level hierarchy, ten-item limits, unique identifiers, and centralized tracking. These constraints, though initially restrictive, create organizational stability that pays dividends repeatedly through reduced friction in daily information management.

