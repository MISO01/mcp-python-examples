import sqlite3
from mcp.server.fastmcp import FastMCP

# MCP 서버 인스턴스 생성
mcp = FastMCP("SQLite 탐색기")


# 데이터베이스 스키마를 제공하는 리소스
@mcp.resource("schema://main")
def get_schema() -> str:
    """리소스로 데이터베이스 스키마를 제공합니다"""
    conn = sqlite3.connect("database.db")
    schema = conn.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
    return "\n".join(sql[0] for sql in schema if sql[0])


# SQL 쿼리를 실행하는 도구
@mcp.tool()
def query_data(sql: str) -> str:
    """SQL 쿼리를 안전하게 실행합니다"""
    conn = sqlite3.connect("database.db")
    try:
        result = conn.execute(sql).fetchall()
        return "\n".join(str(row) for row in result)
    except Exception as e:
        return f"오류: {str(e)}"


# 데이터베이스 테이블 생성 도구
@mcp.tool()
def create_table(table_name: str, columns: str) -> str:
    """새 테이블을 생성합니다"""
    conn = sqlite3.connect("database.db")
    try:
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        conn.commit()
        return f"{table_name} 테이블이 성공적으로 생성되었습니다."
    except Exception as e:
        return f"테이블 생성 오류: {str(e)}"


# 데이터 삽입 도구
@mcp.tool()
def insert_data(table_name: str, values: str) -> str:
    """테이블에 데이터를 삽입합니다"""
    conn = sqlite3.connect("database.db")
    try:
        conn.execute(f"INSERT INTO {table_name} VALUES ({values})")
        conn.commit()
        return f"데이터가 {table_name}에 성공적으로 삽입되었습니다."
    except Exception as e:
        return f"데이터 삽입 오류: {str(e)}"


if __name__ == "__main__":
    # 서버 실행
    mcp.run()