import os
import hashlib
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as msgbox
from tkinter.tix import ListNoteBook

##################################################################
# 추가 내역
#
# 불러올 파일과 다른 이름으로 저장할 파일 지정
#   : filedialog 함수를 이용
# 기본 '제목 없음'에 파일 이름으로 프로그램 타이틀 변경
#   : 저장할 때, 불러올 때 파일 이름 정보를 가져와 타이틀 변경 os.path.splitext(file.path)[0].split('/')[-1]
# 새로 만들기 함수 생성
#   : 텍스트 위젯의 내용을 모두 지우고 파일 이름과 경로 정보를 초기화하고 타이틀도 그에 맞게 변경
# 저장시 마지막 \n처리: # 저장시 마지막 \n처리
#   : get함수 사용 시 END까지 가져오면 끝에 \n을 가져오기에 가져오는 범위를 END에서 1c만큼 빼준다 note.get("1.0", END+"-1c")
# 타이틀 실시간 변경
#   : after함수를 써서 set_renew 함수를 1ms마다 호출
# 내용 변경 시 타이틀 앞에 *표시, 저장 시 사라짐
#   : fileinfo에 화면에 표시하지 않는 text위젯을 생성, 저장된 내용을 복사해 현재 편집중인 내용과 hashlib 모듈을 이용해 해쉬값을 비교, 반영
# 저장하지 않고 종료 시 경고 메시지 (예/아니오/취소)
#   : 위 사항의 해쉬값 비교 결과를 이용해 열기, 종료 시 저장 여부를 messagebox의 yesnocancel을 이용해 구현
# 끝내기 메뉴가 아닌 윈도우의 X버튼을 눌렀을 때도 끝내기와 같은 효과 부여
#   : Tk 클래스 내의 protocol 메소드를 써서 윈도우 닫힘을 제어하는 프로토콜(WM_DELETE_WINDOW)을 호출하여 프로토콜 제어 진행시 동작할 함수 지정

##################################################################
# 수정할 사항
#
# 단축키 지정
# 편집 메뉴 추가 (실행 취소//잘라내기, 복사, 붙여넣기, 삭제//찾기, 다음찾기, 이전찾기, 바꾸기, 이동//모두 선택, 시간/날짜)
# 서식 메뉴 추가 (자동 줄 바꿈(체크박스), 글꼴...)
# 보기 메뉴 추가 (확대하기/축소하기(추가메뉴- 확대, 축소, 기본값 복원), 상태 표시줄(체크박스))
# 도움말 메뉴 추가 (도움말 보기, 피드백 보내기//메모장 정보)
# 파일 메뉴 추가 (새 창//페이지 설정, 인쇄...)
# 우클릭 메뉴 추가 (실행 취소//잘라내기, 복사, 붙여넣기, 삭제//모두 선택//오른쪽에서 왼쪽으로 읽기)


# 타이틀, 변경상태 실시간 갱신 함수
def set_renew():
    txt_hash = hashlib.sha256()
    txt_hash.update(note.get("1.0", END+"-1c").encode('utf-8'))
    file_hash = hashlib.sha256()
    file_hash.update(file.txt.get("1.0", END+"-1c").encode('utf-8'))
    if file_hash.hexdigest() == txt_hash.hexdigest():
        file.modified = False
        root.title(f"{file.name} - 메모장")
    else:
        file.modified = True
        root.title(f"*{file.name} - 메모장")
    root.after(1, set_renew)

# 파일 정보 저장 클래스
class Fileinfo():
    def __init__(self):
        self.name = "제목 없음"
        self.path = "제목 없음"
        self.txt = Text()
        self.modified = False

# 새로 만들기
def new_file():
    file.name = "제목 없음"
    file.path = "제목 없음"
    note.delete("1.0", END)
    file.txt.delete("1.0", END)

# 새 창
def new_window():
    pass

# 열기
def open_file():
    ch = save_check()
    if ch == 1:
        save_file()
        return
    elif ch == 0:
        pass
    else:
        return
    path_tmp = filedialog.askopenfilename(initialdir="/",
                                        title="열기",
                                        filetypes=(("텍스트 문서(*.txt)", "*.txt"),
                                            ("모든 파일", "*.*")))
    if not path_tmp:
        return
    file.path = path_tmp
    file.name = os.path.splitext(file.path)[0].split('/')[-1]
    with open(file.path, "r", encoding="utf8") as note_file:
        note.delete("1.0", END)
        note.insert(END, note_file.read())
        note_file.seek(0) # read()로 끝까지 읽었으므로 포인터를 맨 앞으로 이동
        file.txt.delete("1.0", END)
        file.txt.insert(END, note_file.read())

# 저장
def save_file():
    if file.path == "제목 없음":
        save_as_file()
    else:
        try:
            with open(file.path, "w", encoding="utf8") as note_file:
                note_file.write(note.get("1.0", END+"-1c"))
            file.txt.delete("1.0", END)
            file.txt.insert(END, note.get("1.0", END+"-1c"))
        except Exception as err:
            msgbox.showerror("에러", err)

