# Arquitetura — CultiveAI

Diagramas em Mermaid prontos para artigo. Renderizam direto no GitHub.
Para exportar PNG/SVG: cole o bloco em [mermaid.live](https://mermaid.live) → *Actions* → *PNG* ou *SVG*.

> Paleta: cores oficiais do CultiveAI (`#2D6A4F`, `#40916C`, `#95D5B2`, `#E8F5E9`).

---

## 1. Visão de Arquitetura — Containers e Integrações

Como a aplicação é orquestrada em produção via **Docker Compose**, com Nginx como reverse proxy e duas integrações externas (Gemini e Google Earth Engine).

```mermaid
flowchart LR
    User([👤 Usuário<br/>Navegador])

    subgraph Host["🖥️  Servidor — Docker Compose"]
        direction LR

        subgraph FE["📦 frontend"]
            Nginx["Nginx<br/>:80"]
            Vue["Vue 3 + Vite<br/>SPA estática"]
            Nginx --> Vue
        end

        subgraph BE["📦 backend"]
            FastAPI["FastAPI<br/>:8000<br/>Uvicorn"]
        end

        subgraph DB["📦 db"]
            PG[("PostgreSQL 16<br/>:5432")]
        end

        Nginx -.->|proxy /api/v1| FastAPI
        FastAPI -->|SQLAlchemy| PG
    end

    subgraph Ext["☁️  Serviços Externos"]
        Gemini["Google Gemini API<br/>(análise IA)"]
        GEE["Google Earth Engine<br/>(NDVI / satélite)"]
    end

    User -->|HTTPS :80| Nginx
    FastAPI -->|REST| Gemini
    FastAPI -->|Python SDK| GEE

    classDef container fill:#E8F5E9,stroke:#2D6A4F,stroke-width:2px,color:#1B4332;
    classDef external  fill:#E3F2FD,stroke:#1976D2,stroke-width:2px,color:#0D3B66;
    classDef db        fill:#95D5B2,stroke:#1B4332,stroke-width:2px,color:#1B4332;
    classDef user      fill:#FFF3E0,stroke:#F57C00,stroke-width:2px,color:#5C2E00;
    classDef group     fill:#F8FAF9,stroke:#40916C,stroke-width:1px,color:#1B4332;

    class Nginx,Vue,FastAPI container;
    class Gemini,GEE external;
    class PG db;
    class User user;
    class Host,FE,BE,DB,Ext group;
```

---

## 2. Estrutura de Pacotes — Backend (FastAPI)

Arquitetura em camadas. Cada camada só conhece a de baixo, nunca a de cima.

```mermaid
flowchart TD
    Main([main.py<br/>FastAPI app · CORS · routers])

    subgraph API["🌐 API Layer — app/api/"]
        direction LR
        Auth[auth.py]
        Clients[clients.py]
        Properties[properties.py]
        Analysis[analysis.py]
        Deps[deps.py<br/>injeção de dependências]
    end

    subgraph Schemas["📋 Schemas — app/schemas/"]
        direction LR
        SUser[user.py]
        SToken[token.py]
        SClient[client.py]
        SProperty[property.py]
        SAnalysis[analysis.py]
    end

    subgraph Services["⚙️  Services — app/services/"]
        direction LR
        AI[ai_service.py<br/>↔ Gemini]
        GEE_S[gee_service.py<br/>↔ Earth Engine]
        Report[report_service.py<br/>geração PDF]
    end

    subgraph CRUD["🗄️  CRUD — app/crud/"]
        direction LR
        CUser[crud_user.py]
        CClient[crud_client.py]
        CProperty[crud_property.py]
        CAnalysis[crud_analysis.py]
    end

    subgraph Models["🧱 Models — app/models/"]
        direction LR
        MUser[user.py]
        MClient[client.py]
        MProperty[property.py]
        MAnalysis[analysis.py]
    end

    subgraph Core["🔐 Core — app/core/"]
        direction LR
        Config[config.py]
        Security[security.py<br/>JWT · bcrypt]
    end

    subgraph DB["💾 DB — app/db/"]
        direction LR
        Session[session.py<br/>SQLAlchemy engine]
        Base[base.py]
        Alembic[(alembic/<br/>migrations)]
    end

    Main --> API
    API --> Schemas
    API --> CRUD
    API --> Services
    API --> Deps
    Deps --> Core
    CRUD --> Models
    Models --> Base
    Base --> Session
    Services --> Models
    Alembic -.-> Base

    classDef entry  fill:#FFF3E0,stroke:#F57C00,stroke-width:2px,color:#5C2E00;
    classDef api    fill:#D8F3DC,stroke:#2D6A4F,stroke-width:2px,color:#1B4332;
    classDef schema fill:#E8F5E9,stroke:#40916C,stroke-width:1.5px,color:#1B4332;
    classDef svc    fill:#B7E4C7,stroke:#2D6A4F,stroke-width:2px,color:#1B4332;
    classDef crud   fill:#95D5B2,stroke:#1B4332,stroke-width:1.5px,color:#1B4332;
    classDef model  fill:#74C69D,stroke:#1B4332,stroke-width:1.5px,color:#1B4332;
    classDef core   fill:#E3F2FD,stroke:#1976D2,stroke-width:1.5px,color:#0D3B66;
    classDef db     fill:#F1F8E9,stroke:#558B2F,stroke-width:1.5px,color:#1B4332;
    classDef group  fill:#F8FAF9,stroke:#40916C,stroke-width:1px,color:#1B4332;

    class Main entry;
    class Auth,Clients,Properties,Analysis,Deps api;
    class SUser,SToken,SClient,SProperty,SAnalysis schema;
    class AI,GEE_S,Report svc;
    class CUser,CClient,CProperty,CAnalysis crud;
    class MUser,MClient,MProperty,MAnalysis model;
    class Config,Security core;
    class Session,Base,Alembic db;
    class API,Schemas,Services,CRUD,Models,Core,DB group;
```

---

## 3. Estrutura de Pacotes — Frontend (Vue 3)

```mermaid
flowchart TD
    Entry([main.js · App.vue])

    subgraph Router["🧭 Router — src/router/"]
        Idx[index.js<br/>guards de autenticação]
    end

    subgraph Views["📄 Views — src/views/"]
        direction LR
        Login[LoginView]
        Register[RegisterView]
        Home[HomeView]
        Dashboard[DashboardView]
        ClientsV[ClientsView]
        PropertiesV[PropertiesView]
        AnalysisV[AnalysisView]
    end

    subgraph Components["🧩 Components — src/components/"]
        direction LR
        Map[MapComponent<br/>Leaflet]
        AReport[AnalysisReport]
        PDF[ReportPDF<br/>html2pdf]
    end

    subgraph ServicesFE["🔌 Services — src/services/"]
        direction LR
        ApiSvc[ApiService.js<br/>axios · interceptor JWT]
        AuthSvc[auth.js<br/>token storage]
    end

    BE([Backend FastAPI])

    Entry --> Router
    Router --> Views
    Views --> Components
    Views --> ServicesFE
    Components --> ServicesFE
    ApiSvc -.->|HTTP| BE

    classDef entry fill:#FFF3E0,stroke:#F57C00,stroke-width:2px,color:#5C2E00;
    classDef rt    fill:#D8F3DC,stroke:#2D6A4F,stroke-width:2px,color:#1B4332;
    classDef view  fill:#E8F5E9,stroke:#40916C,stroke-width:1.5px,color:#1B4332;
    classDef comp  fill:#B7E4C7,stroke:#2D6A4F,stroke-width:1.5px,color:#1B4332;
    classDef svc   fill:#95D5B2,stroke:#1B4332,stroke-width:1.5px,color:#1B4332;
    classDef ext   fill:#E3F2FD,stroke:#1976D2,stroke-width:2px,color:#0D3B66;
    classDef group fill:#F8FAF9,stroke:#40916C,stroke-width:1px,color:#1B4332;

    class Entry entry;
    class Idx rt;
    class Login,Register,Home,Dashboard,ClientsV,PropertiesV,AnalysisV view;
    class Map,AReport,PDF comp;
    class ApiSvc,AuthSvc svc;
    class BE ext;
    class Router,Views,Components,ServicesFE group;
```

---

## 4. Fluxo de uma Análise NDVI (request lifecycle)

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuário
    participant FE as Vue SPA
    participant NX as Nginx
    participant API as FastAPI
    participant GEE as Earth Engine
    participant AI as Gemini
    participant DB as PostgreSQL

    U->>FE: seleciona propriedade + período
    FE->>NX: POST /api/v1/analysis (JWT)
    NX->>API: proxy
    API->>API: deps.py valida JWT
    API->>GEE: requisita NDVI da geometria
    GEE-->>API: série temporal NDVI
    API->>AI: prompt + dados NDVI
    AI-->>API: laudo interpretado
    API->>DB: persiste análise
    DB-->>API: id
    API-->>FE: relatório JSON
    FE->>U: renderiza mapa + ReportPDF
```
