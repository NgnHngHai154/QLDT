.PHONY: help status frontend-install frontend-dev frontend-build

help:
	@echo "QLDT frontend planning harness"
	@echo "  make status          Show the current project status"
	@echo "  make frontend-install Install frontend dependencies"
	@echo "  make frontend-dev     Start the Vite development server"
	@echo "  make frontend-build   Typecheck and build the frontend"
	@echo "  make help    Show available targets"

status:
	@echo "Frontend modules are under frontend/; API integration depends on contracts/openapi.yaml."

frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build