# 다른 이름으로 저장
def save_as_file():
    path_tmp = filedialog.asksaveasfilename(initialdir="/",
                                            title="다른 이름으로 저장",
                                            defaultextension=".txt",
                                            filetypes=(("텍스트 문서(*.txt)", "*.txt"),
                                                ("모든 파일", "*.*")))
    if not path_tmp:
        return
    file.path = path_tmp
    file.name = os.path.splitext(file.path)[0].split('/')[-1]
    with open(file.path, "w", encoding="utf8") as note_file:
        note_file.write(note.get("1.0", END+"-1c"))
    file.txt.delete("1.0", END)
    file.txt.insert(END, note.get("1.0", END+"-1c"))

# 저장 확인
def save_check():
    if file.modified == True:
        msg = msgbox.askyesnocancel(title="메모장", message=f"변경내용을 {file.path}에 저장하시겠습니까?")
        if msg == 1:
            return 1
        elif msg == 0:
            return 0
        else:
            return 2
    else:
        return 0

# 끝내기
def exit():
    ch = save_check()
    if ch == 1:
        save_file()
        return
    elif ch == 0:
        pass
    else:
        return
    root.destroy()

# 우클릭
class RightClick():
    def __init__(self):
        self.rmenu = Menu(root, tearoff=0)
        self.rmenu.add_command(label="실행 취소")
        self.rmenu.add_separator()
        self.rmenu.add_command(label="잘라내기")
        self.rmenu.add_command(label="복사")
        self.rmenu.add_command(label="붙여넣기")
        self.rmenu.add_command(label="삭제")
        self.rmenu.add_separator()
        self.rmenu.add_command(label="모두 선택")
        self.rmenu.add_separator()
        self.rmenu.add_command(label="오른쪽에서 왼쪽으로 읽기")
    def popup(self, event):
        try:
            self.rmenu.tk_popup(event.x_root, event.y_root)
        finally:
            self.rmenu.grab_release()

# 메인 창
root = Tk()
root.geometry("640x480")

# 메뉴
menu = Menu(root)
# 파일
menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="새로 만들기", command=new_file)
menu_file.add_command(label="새 창", command=new_window)
menu_file.add_command(label="열기...", command=open_file)
menu_file.add_command(label="저장", command=save_file)
menu_file.add_command(label="다른 이름으로 저장...", command=save_as_file)
menu_file.add_separator()
menu_file.add_command(label="페이지 설정")
menu_file.add_command(label="인쇄")
menu_file.add_separator()
menu_file.add_command(label="끝내기", command=exit)
menu.add_cascade(label="파일", menu=menu_file)
# 편집
menu_edit = Menu(menu, tearoff=0)
menu_edit.add_command(label="실행 취소")
menu_edit.add_separator()
menu_edit.add_command(label="잘라내기")
menu_edit.add_command(label="복사")
menu_edit.add_command(label="붙여넣기")
menu_edit.add_command(label="삭제")
menu_edit.add_separator()
menu_edit.add_command(label="찾기")
menu_edit.add_command(label="다음찾기")
menu_edit.add_command(label="이전찾기")
menu_edit.add_command(label="바꾸기")
menu_edit.add_command(label="이동")
menu_edit.add_separator()
menu_edit.add_command(label="모두 선택")
menu_edit.add_command(label="시간/날짜")
menu.add_cascade(label="편집", menu=menu_edit)
# 서식
menu_format = Menu(menu, tearoff=0)
menu_format.add_checkbutton(label="자동 줄 바꿈")
menu_format.add_command(label="글꼴...")
menu.add_cascade(label="서식", menu=menu_format)
# 보기
menu_view = Menu(menu, tearoff=0)
menu_exp_red = Menu(menu_view, tearoff=0)
menu_exp_red.add_command(label="확대")
menu_exp_red.add_command(label="축소")
menu_exp_red.add_command(label="기본값 복원")
menu_view.add_cascade(label="확대하기/축소하기", menu=menu_exp_red)
menu_view.add_checkbutton(label="상태 표시줄")
menu.add_cascade(label="보기", menu=menu_view)
# 도움말
menu_help = Menu(menu, tearoff=0)
menu_help.add_command(label="도움말 보기")
menu_help.add_command(label="피드백 보내기")
menu_help.add_separator()
menu_help.add_command(label="메모장 정보")
menu.add_cascade(label="도움말", menu=menu_help)

# 메모장 공간
scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")
note = Text(root, yscrollcommand=scrollbar.set)
note.pack(side="left", fill="both", expand=True)
scrollbar.config(command=note.yview)

file = Fileinfo()
set_renew()

root.config(menu=menu)
root.bind("<Button-3>", RightClick().popup)
root.protocol('WM_DELETE_WINDOW', exit)
root.mainloop()