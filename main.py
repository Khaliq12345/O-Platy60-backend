from src.api.app import app
import uvicorn

# Exposer l'application pour uvicorn
# uvicorn main:app --reload

def main():
    print("Hello from o-platy60-backend!")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
