# main.py
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

console = Console()

# ================== CHECK THAM SỐ ==================
if len(sys.argv) != 3:
    console.print(
        "[bold red]❌ Sai cú pháp![/bold red]\n"
        "[yellow]👉 Dùng:[/yellow] python main.py <SDT_10_SO> <SO_LAN>\n"
        "[cyan]Ví dụ:[/cyan] python main.py 0987654321 50"
    )
    sys.exit(1)

phone = sys.argv[1]
count = sys.argv[2]

# ===== CHECK SĐT =====
if not phone.isdigit() or len(phone) != 10:
    console.print(
        "[bold red]❌ SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ![/bold red]\n"
        "[yellow]👉 Yêu cầu:[/yellow] đúng 10 chữ số\n"
        "[cyan]Ví dụ:[/cyan] 0987654321"
    )
    sys.exit(1)

# ===== CHECK SỐ LẦN =====
if not count.isdigit() or int(count) <= 0:
    console.print("[bold red]❌ SỐ LẦN PHẢI LÀ SỐ NGUYÊN > 0[/bold red]")
    sys.exit(1)

# ================== UI ==================
console.print(Align.center(Panel(
    "[bold yellow on blue]🌟 TOOL SPAM SMS / CALL 🌟[/bold yellow on blue]",
    subtitle="[italic magenta]MAIN CONTROLLER[/italic magenta]",
    border_style="yellow"
)))

console.print(f"[bold green]📱 SĐT:[/bold green] {phone}")
console.print(f"[bold cyan]🔢 Số lần:[/bold cyan] {count}\n")

# ================== MODULE LIST ==================
modules = [
    "call.py",
    "call1.py",
    "call2.py",
    "spam1.py",
    "spam2.py",
    "spam3.py",
    "spam4.py",
    "spam5.py",
    "spam6.py",
    "spam7.py",
    "spamcall.py",
]

processes = []

# ================== RUN MODULES ==================
for module in modules:
    console.print(f"[yellow]🚀 Chạy {module}[/yellow]")
    p = subprocess.Popen(
        ["python", module, phone, count],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    processes.append(p)

# ================== WAIT ==================
for p in processes:
    p.wait()

console.print(Align.center(Panel(
    "[bold white on green]🎉 TẤT CẢ MODULE ĐÃ HOÀN TẤT 🎉[/bold white on green]",
    border_style="green"
)))