import argparse
import contextlib
import datetime
import json
import os
import shutil
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--workspace", type=Path, required=True)
parser.add_argument("--newman", default="newman")
args = parser.parse_args()
WORK = args.workspace
WORK.mkdir(parents=True, exist_ok=True)
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)
results = []


def run(name, command, expected=0, env=None, cwd=None):
    result = subprocess.run(
        [str(x) for x in command],
        capture_output=True,
        text=True,
        env={**os.environ, **(env or {})},
        cwd=cwd or ROOT,
        timeout=90,
    )
    output = result.stdout + result.stderr
    (WORK / f"{name}.log").write_text(output)
    record = {
        "name": name,
        "expected_exit": expected,
        "actual_exit": result.returncode,
        "verified": result.returncode == expected,
    }
    results.append(record)
    (EVIDENCE / f"{name}.md").write_text(
        f"# Протокол: {name}\n\nДата: {datetime.datetime.now().astimezone().isoformat()}\n\nКоманда: `{shlex_join(command)}`\n\nОжидался код {expected}, получен {result.returncode}.\n\n```text\n{output}\n```\n"
    )
    print(
        f"{'OK' if record['verified'] else 'ERROR'} {name}: exit={result.returncode}, expected={expected}",
        flush=True,
    )
    return output


def shlex_join(command):
    import shlex

    return shlex.join(str(x) for x in command)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, directory=None, **kw):
        super().__init__(*a, directory=str(WORK / "http-data"), **kw)

    def do_GET(self):
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            super().do_GET()

    def log_message(self, *a):
        pass


@contextlib.contextmanager
def server():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    try:
        yield srv.server_port
    finally:
        srv.shutdown()
        srv.server_close()
        thread.join()


def clone_data(name):
    target = WORK / name
    if target.exists():
        raise RuntimeError(f"Каталог уже существует: {target}")
    shutil.copytree(ROOT / "testing" / name / "data", target)
    return target


def shell(name, lab, script="run_all.sh", expected=0, env=None, extra=()):
    return run(
        name,
        ["bash", ROOT / "testing" / lab / script, *extra],
        expected,
        {"QA_RUN": str(WORK / "runtime"), **(env or {})},
    )


http_data = WORK / "http-data"
http_data.mkdir(exist_ok=True)
(http_data / "index.html").write_text("<h1>Учебная ИС</h1>")
(http_data / "robots.txt").write_text("User-agent: *\nDisallow:\n")
(http_data / "favicon.ico").write_bytes(b"\x00\x00\x01\x00")
shutil.copy(ROOT / "testing/bash_basics/data/users.csv", http_data / "users.csv")
run(
    "python_tests",
    [sys.executable, "-m", "pytest", "-q", "--basetemp", WORK / "pytest"],
)
run(
    "compile",
    [
        sys.executable,
        "-m",
        "compileall",
        "-q",
        ROOT / "web",
        ROOT / "testing",
        ROOT / "tests",
        ROOT / "tools",
    ],
)
for path in sorted((ROOT / "testing").rglob("*.sh")):
    checked = subprocess.run(["bash", "-n", path], capture_output=True)
    if checked.returncode:
        raise RuntimeError(checked.stderr.decode())
run(
    "web01_init",
    [sys.executable, ROOT / "web/practice_01/init_db.py"],
    env={"TASK_DB": str(WORK / "web01.db")},
)
run(
    "web01_repeat",
    [sys.executable, ROOT / "web/practice_01/init_db.py"],
    env={"TASK_DB": str(WORK / "web01.db")},
)
run(
    "web01_schema",
    [sys.executable, ROOT / "web/practice_01/check_db.py"],
    env={"TASK_DB": str(WORK / "web01.db")},
)
console = subprocess.run(
    [sys.executable, ROOT / "web/practice_02/crud_console.py"],
    input="2\nПодготовить отчёт\n1\n3\n1\n1\n4\n1\n1\n3\nabc\n0\n",
    text=True,
    capture_output=True,
    env={**os.environ, "TASK_DB": str(WORK / "console.db")},
)
(EVIDENCE / "web02_console.md").write_text(
    "# Реальный сеанс консольного CRUD\n\n```text\n"
    + console.stdout
    + console.stderr
    + "\n```\n"
)
if console.returncode != 0 or "done" not in console.stdout:
    raise RuntimeError("Консольный CRUD не прошёл")
