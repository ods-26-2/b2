from datetime import datetime, timezone

class TimeService:
    def __init__(self, service_name="global-time-service"):
        self.service_name = service_name

    def get_current_utc_timestamp(self) -> str:
        """Retorna o timestamp no padrão ISO 8601 UTC."""
        return datetime.now(timezone.utc).isoformat()

    def get_current_epoch_ms(self) -> int:
        """Retorna o tempo em milissegundos (Epoch)."""
        return int(datetime.now(timezone.utc).timestamp() * 1000)

    def create_reply_payload(self, correlation_id: str) -> dict:
        """Monta o payload de resposta seguindo o padrão exigido pelo projeto."""
        now_utc = self.get_current_utc_timestamp()
        
        return {
            "schema": "ods.system.time",
            "schema_version": "1.0",
            "message_type": "reply",
            "producer": self.service_name,
            "published_at": now_utc,
            "payload": {
                "correlation_id": correlation_id,
                "status": "success",
                "capture_time": {
                    "utc_timestamp": now_utc,
                    "epoch_ms": self.get_current_epoch_ms()
                }
            }
        }