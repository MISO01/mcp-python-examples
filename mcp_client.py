from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


# stdio 연결을 위한 서버 매개변수 생성
server_params = StdioServerParameters(
    command="python",  # 실행 파일
    args=["mcp_server.py"],  # 명령줄 인수
    env=None,  # 환경 변수
)


# 샘플링 콜백 함수 (선택 사항)
async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="모델에서 보내는 안녕하세요!",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


async def run():
    # stdio 클라이언트 연결
    async with stdio_client(server_params) as (read, write):
        # 클라이언트 세션 초기화
        async with ClientSession(
            read, write, sampling_callback=handle_sampling_message
        ) as session:
            # 연결 초기화
            await session.initialize()
            
            print("MCP 서버에 연결되었습니다.")
            
            # 사용 가능한 프롬프트 나열
            prompts = await session.list_prompts()
            print(f"사용 가능한 프롬프트: {prompts}")
            
            # 프롬프트 가져오기 (있는 경우)
            if prompts:
                prompt_name = prompts[0].name
                prompt = await session.get_prompt(prompt_name, arguments={"message": "안녕하세요"})
                print(f"프롬프트 결과: {prompt}")
            
            # 사용 가능한 리소스 나열
            resources = await session.list_resources()
            print(f"사용 가능한 리소스: {resources}")
            
            # 사용 가능한 도구 나열
            tools = await session.list_tools()
            print(f"사용 가능한 도구: {tools}")
            
            # 도구 호출 (있는 경우)
            if tools:
                tool_name = tools[0].name
                first_arg_name = tools[0].arguments[0].name if tools[0].arguments else None
                
                if first_arg_name:
                    result = await session.call_tool(tool_name, arguments={first_arg_name: "테스트"})
                else:
                    result = await session.call_tool(tool_name, arguments={})
                
                print(f"도구 호출 결과: {result}")


if __name__ == "__main__":
    import asyncio
    
    asyncio.run(run())