with server() as port, server() as port2:
    base = f"http://127.0.0.1:{port}"
    env = {
        "QA_URL": base + "/users.csv",
        "QA_HOST": "127.0.0.1",
        "QA_PORT": str(port),
        "QA_PID": str(os.getpid()),
    }
    for lab in ["bash_basics", "linux_kernel"]:
        shell(lab + "_healthy", lab, env=env)
        shell(
            lab + "_stopped",
            lab,
            expected=1,
            env={
                **env,
                "QA_URL": "http://127.0.0.1:1/users.csv",
                "QA_PORT": "1",
                "QA_PID": "99999999",
            },
        )
        data = clone_data(lab)
        with (data / "users.csv").open("a") as f:
            f.write("1,Duplicate,active\n")
        shell(
            lab + "_duplicate",
            lab,
            "test_unique_ids.sh",
            expected=1,
            env={**env, "QA_DATA": str(data)},
        )
    backup = WORK / "backup"
    run(
        "backup_setup", ["bash", ROOT / "testing/bash_extended/setup_backup.sh", backup]
    )
    ext_env = {
        "QA_BACKUP": str(backup),
        "QA_PORT1": str(port),
        "QA_PORT2": str(port2),
        "QA_CLOSED_PORT": "1",
    }
    shell("extended_healthy", "bash_extended", env=ext_env)
    with (backup / "backup.tar.gz").open("ab") as f:
        f.write(b"damage")
    shell(
        "extended_broken_backup",
        "bash_extended",
        "test_backup.sh",
        expected=1,
        env=ext_env,
    )
    data = clone_data("bash_extended")
    with (data / "app.conf").open("a") as f:
        f.write("user=\n")
    shell(
        "extended_empty_config",
        "bash_extended",
        "test_config.sh",
        expected=1,
        env={"QA_DATA": str(data)},
    )
    text = (data / "users.csv").read_text().replace("2,Мария", "1,Мария")
    (data / "users.csv").write_text(text)
    shell(
        "extended_duplicate_csv",
        "bash_extended",
        "test_csv.sh",
        expected=1,
        env={"QA_DATA": str(data)},
    )
    system_env = {
        "QA_URL_BASE": base,
        "QA_CONF": str(data / "app.conf"),
        "QA_APP_LOG": str(data / "app.log"),
    }
    (data / "app.conf").chmod(0o666)
    shell(
        "system_insecure_permissions",
        "linux_system",
        "integrity_check.sh",
        expected=1,
        env=system_env,
    )
    shell(
        "system_error_log", "linux_system", "log_check.sh", expected=1, env=system_env
    )
    shell("system_full", "linux_system", expected=1, env=system_env)
    (data / "app.conf").chmod(0o644)
    (data / "app.log").write_text("2026-11-08 10:00:00 INFO Сервер запущен\n")
    shell("system_after_fix", "linux_system", env=system_env)
    shell("stlc_healthy", "stlc", "run_stlc_tests.sh", extra=[base])
    (http_data / "robots.txt").rename(http_data / "robots.backup")
    shell("stlc_missing_robots", "stlc", "run_stlc_tests.sh", expected=1, extra=[base])
    (http_data / "robots.backup").rename(http_data / "robots.txt")
    shell("stlc_restored", "stlc", "run_stlc_tests.sh", extra=[base])
    run(
        "stlc_public_example",
        ["bash", ROOT / "testing/stlc/run_stlc_tests.sh", "https://example.com"],
        expected=1,
        env={"QA_RUN": str(WORK / "runtime")},
    )
# Серверы действительно остановлены
shell("bash_real_stop", "bash_basics", expected=1, env=env)
ops = WORK / "json_operations"
shutil.copytree(ROOT / "testing/json_operations", ops)
ops_env = {"JSON_DATA": str(ops)}
for script in [
    "01_write.py",
    "02_read.py",
    "04_format.py",
    "users_report.py",
    "warehouse_report.py",
]:
    run("jsonops_" + script[:-3], [sys.executable, ops / script], env=ops_env)
