# gql_personalities/1: co musíme udělat

Téma: **PersonalData** + **Education** (služba doplňuje identitu uživatele o osobní a studijní údaje).
Skupina: ŠR 2026/27 ZS 23-5KB, zadání od Štefka (přeposlal Koláček).

---

## 1. Deadliny

| Datum | Co odevzdat / udělat | Hotovo |
|---|---|------|
| **9. 10. 2026** | Vybrané téma, fork nebo příprava, **repository na GitHubu** | [✓]  |
| **23. 10. 2026** | **1. PD: databázová vrstva** (DB modely, SQLAlchemy 2.x) | [✓]  |
| **23. 11. 2026** | **2. PD: vrstva služeb** (Services + Loadery) | [ ]  |
| **15. 1. 2027** | **Agentní den**, společná prezentace za celou skupinu | [ ]  |
| **25. 1. / 26. 1. 2027** | **3. PD: vrstva GQL** (typy, resolvery, mutace) | [ ]  |

Pozn.: k účasti na každém projektovém dni patří **commit na GitHubu ne starší než 1 týden** (5 b za den, celkem 15 b). Omluvenou neúčast lze individuálně nahradit.

---

## 2. Datový model

### PersonalData (max. 1 záznam na uživatele)
- `user_id` – identifikátor uživatele (unikátní, federace na UserGQLModel)
- `birth_number` – rodné číslo (**citlivý údaj**)
- `birth_date` – datum narození
- `birth_place` – místo narození
- `citizenship` – státní občanství
- `nationality` – národnost (nepovinné)
- `personal_title` – titul / další osobní údaj
- `note` – poznámka

### Education (více záznamů na osobu)
- `user_id` – osoba, které se záznam týká
- `institution_name` – škola / instituce
- `study_program` – program nebo obor
- `degree` – titul / kvalifikace
- `started` – začátek (datum nebo rok)
- `finished` – konec (datum nebo rok)
- `graduated` – úspěšně dokončeno (ano/ne)
- `description` – doplňující informace

