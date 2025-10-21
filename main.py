from src.api import app
import uvicorn


def main():
    print("Hello from o-platy60-backend!")
    uvicorn.run("src.api.app:app", reload=True)


if __name__ == "__main__":
    main()
