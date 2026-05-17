from datetime import datetime, timedelta
import asyncio

def init_print():
    banner = """
===========================================
    A D M I N   N I G H T
===========================================
    ( 인원 수 / 인원 명 )을 입력해주세요.
    """
    print(banner)

def input_members():
    count = int(input("인원 수를 입력하세요: "))

    members = []

    for i in range(count):
        name = input(f"{i + 1}번째 인원 이름: ")
        members.append(name)

    return members

async def end_timer(seconds):
    print(f"\n⏳ 타이머 시작 ({seconds}초 대기)\n")

    await asyncio.sleep(seconds)

    print("\n🔔 어드민 나잇 종료 시간입니다!")

async def main():
    # 시작시간: 현재시간
    start_time = datetime.now()
    # 종료시간: 현재시간 + 1시간
    end_time = start_time + timedelta(hours=1)

    members = input_members()
    
    
    # # 테스트용 3초 타이머
    # await end_timer(3)
    
    focus_time = (end_time - start_time).total_seconds()
    await end_timer(focus_time)

    print("\n===== 어드민 나잇 정보 =====")
    print(f"시작 시간: {start_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"종료 시간: {end_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"인원 수: {len(members)}")

    print("\n[인원 목록]")
    for member in members:
        print(f"- {member}")
    


if __name__ == "__main__":
    init_print()
    asyncio.run(main())