### Certificates (více záznamů na osobu)
- `user_id` - osoba které se záznam týká
- `type` - typ certifikátu -> odkaz na certificate types (gql_personalities -> delal to babis2 takze tak (najdi si https://github.com/matejtresnak/gql_personalities))
- `received` - dosažení (datum nebo rok)
- `expiration` - konec certifikátu (datum nebo rok)
- `description` - doplňujúce informácie
- `Tabulka_1` user_certificates (`user_id`, `certificate_id`, `issue_date`, `expiration_date`) - spojovací tabulka pro více certifikátů na osobu
- `Tabulka_2` certificate_types (`certificate_id`, `name`, `description`) - číselník typů certifikátů

Vztahy: `User → Personality → Education`

### K ujasnění se zadavatelem
- [ ] Je `user_id` totéž co `user_id`, nebo je Personality samostatná entita? (v PersonalData je `user_id`, v Education `user_id`)
- [ ] Datový typ `started` / `finished`: datum, nebo i samotný rok? (zadání říká „datum nebo rok“)
- [ ] Zda má Education navázat na číselník (typy typů), např. typ studia nebo stupeň titulu

---

## 3. Co je potřeba implementovat

### Architektura (porušení = **−15 b**)
`GQL typ / resolver → Service → Loader → DB model`
- držet strukturu ze vzorového **gql_evolution, větev 2026**
- moduly v `src/…`: Modely / Loadery / Services / GQLModely

### Technologie
- Python 3.11+
- strawberry-graphql + strawberry.federation
- ASGI server (uvicorn)
- SQLAlchemy 2.x
- DataLoadery (řeší N+1)
- Docker / Docker Compose (doporučené), `.env` pro konfiguraci

### Funkčnost
- [ ] Query a Mutations **pro všechny typy** (PersonalData, Education, číselníky)
- [ ] Číselníky (typy) implementovat jako **stromy** („typy typů“)
- [ ] **Atomické mutace**: při chybě kompletní rollback, jinak commit; použít typové dataloadery
- [ ] Chybové kódy (**UUID**) u všech chyb z resolverů + **slovník chybových kódů** s popisem
- [ ] Návratové typy CUD resolverů obsahují chybové typy; u CU **unie** chybových typů a typu, se kterým operace pracuje
- [ ] **Popisy (description)** u GQL typů, inputů a argumentů tak, aby AI dokázala vybrat správný typ z pokynu
- [ ] **Filtry na vektorové atributy** u GQL typů a u fieldů v Query
- [ ] **Popisné direktivy u cizích klíčů** v GQL typech
- [ ] **WhoAmIExtension** aktivní (ověření autentizace)
- [ ] **Autorizace** atributů a CUD operací: kdo a za jakých okolností smí co (15 b); u `birth_number` obzvlášť
- [ ] Federace: údaje o uživateli přes `UserGQLModel`, **bez kopií**
- [ ] Ověřit integraci do federace přes docker compose

### Soubory a data
- [ ] `public/`: `graphiql.html`, `voyager.html`, `tests.html` (gql_office), `liveschema.html`, `livedata.html`
- [ ] **Demodata** pro naše struktury
- [ ] Příspěvek do společného **`systemdata.json`**
- [ ] `tests/` s unit a integračními testy + coverage report
- [ ] `README.md` jako deníček

---

## 4. Společný úkol (celá skupina)
- Sdílený **agent (PydanticAI)**, upravit podle potřeb, lze použít GitHub MCP server
- Použít ho při řešení úkolů
- Agent z celé skupiny vybere 3 studenty, kteří dostanou bonus **30 / 20 / 10 b**
- Výstup: společná prezentace na **Agentním dni 15. 1. 2027**

---

## 4d. Demodata + oprava FK (2026-10-16)

Přidána testovací data do `systemdata.json` pro všechny nové tabulky (načítají se při `DEMODATA=True`).

| Tabulka | Záznamy |
|---|---|
| `education_types` | 6 uzlů stromu (VŠ: Bc/Ing/PhD, SŠ: Maturitní) |
| `certificate_types` | 4 typy (CCNA, AWS CP, ECDL, Řidičský průkaz B) |
| `personal_data` | 3 osoby (Jan Novák, Marie Svobodová, Petr Kratochvíl) |
| `education` | 4 záznamy (Jan 2×, Marie 1×, Petr 1×) |
| `user_certificates` | 4 záznamy (Jan 2 cert, Marie 1, Petr 1) |

---

## 4c. EducationTypeModel – číselník (strom) pro typy vzdělání (2026-10-14)

Přidán `EducationTypeModel` jako strom číselníkových hodnot pro klasifikaci záznamů o vzdělání.

**Proč strom?**
Zadání vyžaduje číselníky implementovat jako „typy typů" (stromy). Uzly mají `parent_id` – FK na sebe sama – takže lze modelovat hierarchii, např.:

```
VŠ vzdělání  (parent_id = NULL)
 ├── Bakalářské  (parent_id → VŠ vzdělání)
 ├── Magisterské (parent_id → VŠ vzdělání)
 └── Doktorské   (parent_id → VŠ vzdělání)

SŠ vzdělání  (parent_id = NULL)
 ├── Maturitní    (parent_id → SŠ vzdělání)
 └── Učební obor  (parent_id → SŠ vzdělání)
```

Kořenové uzly mají `parent_id = NULL`. `EducationModel.type_id` je FK na tento číselník – konkrétní záznam o vzdělání jednoduše ukáže na uzel v tomto stromě.

**Soubory:**
- `src/DBDefinitions/Domain_Personalities/Education` – nový model, tabulka `educationtypes`
- `src/DBDefinitions/Domain_Personalities/Education` – přidán `type_id` FK + `type` relationship

---

## 4b. Opravené bugy (2026-10-14)

| Soubor | Bug | Oprava |
|---|---|---|
| `src/ServiceDefinitions/main.py` | `loader.insert()` volá jen `flush()`, ne `commit()` → data se po CLI create odrolují, tabulka vypadá prázdná | Přidán `await session.commit()` po každé operaci |
| `src/GraphTypeDefinitions/Domain_Personalities/Certificates` | Chyběly wrapper třídy `Query_Domain_Certificates` a `Mutation_Domain_Certificates` | Doplněny podle vzoru Education/PersonalData |
| `src/GraphTypeDefinitions/query.py` | `Query_Domain_Certificates` použit bez importu → `NameError` | Přidán import z `Certificates` |
| `src/GraphTypeDefinitions/mutation.py` | `Mutation_Domain_Certificates` použit bez importu → `NameError` | Přidán import z `Certificates` |

---

## 5. Hodnocení (max. 120 b)

| Položka | Body | Poznámka |
|---|---|---|
| Projektové dny (3×) | 15 | 5 b za den, commit ne starší než 1 týden |
| Příběh / deníček (README.md) | 5 | časová posloupnost commitů, problémy, objevy, řešení |
| Komentáře v kódu + description v GQL | až 5 | |
| Autorizace atributů a CUD | až 15 | |
| `systemdata.json` | 5 | |
| Code coverage ≥ 95 % | 10 | včetně správnosti testů |
| Obhajoba | 60 | každý předvede svou část |
| Porušení architektury | **−15** | |

- Úspěšné absolvování: **více než 50 b**
- Známka **A**: **90 b a více**

---

## 6. Užitečné příkazy

### Docker
```bash
# Spustit celý stack (builduje lokálně z kódu)
docker compose up --build

# Spustit bez rebuildu
docker compose up

# Zastavit (data zůstanou)
docker compose down

# Zastavit A smazat všechna data
docker compose down -v

# Buildovat a pushovat tvůj image na Docker Hub
docker build -t velkayolanda/gql-personalities:latest .
docker push velkayolanda/gql-personalities:latest
```

### CLI – Service vrstva (spouštět z rootu projektu)

**List:**
```
python -m src.ServiceDefinitions.main EducationType list
```
```
python -m src.ServiceDefinitions.main Education list
```
```
python -m src.ServiceDefinitions.main PersonalData list
```
```
python -m src.ServiceDefinitions.main CertificateType list
```
```
python -m src.ServiceDefinitions.main UserCertificate list
```

**Create** (createdby_id, changedby_id, rbacobject_id se doplní automaticky):
```
python -m src.ServiceDefinitions.main EducationType create "{\"name\": \"Název\", \"name_en\": \"Name\"}"
```
```
python -m src.ServiceDefinitions.main Education create "{\"personality_id\": \"uuid-zde\", \"institution_name\": \"FIT CVUT\", \"study_program\": \"Informatika\", \"degree\": \"Bc.\", \"started\": \"2022-09-01\", \"graduated\": false}"
```
```
python -m src.ServiceDefinitions.main PersonalData create "{\"user_id\": \"uuid-zde\", \"note\": \"Poznamka\"}"
```
```
python -m src.ServiceDefinitions.main CertificateType create "{\"name\": \"Název\", \"description\": \"Popis\"}"
```
```
python -m src.ServiceDefinitions.main UserCertificate create "{\"user_id\": \"uuid-zde\", \"certificate_id\": \"uuid-zde\", \"issue_date\": \"2024-01-01\", \"is_valid\": true}"
```

**Get podle ID:**
```
python -m src.ServiceDefinitions.main CertificateType get "{\"id\": \"uuid-zde\"}"
```

### Testy

**Všechny testy:**
```
pytest tests/ -v
```

**Jen CRUD testy service vrstvy (integrační, potřebuje běžící DB):**
```
pytest tests/services/test_servicedefinitions_crud.py -v
```

**S výpisem logů:**
```
pytest tests/services/test_servicedefinitions_crud.py -v -s
```

---

## 7. Navržený postup podle termínů

**Do 9. 10.**
- [X] Potvrdit téma (pávkovi do tabulky)
- [x] Vytvořit fork / repository, přidat všechny členy
- [x] Rozdělit práci (PersonalData vs. Education + číselníky) pridane téma certifikáty
- [x] Projít vzorový gql_evolution (větev 2026)

**Do 23. 10. (DB vrstva)**
- [x] DB modely PersonalData, Education, číselníky (stromy)
- [x] Unikátní omezení na `user_id` v PersonalData
- [x] Připojení databáze, `.env`, docker compose
- [x] Začít README deníček

**Do 23. 11. (služby)**
- [x] pridat rbac, created by, lastchange
- [x] pridat kategorie do certifikatu - strom
- [x] Loadery a Services pro všechny entity
- [x] Transakce a rollback
- [x] Unit testy služeb
- [x] Demodata

**Do 15. 1. (agentní den)**
- [ ] Zapojit sdíleného PydanticAI agenta
- [ ] Příprava společné prezentace

**Do 25. / 26. 1. (GQL vrstva)**
- [ ] GQL typy, inputy, resolvery, chybové unie, kódy chyb
- [ ] Filtry, popisy, direktivy u cizích klíčů
- [ ] WhoAmIExtension + autorizace
- [ ] HTML soubory v `public/`
- [ ] `systemdata.json`
- [ ] Coverage ≥ 95 %
- [ ] Docker image na Docker Hub
- [ ] Dokončit README
- [ ] Připravit obhajobu své části