run("jsonops_healthy", ["bash", ops / "run_tests.sh"], env=ops_env)
run("jsonops_edit", [sys.executable, ops / "03_edit.py"], env=ops_env)
run("jsonops_after_edit", ["bash", ops / "run_tests.sh"], env=ops_env)
run(
    "jsonops_homework_edit",
    [sys.executable, ops / "03_edit.py", "--homework"],
    env=ops_env,
)
run(
    "jsonops_diff",
    [
        sys.executable,
        ops / "json_diff.py",
        ROOT / "testing/json_operations/user.json",
        ops / "user.json",
    ],
)
run("jsonops_pretty", [sys.executable, ops / "json_pretty.py", ops / "user.json"])
(ops / "user.json").write_text('{"name": "Иван",')
run(
    "jsonops_broken",
    [sys.executable, ops / "test_02_valid.py"],
    expected=1,
    env=ops_env,
)
run(
    "jsonops_json_tool_broken",
    [sys.executable, "-m", "json.tool", ops / "user.json"],
    expected=1,
)
run("jsonops_reset", [sys.executable, ops / "01_write.py"], env=ops_env)
run("jsonops_restored", ["bash", ops / "run_tests.sh"], env=ops_env)
for file in ["users_report.json", "warehouse_report.json"]:
    shutil.copy(ops / file, ROOT / "testing/json_operations" / file)
data = clone_data("json_validation")
shell("jsonval_healthy", "json_validation", env={"QA_DATA": str(data)})
for case in [
    "syntax",
    "missing",
    "type",
    "duplicate",
    "extra",
    "email",
    "encoding",
    "price",
    "status",
]:
    for name in ["users", "config", "products", "orders"]:
        shutil.copy(
            ROOT / f"testing/json_validation/data/{name}.json", data / f"{name}.json"
        )
    file = (
        "config"
        if case in ["missing", "type"]
        else "products"
        if case == "price"
        else "orders"
        if case == "status"
        else "users"
    )
    path = data / f"{file}.json"
    value = json.loads(path.read_text())
    if case == "syntax":
        path.write_text('{"users": [')
    elif case == "encoding":
        path.write_bytes(b"\xff")
    else:
        if case == "missing":
            del value["server"]["port"]
        if case == "type":
            value["server"]["port"] = "8080"
        if case == "duplicate":
            value["users"][1]["id"] = value["users"][0]["id"]
        if case == "extra":
            value["users"][0]["debug"] = True
        if case == "email":
            value["users"][0]["email"] = "a@"
        if case == "price":
            value["products"][0]["price"] = -1
        if case == "status":
            value["orders"][0]["status"] = "unknown"
        path.write_text(json.dumps(value, ensure_ascii=False))
    shell("jsonval_" + case, "json_validation", expected=1, env={"QA_DATA": str(data)})
shell("jsonval_restored", "json_validation")
run(
    "postman_positive",
    [
        args.newman,
        "run",
        ROOT / "testing/postman/homework.postman_collection.json",
        "-e",
        ROOT / "testing/postman/test.postman_environment.json",
        "--timeout-request",
        "15000",
        "--reporters",
        "cli,json",
        "--reporter-json-export",
        WORK / "postman-positive.json",
    ],
)
run(
    "postman_negative",
    [
        args.newman,
        "run",
        ROOT / "testing/postman/negative.postman_collection.json",
        "-e",
        ROOT / "testing/postman/test.postman_environment.json",
        "--timeout-request",
        "15000",
    ],
    expected=1,
)
(EVIDENCE / "verification.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2)
)
(EVIDENCE / "verification.md").write_text(
    "# Сводная проверка\n\n| Прогон | Ожидаемый код | Фактический код | Результат |\n|---|---:|---:|---|\n"
    + "".join(
        f"| {r['name']} | {r['expected_exit']} | {r['actual_exit']} | {'OK' if r['verified'] else 'ERROR'} |\n"
        for r in results
    )
)
print("VERIFIED", sum(r["verified"] for r in results), "/", len(results))
raise SystemExit(0 if all(r["verified"] for r in results) else 1)
