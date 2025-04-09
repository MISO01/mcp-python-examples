# MCP Python SDK 사용 방법

## MCP(Model Context Protocol)란?

MCP는 AI 모델과 애플리케이션이 상호작용하기 위한 표준 프로토콜입니다. 이 프로토콜을 통해 AI 모델은 애플리케이션의 리소스에 접근하고 도구를 호출할 수 있습니다.

## 핵심 개념

MCP는 세 가지 핵심 개념을 정의합니다:

1. **프롬프트(Prompts)**: 사용자 제어 방식으로 상호작용하는 템플릿
2. **리소스(Resources)**: 애플리케이션에서 관리하는 컨텍스트 데이터
3. **도구(Tools)**: AI 모델이 작업을 수행하기 위해 호출할 수 있는 함수

## 서버 구현 방법

### 1. FastMCP를 사용한 간단한 서버

```python
from mcp.server.fastmcp import FastMCP

# MCP 서버 인스턴스 생성
mcp = FastMCP("에코 서버")

# 리소스 정의
@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    return f"리소스 에코: {message}"

# 도구 정의
@mcp.tool()
def echo_tool(message: str) -> str:
    return f"도구 에코: {message}"

# 프롬프트 정의
@mcp.prompt()
def echo_prompt(message: str) -> str:
    return f"이 메시지를 처리해주세요: {message}"

if __name__ == "__main__":
    # 서버 실행
    mcp.run()
```

### 2. 기존 ASGI 서버에 마운트

```python
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("통합 MCP 서버")

# ASGI 앱 생성 및 MCP 서버 마운트
app = Starlette(
    routes=[
        Mount('/mcp', app=mcp.sse_app()),  # MCP 서버를 /mcp 경로에 마운트
    ]
)
```

### 3. 저수준 서버 구현

```python
from mcp.server.lowlevel import Server
from mcp.server.models import InitializationOptions

# 서버 인스턴스 생성
server = Server("예제-서버")

# 도구 목록 처리기
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="example-tool",
            description="예제 도구",
            arguments=[
                types.ToolArgument(
                    name="arg1", 
                    description="예제 인수", 
                    required=True
                )
            ],
        )
    ]
```

## 서버 기능

MCP 서버는 다양한 기능을 제공할 수 있습니다:

1. **리소스 노출**: 파일, API 응답 등의 컨텍스트 데이터 제공
2. **도구 제공**: 모델이 호출할 수 있는 함수 제공
3. **프롬프트 관리**: 사용자 상호작용을 위한 템플릿 제공
4. **로깅 및 모니터링**: 서버 활동 추적
5. **인수 완성**: 도구 호출 시 인수 제안

## 클라이언트 구현 방법

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 서버 매개변수 설정
server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"],
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 연결 초기화
            await session.initialize()
            
            # 도구 호출
            result = await session.call_tool("tool-name", arguments={"arg1": "value"})
```

## MCP의 장점

1. **표준화된 인터페이스**: 일관된 방식으로 AI 모델과 통합
2. **보안**: 명확하게 정의된 기능만 노출
3. **유연성**: 다양한 유형의 애플리케이션과 통합 가능
4. **확장성**: 새로운 기능을 쉽게 추가할 수 있는 구조