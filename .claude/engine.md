# Engine

Edit this file once at project start. Builder and reviewer read it when touching engine-specific code.

## Current engine

`unset` — run `/start` to set this.

---

## Supported engines

When you run `/start`, one of these blocks is activated and the rest are removed from this file. Kept here as reference.

### Godot 4

- **Language:** GDScript 4.x (primary), C# (optional), GDExtension (C++) for perf-critical code
- **Scene structure:** scenes under `scenes/`, scripts under `src/`
- **Key patterns:** signals over polling, Node inheritance, resource files (`.tres`/`.res`) for data-driven values
- **Shaders:** Godot shading language, files in `src/shaders/`
- **Builder conventions:** prefer `@export` over `get_node` string paths, use `class_name` for reusable components
- **Review flags:** direct `get_tree().root.get_node("path/to/node")` calls are a smell — use signals or exported references
- **Test runner:** GUT or gdUnit4

### Unity (2022 LTS+)

- **Language:** C# (primary), HLSL for shaders, ECS/DOTS for perf-critical systems
- **Project structure:** `Assets/Scripts/`, `Assets/Art/`, `Assets/Prefabs/`, `Assets/ScriptableObjects/`
- **Key patterns:** ScriptableObjects for data, Addressables for asset streaming, UI Toolkit for UI (not UGUI for new projects)
- **Shaders:** Shader Graph or HLSL in `Assets/Shaders/`
- **Builder conventions:** `[SerializeField] private` over `public`, avoid `GameObject.Find`, use events over Update polling
- **Review flags:** allocations inside `Update()`, `GetComponent<>()` in hot paths, public fields on MonoBehaviours
- **Test runner:** Unity Test Framework (Edit Mode + Play Mode)

### Unreal Engine 5

- **Language:** C++ (primary), Blueprints for designer-facing logic, HLSL for materials
- **Project structure:** `Source/<ProjectName>/`, `Content/` for assets
- **Key patterns:** Gameplay Ability System (GAS) for abilities, UMG/CommonUI for UI, Chaos for physics
- **Networking:** replication via `UPROPERTY(Replicated)`, RPCs via `UFUNCTION(Server/Client/NetMulticast)`
- **Builder conventions:** UPROPERTY macros on all reflected fields, prefer delegates over tick polling
- **Review flags:** untagged `UPROPERTY`, client-trusted logic in multiplayer, logic in `BeginPlay` that should be in `InitializeComponent`
- **Test runner:** Automation Framework + Gauntlet

### Custom

- Fill in your engine's conventions here. At minimum:
  - **Language(s):**
  - **Key directories:**
  - **Data-driven value pattern:**
  - **Shader/VFX location:**
  - **Common review flags:**
  - **Test runner:**
