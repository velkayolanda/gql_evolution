# Event boilerplate project

Demonstrační boilerplate pro doménu `Event / EventInvitation` podle funkčního vzoru ze `src.zip`.

## Zásady

- GQL vrstva nesmí importovat DB vrstvu ani typově odkazovat na DB modely.
- Pro decoupling mezi vrstvami se používají `Protocol` kontrakty v `src/common/protocols.py`.
- `LoaderMap`, services a GQL typy jsou explicitně definované.
- `EventInvitation` je vazba `Event - User` se stavem pozvánky/účasti.
- `UserGQLModel` je externí federovaná entita pro Apollo Federation.
- `StateGQLModel` je také externí federovaná entita, protože stav pozvánky typicky patří do UG / state-machine subgrafu.
- Page resolvery vždy používají `whereType` definovaný přes `@createInputs2`.
- Mutace používají `BaseService.ExecuteServiceMethod` a `CreateErrorCallback`, aby resolver neobsahoval lokální zpracování výjimek.
- `BaseGQLModel.from_dataclass()` zůstává kompatibilní název, ale interně volá `from_db()` a ukládá původní entitu do `_dbdata` bez `dataclasses.asdict()`.


## Závislost na `uoishelpers`

Projekt pracuje s balíkem `uoishelpers` z repozitáře:

```text
https://github.com/hrbolek/uoishelpers/archive/4e41615436d6effbe248d8503e4df373549bcec3.zip
```

Závislost je uvedená přímo v `pyproject.toml`:

```toml
'uoishelpers @ https://github.com/hrbolek/uoishelpers/archive/4e41615436d6effbe248d8503e4df373549bcec3.zip'
```

Boilerplate proto nepřidává lokální náhražky pro `uoishelpers`. Používá importy ve stejném stylu jako funkční vzor, například:

```python
from uoishelpers.dataloaders.LoaderMapBase import LoaderMapBase
from uoishelpers.dataloaders.IDLoader import IDLoader
from uoishelpers.gqlpermissions import OnlyForAuthentized
from uoishelpers.resolvers import PageResolver, createInputs2
```

Závislost je připnutá na konkrétní commit, aby instalace i CI používaly stejnou verzi.

## Vrstvy

```text
DBDefinitions/
  Domain_Events/
    EventModel.py
    EventInvitationModel.py

Dataloaders/
  __init__.py        # explicitní LoaderMap

ServiceDefinitions/
  Domain_Events/
    EventService.py
    EventInvitationService.py

GraphTypeDefinitions/
  BaseGQLModel.py    # _dbdata + LoaderName kontrakt
  Domain_Events/
    EventGQLModel.py
    EventInvitationGQLModel.py
  Domain_UG/
    UserGQLModel.py  # externí federovaná entita
    StateGQLModel.py # externí federovaná entita
```

## Studenti typicky doplní

1. DB model do `DBDefinitions/Domain_X`.
2. Explicitní položku v `LoaderMap`.
3. Service třídu do `ServiceDefinitions/Domain_X`.
4. GQL typ bez importu DB vrstvy.
5. `InputFilter` přes `@createInputs2`.
6. Query přes `PageResolver(... whereType=...)`.
7. Mutace přes `ExecuteServiceMethod`.

## Spuštění Coder

```bash
python .CoderDefinitions/main.py
```

---

## Deníček – PersonalData část

### 2026-10-09 – DB vrstva PersonalData

Vytvořena databázová vrstva pro doménu `PersonalData` podle vzoru `Domain_Events`.

**Co bylo přidáno:**
- `src/DBDefinitions/Domain_Personalities/PersonalData` – SQLAlchemy 2.x model, tabulka `personaldata`, `UniqueConstraint` na `user_id` (max 1 záznam na uživatele), `user_id` jako soft federation FK (User žije v jiné službě)
- `src/Dataloaders/__init__.py` – doplněn `PersonalDataModel` loader do `LoaderMap`
- `src/ServiceDefinitions/Domain_PersonalData/PersonalDataService.py` – CRUD service přes `BaseService`
- `src/GraphTypeDefinitions/Domain_Personalities/PersonalData` – GQL typ s query (`personal_data_by_id`, `personal_data_page`) a mutacemi (insert / update / delete), chybové kódy jako UUID
- `src/GraphTypeDefinitions/query.py` a `mutation.py` – PersonalData doména zapojena do root Query / Mutation

**Problémy / poznámky:**
- `birth_number` je citlivý údaj – zatím chráněn pouze `OnlyForAuthentized`, autorizace přes role se doplní ve 2. nebo 3. PD
- Education a Certificate modely jsou záměrně vynechány – to je část jiného člena týmu

---

## Deníček – Education část

### 2026-10-12 – DB + Service + GQL vrstva Education

Vytvořena kompletní vrstva pro doménu `Education` podle stejného vzoru jako `PersonalData`.

**Co bylo přidáno:**
- `src/DBDefinitions/Domain_Personalities/Education` – SQLAlchemy 2.x model, tabulka `education`, bez `UniqueConstraint` (více záznamů na osobu); `user_id` jako soft FK na PersonalData
- `src/DBDefinitions/__init__.py` – doplněn import a export `EducationModel`
- `src/Dataloaders/__init__.py` – doplněn `EducationModel` loader do `LoaderMap`
- `src/ServiceDefinitions/Domain_Education/EducationService.py` – CRUD service přes `BaseService`
- `src/ServiceDefinitions/ServiceContext.py` – doplněna property `EducationService` do `ServiceRegistry`
- `src/GraphTypeDefinitions/Domain_Personalities/Education` – GQL typ s query (`education_by_id`, `education_page`) a mutacemi (insert / update / delete), chybové kódy jako UUID
- `src/GraphTypeDefinitions/query.py` a `mutation.py` – Education doména zapojena do root Query / Mutation

