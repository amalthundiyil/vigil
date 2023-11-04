# Notes

- Local python package not found: 
    - Problem: Using pyproject.toml in vigil-backend errored out ("couldn't find matching version 'vigil-backend'")
    - Solution: Remove circular dependency of vigil-backend with vigil-cli
- Mixed Content:
    - Problem: Frontend request from https to backend https but uvicorn redirects and serves using http
    - Solution: https://github.com/tiangolo/fastapi/issues/4284#issuecomment-1190775108
- CORS
    - Problem: CORS error inspite of setting middleware
    - Solution: https://stackoverflow.com/a/65788650/17297103
- Tkinter not found:
    - Problem: Okteto Docker images reported "Import Error: Module _tkinter not found"
    - Solution: Upgraded Docker images to python:3.9 from python:3.8
- Okteto Node error:
    - Problem: Okteto Node docker image failing
    - Solution: Updated docker image from node:18-slim to node:18.18.1-slim
