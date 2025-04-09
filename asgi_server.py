from starlette.applications import Starlette
from starlette.routing import Mount, Host
from starlette.responses import PlainTextResponse
from mcp.server.fastmcp import FastMCP


# MCP 서버 인스턴스 생성
mcp = FastMCP("통합 MCP 서버")


# 간단한 도구 정의
@mcp.tool()
def hello_world(name: str = "세계") -> str:
    """인사말을 반환하는 도구"""
    return f"안녕하세요, {name}님!"


# 메인 웹 앱 라우트
async def homepage(request):
    return PlainTextResponse("메인 웹 애플리케이션 홈페이지")


# ASGI 앱 생성 및 MCP 서버 마운트
app = Starlette(
    routes=[
        Mount('/', app=homepage),
        Mount('/mcp', app=mcp.sse_app()),  # MCP 서버를 /mcp 경로에 마운트
    ]
)

# 또는 동적으로 호스트로 마운트
# app.router.routes.append(Host('mcp.example.com', app=mcp.sse_app()))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)