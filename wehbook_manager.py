import configparser
import logging
import os
import sys
from typing import Any, Dict, List

import requests
import webview

APP_NAME = "Nu4g3 / Wehbook Manager"
SAVE_FOLDER_NAME = "Webhook_Library"
WINDOW_WIDTH = 1150
WINDOW_HEIGHT = 800
DEFAULT_BG_COLOR = "#0a0b0d"
DEFAULT_USERNAME = "Webhook Builder"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class WebhookAPI:
    def __init__(self) -> None:
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.save_dir = os.path.join(self.base_path, SAVE_FOLDER_NAME)
        self._ensure_save_directory()

    def _ensure_save_directory(self) -> None:
        try:
            os.makedirs(self.save_dir, exist_ok=True)
        except OSError as error:
            logger.error("Failed to create save directory: %s", error)

    def send_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        webhook_url = data.get("webhook_url", "").strip()
        if not webhook_url:
            return {"success": False, "error": "L'URL du webhook est manquante."}

        payload: Dict[str, Any] = {
            "content": data.get("content", ""),
            "username": data.get("username", DEFAULT_USERNAME),
            "avatar_url": data.get("avatar_url", ""),
        }

        embeds = data.get("embeds") or []
        components = data.get("components") or []

        if embeds:
            payload["embeds"] = embeds
        if components:
            payload["components"] = components

        try:
            logger.info("Sending message to webhook: %s...", webhook_url[:40])
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            return {"success": True, "message": "Message envoyé avec succès."}
        except requests.exceptions.RequestException as error:
            logger.error("Network error: %s", error)
            return {"success": False, "error": f"Erreur réseau: {error}"}
        except Exception as error:
            logger.error("Unexpected error: %s", error)
            return {"success": False, "error": str(error)}

    def save_webhook(self, data: Dict[str, str]) -> Dict[str, Any]:
        name = data.get("name", "").strip()
        url = data.get("url", "").strip()

        if not name or not url:
            return {"success": False, "error": "Le nom et l'URL sont requis pour l'enregistrement."}

        safe_name = "".join(char if char.isalnum() or char in " .-_()" else "_" for char in name)
        filepath = os.path.join(self.save_dir, f"{safe_name}.cfg")

        try:
            config = configparser.ConfigParser()
            config["webhook"] = {"name": name, "url": url}
            with open(filepath, "w", encoding="utf-8") as file:
                config.write(file)
            logger.info("Saved webhook profile: %s", name)
            return {"success": True, "message": f"Webhook '{name}' ajouté à la bibliothèque."}
        except OSError as error:
            logger.error("Storage error: %s", error)
            return {"success": False, "error": "Impossible d'écrire sur le disque."}

    def get_webhooks(self) -> Dict[str, Any]:
        webhooks: List[Dict[str, str]] = []

        try:
            if os.path.exists(self.save_dir):
                for filename in os.listdir(self.save_dir):
                    if not filename.endswith(".cfg"):
                        continue
                    path = os.path.join(self.save_dir, filename)
                    config = configparser.ConfigParser()
                    config.read(path, encoding="utf-8")
                    if "webhook" not in config:
                        continue
                    webhooks.append(
                        {
                            "name": config.get("webhook", "name"),
                            "url": config.get("webhook", "url"),
                        }
                    )

            webhooks.sort(key=lambda item: item["name"].lower())
            return {"success": True, "webhooks": webhooks}
        except Exception as error:
            logger.error("Load error: %s", error)
            return {"success": False, "error": "Erreur lors du chargement de la bibliothèque."}

    def delete_webhook(self, name: str) -> Dict[str, Any]:
        safe_name = "".join(char if char.isalnum() or char in " .-_()" else "_" for char in name)
        filepath = os.path.join(self.save_dir, f"{safe_name}.cfg")

        try:
            if not os.path.exists(filepath):
                return {"success": False, "error": "Fichier introuvable."}
            os.remove(filepath)
            logger.info("Deleted webhook profile: %s", name)
            return {"success": True, "message": "Supprimé."}
        except OSError as error:
            logger.error("Delete error: %s", error)
            return {"success": False, "error": "Erreur lors de la suppression."}


def run_app() -> None:
    api = WebhookAPI()
    current_dir = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "index.html")
    html_url = f"file:///{html_path.replace('\\', '/')}"

    webview.create_window(
        title=APP_NAME,
        url=html_url,
        js_api=api,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        background_color=DEFAULT_BG_COLOR,
        min_size=(1000, 700),
    )
    webview.start(debug=False)


if __name__ == "__main__":
    run_app()
