import sc

from .config import Config


class App:
    def __init__(self, args) -> None:
        self._args = args
        self._config = Config(args.config)

        self._memory = sc.Memory(self._config.get_path_to_sc_config())

    def run(self):
        self._config.init_env()

        import uvicorn
        from .db.init_db import init_db
        from fastapi import FastAPI
        from .api.api import api_router

        init_db()
        app = FastAPI()
        app.include_router(api_router)

        try:
            uvicorn.run(
                app,
                host=self._config.get_host(),
                port=self._config.get_port(),
                log_level="info",
            )
            self._on_stop()
        except KeyboardInterrupt:
            print("Interrupted with keyboard...")
            self._on_stop()

    def _on_stop(self):
        print("Stopping service...")
        self._memory.close()
