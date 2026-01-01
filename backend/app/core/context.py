import json
import os
from typing import Dict, Any, Optional

CONTEXT_DIR = os.path.join(os.path.dirname(__file__), "../economic_contexts")

class ContextManager:
    _instance = None
    _active_context: Dict[str, Any] = {}
    _loaded_contexts: Dict[str, Dict[str, Any]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContextManager, cls).__new__(cls)
            cls._instance._load_all_contexts()
            cls._instance.set_context("global") # Default
        return cls._instance

    def _load_all_contexts(self):
        for filename in os.listdir(CONTEXT_DIR):
            if filename.endswith(".json"):
                path = os.path.join(CONTEXT_DIR, filename)
                with open(path, "r") as f:
                    data = json.load(f)
                    self._loaded_contexts[data["context_id"]] = data

    def set_context(self, context_id: str):
        if context_id in self._loaded_contexts:
            self._active_context = self._loaded_contexts[context_id]
        else:
            raise ValueError(f"Context '{context_id}' not found.")

    def get_active_context(self) -> Dict[str, Any]:
        return self._active_context

    def get_available_contexts(self) -> Dict[str, str]:
        """Returns map of ID -> Name"""
        return {k: v["name"] for k, v in self._loaded_contexts.items()}

context_manager = ContextManager()
