# 🌙 ADMIN NIGHT
```
💭 ADMIN NIGHT?
'행정·관리'를 뜻하는 어드민(Admin)과 밤(Night)의 합성어.
술자리나 사교 모임 대신 한 공간에 모여 각자 미뤄둔 잡무(이메일 처리, 공과금 납부, 서류 정리 등)를 처리하는 새로운 모임 문화
```
터미널 기반 CLI 관리 프로그램입니다.<br>
**어드민 나잇의 시작 / 종료 시간**과 **참여 인원**을 관리하고,  <br>
**Discord Webhook**을 통해 실시간 알림을 전송합니다.

---

# 📌 기능

- ⏰ 시작 시간 자동 기록
- ⏳ 종료 시간 자동 계산
- 👥 참여 인원 입력 및 관리
- 🔔 Discord 시작 알림 전송
- ✅ Discord 종료 알림 전송
- ⚡ asyncio 기반 비동기 타이머 구현

---

# 🚀 사용법

### 1. 레포지토리 클론

```bash
git clone https://github.com/100-hours-a-week/KTB4-Margaux-AI
cd KTB4-Margaux-AI
```


### 2. 가상환경 설정

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

### 3. Dependencies 설정

```bash
pip3 install requests python-dotenv
pip3 install requests   
```


### 4. `.env`생성
알림을 받을 discord 웹훅 링크를 설정합니다.

```env
DISCORD_WEBHOOK_URL=YOUR_DISCORD_WEBHOOK_URL
```


### 5. 프로그램 시작.

```bash
python3 main.py
```

---
# 📷 실제 사용 예시
<img width="312" height="674" alt="스크린샷 2026-05-17 오후 11 24 09" src="https://github.com/user-attachments/assets/65197659-4977-4642-a1c8-8b4b959ab042" />

---
# ❗️느낀 점
- 어드민 나잇을 진행하면서 종료 알람의 필요성을 느꼈었다.
  <br>실제로 느낀 불편함을 과제를 통해 해결하였고, 앞으로 유용하게 잘 사용할 수 있을 것 같다.
- 수업에서 배운 비동기를 활용하여 timer 기능을 구현할 수 있었다.
  <br>이론을 실제 프로젝트에 적용하며 한층 성장함을 느꼈다.
---
# 💡 추가 발전 방향
1. 프로세스가 의도치않게 종료될 경우를 대비해 MQ에 종료 알림 요청 저장 -> 서버를 분리해 MSA 시스템 구현도 생각.
2. 인원 추가 / 삭제 기능 구현
3. 남은 시간 확인 기능 구현

---
# 📈 깃 전략

```text
Organization Repository
└── main
      ↑
      │ (Pull Request)
      │
Forked Repository
├── main
├── dev
└── feat/*
```

## 브랜치

| Branch | Description |
|---|---|
| `main` | 테스트 및 검증이 완료된 코드를 organization repository에 merge |
| `dev` | 기능 구현이 완료된 feature branch들을 통합 |
| `feat/*` | 개별 기능 개발 브랜치 |

---

