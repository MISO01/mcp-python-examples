from mcp.server.fastmcp import FastMCP

# MCP 서버 인스턴스 생성
mcp = FastMCP("에코 서버")


# 리소스 정의
@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """리소스로 메시지를 에코합니다"""
    return f"리소스 에코: {message}"


# 도구 정의
@mcp.tool()
def echo_tool(message: str) -> str:
    """도구로 메시지를 에코합니다"""
    return f"도구 에코: {message}"


# 프롬프트 정의
@mcp.prompt()
def echo_prompt(message: str) -> str:
    """에코 프롬프트를 생성합니다"""
    return f"이 메시지를 처리해주세요: {message}"


if __name__ == "__main__":
    # 서버 실행
    mcp.run()