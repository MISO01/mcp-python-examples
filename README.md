# MCP Python SDK 예제

Model Context Protocol(MCP) Python SDK를 사용하는 다양한 예제를 담은 저장소입니다.

## 예제 파일 설명

- `mcp_server.py`: 간단한 에코 MCP 서버 예제
- `sqlite_mcp_server.py`: SQLite 데이터베이스와 통합한 MCP 서버 예제
- `asgi_server.py`: 기존 ASGI 서버에 MCP 서버를 마운트하는 예제
- `lowlevel_server.py`: 저수준 MCP API를 사용한 서버 구현 예제
- `mcp_client.py`: MCP 클라이언트 구현 예제
- `MCP_사용법_요약.md`: MCP Python SDK 사용 방법에 대한 요약 문서

## 사용 방법

각 파일을 독립적으로 실행할 수 있습니다. 예를 들어:

```bash
python mcp_server.py
```

## 참고

이 예제들은 [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)를 기반으로 작성되었습니다.