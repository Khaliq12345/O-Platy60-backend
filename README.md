# O-Platy60-backend

O-Platy60-backend/
│── src/
│   ├── api/                  # API layer (routes/controllers)
│   │   └── user_api.py
│   │
│   ├── services/             # Business logic
│   │   └── user_service.py
│   │
│   ├── repositories/         # (Optional) abstraction over Supabase queries
│   │   └── user_repo.py
│   │
│   ├── schemas/              # Pydantic models for validation
│   │   └── user.py
│   │
│   ├── core/                 
│   │   ├── config.py         # Supabase URL, keys
│   │   └── supabase_client.py # Client initialization
│   │
│   └── main.py               # Entry point (FastAPI app)
│
├── tests/
├── requirements.txt
└── README.md
