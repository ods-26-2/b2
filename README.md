# 🕒 Global Time Service (`global-time-service`)

> Responsável por fornecer o tempo de captura global sincronizado para todos os componentes do sistema.

## 📖 Visão Geral

Em um sistema distribuído, relógios locais de diferentes máquinas ou containers sofrem desvios (*clock drift*). O **Global Time Service** atua como a **fonte única da verdade temporal** para o projeto. 

Sempre que o seu componente precisar registrar o timestamp exato de um evento ou captura (frames de vídeo, logs, detecções, etc.), ele deve consultar este serviço via barramento Pub/Sub.

---

## 🏗 Arquitetura & Protocolo

- **Modelo de Comunicação:** Comando/Consulta Textual (`query` / `reply`).
- **Formato das Mensagens:** JSON.
- **Protocolo de Transporte:** MQTT (Porta padrão `1883`).
- **Tópico de Solicitações (Entrada):** `ods/system/time/requests`
- **Tópico de Respostas (Saída):** `ods/system/time/responses`

---

## 📜 Especificação das Mensagens (Contrato JSON)

### 1. Solicitação de Tempo (`query`)
Para solicitar o tempo de captura global, publique no tópico **`ods/system/time/requests`**:

```json
{
  "schema": "ods.system.time",
  "schema_version": "1.0",
  "message_type": "query",
  "producer": "<NOME_DO_SEU_COMPONENTE>",
  "published_at": "<TIMESTAMP_UTC_DO_ENVIO>",
  "payload": {
    "action": "get_global_time",
    "correlation_id": "<IDENTIFICADOR_UNICO_DA_REQUISICAO>"
  }
}
```

### 2. Resposta do Serviço (reply)

```json
{
  "schema": "ods.system.time",
  "schema_version": "1.0",
  "message_type": "reply",
  "producer": "global-time-service",
  "published_at": "2026-10-08T05:11:23.601440+00:00",
  "payload": {
    "correlation_id": "<IDENTIFICADOR_UNICO_DA_REQUISICAO>",
    "status": "success",
    "capture_time": {
      "utc_timestamp": "2026-10-08T05:11:23.601440+00:00",
      "epoch_ms": 1791436283601
    }
  }
}
```

## Como Executar o Docker

1. **Construir a Imagem**\
docker build -t global-time-service:latest .

2. **Subir o Container**\
docker run -d \
  --name global-time-service \
  -e BROKER_ADDRESS="broker.hivemq.com" \
  -e BROKER_PORT=1883 \
  global-time-service:latest

3. **Verificar Logs**\
docker logs -f global-time-service