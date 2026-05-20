from datetime import datetime, timedelta
import asyncio

import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
members = []

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

    global members
    members = []

    for i in range(count):
        name = input(f"{i + 1}번째 인원 이름: ")
        members.append(name)

    return members

def update_members():
    print("\n[인원 수정]")
    print("현재 인원 목록:")
    for idx, member in enumerate(members, start=1):
        print(f"{idx}. {member}")

    print("\n수정할 인원의 번호를 입력하세요 (예: 1 3 ...):")
    indices = input().split()

    updated = []
    for index in indices:
        idx = int(index) - 1
        if 0 <= idx < len(members):
            old_name = members[idx]
            new_name = input(f"{old_name} -> 새로운 이름: ")
            members[idx] = new_name
            updated.append(f"{old_name} -> {new_name}")
        else:
            print(f"잘못된 번호: {index}")

    if updated:
        details = "\n".join([f"• {line}" for line in updated])
        send_member_update_message("수정됨", details)
            
def remove_member():
    global members
    print("\n[인원 제거]")
    print("현재 인원 목록:")
    for idx, member in enumerate(members, start=1):
        print(f"{idx}. {member}")

    print("\n제거할 인원의 번호를 입력하세요 (예: 1 3 ...):")
    indices = input().split()

    removed = []
    remaining = []
    for idx, member in enumerate(members, start=1):
        if str(idx) in indices:
            removed.append(member)
        else:
            remaining.append(member)

    members = remaining
    if removed:
        details = "\n".join([f"• {name}" for name in removed])
        send_member_update_message("제거됨", details)


def add_member():
    global members
    print("\n[인원 추가]")
    new_name = input("추가할 인원의 이름을 입력하세요: ")
    members.append(new_name)
    send_member_update_message("추가됨", f"• {new_name}님이 추가되었습니다.")

def send_discord_message(title, description, color=0x5865F2):
    data = {
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color
            }
        ]
    }

    requests.post(WEBHOOK_URL, json=data)


def send_member_update_message(action, details=""):
    member_text = "\n".join([f"• {member}" for member in members]) if members else "없음"
    description = (
        f"**{action}**\n"
        f"{details}\n\n"
        f"👥 현재 인원 ({len(members)}명)\n"
        f"{member_text}"
    )

    send_discord_message(f"📝 ADMIN NIGHT MEMBER {action}", description, color=0xFEE75C)

async def get_input_async(prompt):
    """비동기로 사용자 입력을 받습니다"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)

def print_menu():
    """메뉴를 출력합니다"""
    menu = """
=== [ 인원 관리 메뉴 ] ===
1. 인원 추가
2. 인원 제거
3. 인원 수정
4. 인원 확인
5. 종료
=======================
"""
    print(menu)

async def end_timer(seconds, start_time, end_time):
    """타이머를 실행하면서 동시에 메뉴 입력을 받습니다"""
    global members
    
    timer_task = asyncio.create_task(timer_countdown(seconds))
    input_task = asyncio.create_task(menu_input_loop(start_time, end_time))
    
    # 두 작업 중 하나가 완료될 때까지 대기
    done, pending = await asyncio.wait(
        [timer_task, input_task],
        return_when=asyncio.FIRST_COMPLETED
    )
    
    # 남은 작업 취소
    for task in pending:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    
    print("\n🔔 어드민 나잇 종료 시간입니다!")

async def timer_countdown(seconds):
    """남은 시간을 표시하며 카운트다운합니다"""
    start = datetime.now()
    
    print(f"\n⏳ 타이머 시작 ({int(seconds)}초 대기)\n")
    
    while True:
        elapsed = (datetime.now() - start).total_seconds()
        remaining = max(0, seconds - elapsed)
        
        if remaining <= 0:
            break
        
        minutes = int(remaining // 60)
        secs = int(remaining % 60)
        print(f"\r⏰ 남은 시간: {minutes}분 {secs}초", end="", flush=True)
        
        await asyncio.sleep(1)
    
    print("\r" + " " * 50 + "\r", end="", flush=True)

async def menu_input_loop(start_time, end_time):
    """메뉴 입력을 받고 처리합니다"""
    global members
    
    while True:
        try:
            print_menu()
            choice = await get_input_async("선택: ")
            
            if choice == "1":
                add_member()
            elif choice == "2":
                remove_member()
            elif choice == "3":
                update_members()
            elif choice == "4":
                print_member_list()
            elif choice == "5":
                print("\n🔔 어드민 나잇을 조기 종료합니다.")
                break
            else:
                print("❌ 잘못된 선택입니다. 다시 시도하세요.")
        except Exception as e:
            print(f"오류 발생: {e}")
            break

def print_member_list():
    """현재 인원 목록을 출력합니다"""
    print("\n[현재 인원 목록]")
    if not members:
        print("인원이 없습니다.")
    else:
        for idx, member in enumerate(members, start=1):
            print(f"{idx}. {member}")
    print()

async def main():
    # 시작시간: 현재시간
    start_time = datetime.now()
    # 종료시간: 현재시간 + 1시간
    end_time = start_time + timedelta(hours=1)

    global members
    members = input_members()
    
    # 시작 알림
    member_text = "\n".join([f"• {member}" for member in members])

    description = (
        f"📅 **시작 시간**\n"
        f"{start_time.strftime('%Y-%m-%d %H:%M')}\n\n"

        f"⏰ **종료 시간**\n"
        f"{end_time.strftime('%Y-%m-%d %H:%M')}\n\n"

        f"👥 **참여 인원 ({len(members)}명)**\n"
        f"{member_text}"
    )

    send_discord_message(
        "🌙 ADMIN NIGHT START",
        description,
        color=0x57F287
    )
    
    print("\n===== 어드민 나잇 정보 =====")
    print(f"시작 시간: {start_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"종료 시간: {end_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"인원 수: {len(members)}")

    print("\n[인원 목록]")
    for member in members:
        print(f"- {member}")
    
    # # 테스트용 3초 타이머
    # await end_timer(3, start_time, end_time)
    
    focus_time = (end_time - start_time).total_seconds()
    await end_timer(focus_time, start_time, end_time)

    end_description = (
        f"\n✅ 어드민 나잇이 종료되었습니다.\n\n"
        f"📅 **시작 시간**\n"
        f"{start_time.strftime('%Y-%m-%d %H:%M')}\n\n"

        f"⏰ **종료 시간**\n"
        f"{end_time.strftime('%Y-%m-%d %H:%M')}\n\n"

        f"👥 **참여 인원 ({len(members)}명)**\n"
        f"{member_text}\n\n"
        f"👏 오늘 하루도 고생 많았습니다!"
    )

    send_discord_message(
        "🔔 ADMIN NIGHT END",
        end_description,
        color=0xED4245
    )
    

if __name__ == "__main__":
    init_print()
    asyncio.run(main())