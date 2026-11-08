import argparse
import contextlib
import html
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--workspace", type=Path, required=True)
args = parser.parse_args()
WORK = args.workspace
WORK.mkdir(parents=True, exist_ok=True)
SHOTS = ROOT / "evidence/screenshots"
SHOTS.mkdir(parents=True, exist_ok=True)


@contextlib.contextmanager
def serve(stage, db=None):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    log = (WORK / f"{stage}-server.log").open("w")
    process = subprocess.Popen(
        [sys.executable, ROOT / "web" / stage / "app.py"],
        env={**os.environ, "PORT": str(port), **({"TASK_DB": str(db)} if db else {})},
        stdout=log,
        stderr=log,
    )
    try:
        for _ in range(100):
            try:
                urlopen(f"http://127.0.0.1:{port}", timeout=0.5)
                break
            except OSError:
                if process.poll() is not None:
                    raise RuntimeError("Сервер завершился")
                time.sleep(0.1)
        else:
            raise RuntimeError("Сервер не запустился")
        yield f"http://127.0.0.1:{port}"
    finally:
        process.terminate()
        process.wait(timeout=5)
        log.close()


with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=shutil.which("chromium"), headless=True, args=["--no-sandbox"]
    )
    page = browser.new_page(
        viewport={"width": 1280, "height": 900}, device_scale_factor=1
    )
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    with serve("practice_03") as url:
        page.goto(url)
        assert page.get_by_role("heading", name="Hello, Flask!").is_visible()
        page.screenshot(path=str(SHOTS / "web03-home.png"), full_page=True)
        page.get_by_role("link", name="О проекте").click()
        assert page.get_by_role("heading", name="О проекте").is_visible()
        page.screenshot(path=str(SHOTS / "web03-about.png"), full_page=True)
        assert page.goto(url + "/nonexistent").status == 404
    for stage in ["practice_04", "practice_05"]:
        db = WORK / f"{stage}.db"
        with serve(stage, db) as url:
            page.goto(url)
            assert page.get_by_text("Список пуст", exact=True).is_visible()
            page.screenshot(path=str(SHOTS / f"{stage}-empty.png"), full_page=True)
            if stage == "practice_04":
                with sqlite3.connect(db) as conn:
                    conn.execute(
                        "INSERT INTO tasks(title) VALUES (?)",
                        ("Разобраться с Flask и SQLite",),
                    )
                    conn.execute(
                        "INSERT INTO tasks(title,status) VALUES (?,?)",
                        ("Создать базу данных", "done"),
                    )
                page.reload()
            else:
                page.get_by_label("Новая задача").fill(
                    "Подготовить отчёты по практическим работам"
                )
                with page.expect_response(
                    lambda r: r.request.method == "POST"
                ) as response:
                    page.get_by_role("button", name="Добавить").click()
                assert response.value.status == 302
                page.wait_for_load_state()
                page.reload()
                assert page.locator("li").count() == 1
                page.get_by_label("Новая задача").fill("'); DROP TABLE tasks; --")
                page.get_by_role("button", name="Добавить").click()
                page.wait_for_load_state()
                assert page.locator("li").count() == 2
            page.screenshot(path=str(SHOTS / f"{stage}-desktop.png"), full_page=True)
            page.set_viewport_size({"width": 390, "height": 844})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.screenshot(path=str(SHOTS / f"{stage}-mobile.png"), full_page=True)
            page.set_viewport_size({"width": 1280, "height": 900})
            if stage == "practice_05":
                page.get_by_label("Новая задача").fill("   ")
                page.get_by_role("button", name="Добавить").click()
                page.wait_for_load_state()
                assert page.get_by_role("alert").is_visible()
                page.screenshot(
                    path=str(SHOTS / "web05-validation.png"), full_page=True
                )
        if stage == "practice_05":
            with serve(stage, db) as url:
                page.goto(url)
                assert page.locator("li").count() == 2
                page.screenshot(
                    path=str(SHOTS / "web05-after-restart.png"), full_page=True
                )
    for name in [
        "web01_schema",
        "web02_console",
        "bash_basics_healthy",
        "bash_real_stop",
        "linux_kernel_healthy",
        "linux_kernel_stopped",
        "extended_healthy",
        "extended_broken_backup",
        "system_full",
        "system_after_fix",
        "stlc_healthy",
        "stlc_missing_robots",
        "jsonops_healthy",
        "jsonops_broken",
        "jsonval_healthy",
        "jsonval_syntax",
        "postman_positive",
        "postman_negative",
    ]:
        text = (ROOT / f"evidence/{name}.md").read_text()
        body = text.split("```text\n", 1)[1].rsplit("```", 1)[0]
        lines = body.splitlines()
        if len(lines) > 36:
            lines = (
                lines[:28]
                + ["… Полный протокол доступен в evidence/" + name + ".md"]
                + lines[-5:]
            )
        markup = (
            '<html lang="ru"><meta charset="utf-8"><style>body{margin:0;background:#f3f4ef;color:#243d36;font:16px Arial;padding:38px}h1{font-size:24px}p{font-size:13px;color:#5d7065}pre{font:15px/1.6 monospace;white-space:pre-wrap;overflow-wrap:anywhere;background:white;padding:24px;border:1px solid #d8dfd6;border-radius:8px}</style><h1>Протокол выполнения · '
            + html.escape(name)
            + "</h1><p>Миронова Анна Андреевна · 4-ИСП9-46 · Фактический вывод программы</p><pre>"
            + html.escape("\n".join(lines))
            + "</pre></html>"
        )
        file = WORK / f"{name}.html"
        file.write_text(markup)
        page.goto(file.as_uri())
        page.screenshot(path=str(SHOTS / f"{name}.png"), full_page=True)
    assert not errors, errors
    browser.close()
print("Playwright: routes, form, PRG, restart, mobile layout PASS; screenshots saved")
