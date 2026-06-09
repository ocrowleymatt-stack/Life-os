from fastapi import FastAPI

app = FastAPI(title='Daedalus API')

@app.get('/')
def root():
    return {
        'service': 'Daedalus API',
        'status': 'bootstrap',
        'safe_mode': True
    }
