from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions


# 서버 수명 주기 관리를 위한 비동기 컨텍스트 매니저
@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[dict]:
    """서버 시작 및 종료 수명 주기를 관리합니다."""
    # 시작 시 리소스 초기화
    db = {"users": [{"id": 1, "name": "홍길동"}, {"id": 2, "name": "김철수"}]}
    print("서버가 시작되었습니다.")
    try:
        yield {"db": db}
    finally:
        # 종료 시 정리
        print("서버가 종료되었습니다.")


# 서버 인스턴스 생성 (수명 주기 관리 포함)
server = Server("예제-서버", lifespan=server_lifespan)


# 프롬프트 목록 처리기
@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="인사-프롬프트",
            description="인사말 프롬프트 템플릿",
            arguments=[
                types.PromptArgument(
                    name="이름", description="인사할 사람 이름", required=True
                )
            ],
        )
    ]


# 프롬프트 가져오기 처리기
@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    if name != "인사-프롬프트":
        raise ValueError(f"알 수 없는 프롬프트: {name}")
    
    # 인수에서 이름 가져오기 또는 기본값 사용
    user_name = arguments.get("이름", "사용자") if arguments else "사용자"
    
    return types.GetPromptResult(
        description="인사말 예제",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=f"{user_name}님, 안녕하세요!"),
            )
        ],
    )


# 도구 호출 처리기
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> str:
    ctx = server.request_context
    db = ctx.lifespan_context["db"]
    
    if name == "get-users":
        return db["users"]
    elif name == "get-user-by-id":
        user_id = arguments.get("id")
        if user_id is None:
            return "오류: 사용자 ID가 필요합니다."
        
        # DB에서 사용자 찾기
        for user in db["users"]:
            if user["id"] == user_id:
                return user
        
        return f"오류: ID {user_id}의 사용자를 찾을 수 없습니다."
    else:
        return f"알 수 없는 도구: {name}"


# 도구 목록 처리기
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get-users",
            description="모든 사용자 목록을 가져옵니다",
            arguments=[],
        ),
        types.Tool(
            name="get-user-by-id",
            description="ID로 사용자를 가져옵니다",
            arguments=[
                types.ToolArgument(
                    name="id", description="사용자 ID", required=True, schema={"type": "number"}
                )
            ],
        ),
    ]


# 서버 실행 함수
async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="예제-서버",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio
    
    asyncio.run(run())