**Problémy / poznámky:**
- `started` a `finished` jsou uloženy jako `datetime.date`; pokud zadání vyžaduje jen rok, lze použít datum 1. 1. daného roku
- `user_id` je soft FK – nevynucuje referenční integritu na DB úrovni, stejně jako `user_id` v PersonalData

---

## Deníček – Certificates část

### 2026-10-14 – DB + Service + GQL vrstva Certificates (commit e7d9e0b)

Vytvořena kompletní vrstva pro doménu `Certificates` podle stejného vzoru jako `PersonalData` a `Education`.

**Co bylo přidáno:**
- `src/DBDefinitions/Domain_Personalities/Certificates` – SQLAlchemy 2.x model, tabulka `certificates`; obsahuje `user_id` s FK na `personaldata.id` (nullable=False), dále `title`, `issuer`, `certificate_number`, `issued`, `valid_to`, `level`, `description` a `certificate_type_id` (soft link na číselník v cizí službě gql_personalities)
- `src/DBDefinitions/__init__.py` – doplněn import a export `CertificateModel`
- `src/Dataloaders/__init__.py` – doplněn `CertificateModel` loader do `LoaderMap`
- `src/ServiceDefinitions/Domain_Certificates/CertificateTypeService.py` – CRUD service přes `BaseService`
- `src/ServiceDefinitions/ServiceContext.py` – doplněna property `CertificateService` do `ServiceRegistry`
- `src/GraphTypeDefinitions/Domain_Personalities/Certificates` – GQL typ s query (`certificate_by_id`, `certificate_page`), filtrem (`CertificateInputFilter`) a mutacemi insert / update / delete; chybové kódy jako UUID
- `src/GraphTypeDefinitions/query.py` a `mutation.py` – Certificates doména zapojena do root Query / Mutation

**Problémy / poznámky:**
- `certificate_type_id` je uloženo jako `String`, ne UUID – záměrně, protože číselník typů certifikátů žije v externí službě (`gql_personalities`), takže FK constraint na DB úrovni nedává smysl
- `user_id` je `nullable=False` na DB úrovni; GQL input ho má jako `Optional` – při vytvoření bez `user_id` dojde k NOT NULL chybě z PostgreSQL

---

### 2026-10-14 – EducationTypeModel (číselník stromového typu)

Přidán číselník pro typy vzdělání jako strom (self-referenční `parent_id`), podle vzoru `EventTypeModel`.

**Co je číselník a proč strom?**
Zadání vyžaduje číselníky implementovat jako „typy typů". Každý uzel v tabulce `educationtypes` může mít `parent_id` ukazující na jiný uzel ve stejné tabulce – tím vzniká hierarchie. Kořenové kategorie (např. „VŠ vzdělání") mají `parent_id = NULL`, jejich podtypy (Bakalářské, Magisterské, Doktorské) ukazují na ně přes `parent_id`. `EducationModel.type_id` pak FK odkazuje na konkrétní uzel v tomto stromě.

```
VŠ vzdělání  (parent_id = NULL)
 ├── Bakalářské  (parent_id → VŠ vzdělání)
 ├── Magisterské (parent_id → VŠ vzdělání)
 └── Doktorské   (parent_id → VŠ vzdělání)

SŠ vzdělání  (parent_id = NULL)
 ├── Maturitní    (parent_id → SŠ vzdělání)
 └── Učební obor  (parent_id → SŠ vzdělání)
```

**Co bylo přidáno:**
- `src/DBDefinitions/Domain_Personalities/Education` – SQLAlchemy 2.x model, tabulka `educationtypes`, `parent_id` self-FK, vztahy `parent` / `children` / `educations`
- `src/DBDefinitions/Domain_Personalities/Education` – přidán `type_id` FK na `educationtypes.id` a `type` relationship
- `src/DBDefinitions/Domain_Personalities/Education` a `src/DBDefinitions/__init__.py` – doplněn export `EducationTypeModel`

---

### 2026-10-14 – Opravy bugů (session commit + zapojení do schématu)

Po otestování CLI (`python -m src.ServiceDefinitions.main PersonalData create ...`) se ukázaly dva problémy.

**Bug 1 – data po create zmizela (platí pro všechny domény v Service CLI)**

`IDLoader.insert()` z knihovny `uoishelpers` volá interně jen `session.flush()`, nikoliv `session.commit()`. V GQL vrstvě commit zajišťuje `SessionCommitExtension`, ale v testovacím CLI (`src/ServiceDefinitions/main.py`) taková extension neexistuje. Výsledek: session se zavřela bez commitu, transakce se odrolovala, vložená data zmizela. Oprava: přidán `await session.commit()` za každou operaci v `run_async`.

**Bug 2 – Certificate mutace a query nefungovaly vůbec**

V `src/GraphTypeDefinitions/Domain_Personalities/Certificates` chyběly wrapper třídy `Query_Domain_Certificates` a `Mutation_Domain_Certificates` (vzor: Education, PersonalData mají tyto wrappery). Zároveň `query.py` i `mutation.py` odkazovaly na tyto třídy bez importu → `NameError` při kompilaci celého GQL schématu. Oprava: doplněny wrapper třídy v `__init__.py` a importy v `query.py` / `mutation.py`.

**Soubory změněné při opravě:**
- `src/ServiceDefinitions/main.py` – `await session.commit()` po operacích
- `src/GraphTypeDefinitions/Domain_Personalities/Certificates` – přidány `Query_Domain_Certificates`, `Mutation_Domain_Certificates`
- `src/GraphTypeDefinitions/query.py` – přidán import `Query_Domain_Certificates`
- `src/GraphTypeDefinitions/mutation.py` – přidán import `Mutation_Domain_Certificates`