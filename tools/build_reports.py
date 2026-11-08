import argparse
import html
import importlib.metadata
import json
import platform
import shutil
import sqlite3
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright
from report_data import WEB, TESTING

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/RealLalka/mdk-coursework-mironova-2026"
STUDENT = "Миронова Анна Андреевна"
GROUP = "4-ИСП9-46"
SUFFIX = "Миронова_Анна_Андреевна_4-ИСП9-46"
parser = argparse.ArgumentParser()
parser.add_argument("--workspace", type=Path, required=True)
args = parser.parse_args()
WORK = args.workspace
WORK.mkdir(parents=True, exist_ok=True)
DOCS = ROOT / "reports"
DOCS.mkdir(exist_ok=True)
CSS = """#title-block-header{display:none}@page{size:A4;margin:20mm 17mm 20mm}*{box-sizing:border-box}body{font-family:"Liberation Sans",Arial,sans-serif;font-size:10.5pt;line-height:1.52;color:#25362e;margin:0}a{color:#236148;overflow-wrap:anywhere}h1{font-size:25pt;line-height:1.2;font-weight:normal}h2{font-size:16pt;margin-top:25pt;padding-bottom:6pt;border-bottom:1px solid #cbd8cd;break-after:avoid}h3{font-size:12pt;margin-top:18pt;break-after:avoid}p{orphans:3;widows:3}pre{font-family:"Liberation Mono",monospace;font-size:8pt;line-height:1.4;padding:12pt;background:#f3f5f0;border:1px solid #dae1d8;white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word}code{font-family:"Liberation Mono",monospace;font-size:8.5pt}pre code{font-size:inherit}table{border-collapse:collapse;width:100%;font-size:8pt;margin:14pt 0;table-layout:fixed}th,td{border:1px solid #cbd8cd;padding:6pt;overflow-wrap:anywhere;text-align:left;vertical-align:top}th{background:#edf2e9}thead{display:table-header-group}tr{break-inside:avoid}img{display:block;max-width:100%;max-height:205mm;object-fit:contain;margin:12pt auto}figure{margin:16pt 0;break-inside:avoid}figcaption{font-size:9pt;color:#586b5e}.cover{height:245mm;display:flex;flex-direction:column;justify-content:center;page-break-after:always;border-top:7pt solid #2b5a43}.cover .course{font-size:12pt;letter-spacing:1pt;color:#607563}.cover .author{margin-top:30pt;font-size:12pt}.cover .meta{font-size:10pt;color:#607563;margin-top:30pt}.pagebreak{break-before:page}.listing{break-before:page}.listing h3{font-size:11pt}.note{background:#edf2e9;padding:12pt;border-left:3pt solid #6c8b74}"""
(WORK / "report.css").write_text(CSS)


def cover(course, title):
    return f'''<div class="cover"><p class="course">ПРАКТИЧЕСКАЯ РАБОТА · {course}</p><h1>{html.escape(title)}</h1><div class="author"><p>Выполнила: {STUDENT}<br>Группа: {GROUP}</p></div><div class="meta"><p>Преподаватель: А. Кондыбаева<br>Дата выполнения: 08.11.2026<br>Репозиторий: <a href="{REPO}">{REPO}</a></p></div></div>\n\n'''


def qa(items):
    return "\n## Ответы на контрольные вопросы\n\n" + "".join(
        f"### {i}. {question}\n\n{answer}\n\n"
        for i, (question, answer) in enumerate(items, 1)
    )


def shots(names):
    return "\n## Скриншоты и примеры выполнения\n\n" + "".join(
        f'<figure><img src="{"../evidence/screenshots/" + name + ".png"}" alt="{name}"><figcaption>Рисунок {i}. {name}. Фактический запуск; для консольных работ показан оформленный протокол вывода, для веб-приложений и Postman — интерфейс программы.</figcaption></figure>\n\n'
        for i, name in enumerate(names, 1)
    )


def code_appendix(directory):
    text = '\n<div class="pagebreak"></div>\n\n## Приложение. Листинги файлов\n\n'
    for path in sorted((ROOT / directory).rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or ".logs" in path.parts:
            continue
        if path.suffix not in [
            ".py",
            ".sh",
            ".html",
            ".css",
            ".json",
            ".csv",
            ".conf",
            ".feature",
        ]:
            continue
        lang = {
            ".py": "python",
            ".sh": "bash",
            ".html": "html",
            ".json": "json",
            ".css": "css",
        }.get(path.suffix, "text")
        text += f"### {path.relative_to(ROOT)}\n\n```{lang}\n{path.read_text().rstrip()}\n```\n\n"
    return text


def evidence(names):
    text = "\n## Протоколы проверок\n\n"
    for name in names:
        path = ROOT / "evidence" / f"{name}.md"
        if not path.exists():
            raise FileNotFoundError(path)
        data = path.read_text()
        if "```text\n" in data:
            output = data.split("```text\n", 1)[1].rsplit("```", 1)[0]
            text += f"### {name}\n\nПолный протокол: [evidence/{name}.md]({REPO}/blob/main/evidence/{name}.md).\n\n```text\n{output.strip()}\n```\n\n"
        else:
            text += data.replace("# ", "### ", 1) + "\n\n"
    return text


ENV = f"""## Стенд и воспроизведение

Фактическая ОС: Arch Linux в WSL/Linux, ядро {platform.release()}. Python {platform.python_version()}, SQLite {sqlite3.sqlite_version}, Flask {importlib.metadata.version("flask")}; браузер Chromium; настольный Postman 9.31.30 и Newman 6.2.1 для API-прогонов. Условия некоторых заданий называют РОСА и Python 3.8: переносимые команды выполнены на текущем Linux; совместимость именно с РОСА и Python 3.8 отдельным прогоном не подтверждена. Ограничения окружения отражены как WARN/SKIP, а не как успешные проверки.

Команды установки и запуска приведены в [README]({REPO}#readme). Полный автоматический прогон: `python tools/verify.py --workspace <новый-каталог-результатов> --newman <путь-к-newman>`. Он создаёт изолированные копии, запускает локальные сервисы и отрицательные сценарии, затем останавливает собственные процессы. Ненулевой код ожидается только в явно помеченных отрицательных опытах.

"""
SOURCES = """## Использованные материалы

Условия работ: репозитории softboxdev/programming_course и softboxdev/test_methodologies; точные ссылки и commit SHA зафиксированы в SOURCES.md.

Документация: [Python sqlite3](https://docs.python.org/3.14/library/sqlite3.html), [Python json](https://docs.python.org/3.14/library/json.html), [Flask Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/), [Postman Newman](https://learning.postman.com/docs/reference/newman-cli/command-line-integration-with-newman/).
"""
entries = []
for i, (title, functionality, complexity, images, questions) in enumerate(WEB, 1):
    stage = f"web/practice_{i:02}"
    command = (
        "python "
        + stage
        + ("/init_db.py" if i == 1 else "/crud_console.py" if i == 2 else "/app.py")
    )
    source = f"https://github.com/softboxdev/programming_course/blob/5a0653dd8acd2209367840687924e6be31715792/practice/{i:02}_practice_client_server_app.md"
    body = (
        cover("МДК.09.01", f"№{i}. {title}")
        + f"## Цель работы\n\nОсвоить: {title.lower()}.\n\nУсловие: [практическая работа №{i}]({source}).\n\n## Реализованный функционал\n\n{functionality}\n\n## Запуск\n\n```bash\n{command}\n```\n\n"
        + ENV
        + f"## Анализ сложности\n\n{complexity}\n\n"
        + shots(images)
        + qa(questions)
    )
    checks = {
        1: ["web01_init", "web01_repeat", "web01_schema", "additional_checks"],
        2: ["web02_console", "python_tests"],
        3: ["additional_checks", "compile"],
        4: ["python_tests"],
        5: ["python_tests"],
    }[i]
    body += (
        evidence(checks)
        + "\n## Вывод\n\nТребования выбранной практики реализованы. Результат проверен фактическим выполнением и автоматическими проверками; детали и границы проверки приведены выше.\n\n"
        + SOURCES
        + code_appendix(stage)
    )
    filename = f"МДК09_ПР{i:02}_{['SQLite', 'CRUD', 'Flask', 'Чтение', 'Форма'][i - 1]}_{SUFFIX}.pdf"
    entries.append((f"web{i:02}", filename, f"МДК.09.01 №{i}: {title}", stage, body))
for i, (
    slug,
    title,
    source,
    functionality,
    complexity,
    positive,
    negative,
    questions,
    extra,
) in enumerate(TESTING, 1):
    source_url = (
        "https://github.com/softboxdev/test_methodologies/blob/e428908592dc365348cf30024e3e61cbc9e97395/it_test_methodologies/"
        + source
    )
    body = (
        cover("МДК.05.03", title)
        + f"## Цель работы\n\nПроверить корректность работы ИС и научиться обнаруживать воспроизводимые дефекты.\n\nУсловие: [{source}]({source_url}).\n\n## Выполненная работа\n\n{functionality}\n\n"
        + ENV
        + f"## Анализ сложности\n\n{complexity}\n\n"
        + extra
    )
    images = [positive, negative]
    if slug == "postman":
        images = ["postman-desktop-response", "postman-desktop-tests", negative]
    body += shots(images) + qa(questions) + evidence([positive, negative])
    if slug == "json_validation":
        body += evidence(["json-benchmark", "json-pretty"])
    if (
        slug in ["linux_kernel", "json_validation", "bash_basics"]
        and (ROOT / "evidence/cron.md").exists()
    ):
        body += evidence(["cron"])
    if slug == "stlc":
        body += (
            "\n## Спецификация Gherkin\n\n```gherkin\n"
            + (ROOT / "testing/stlc/login.feature").read_text()
            + "```\n\n"
            + evidence(["stlc_restored", "stlc_public_example"])
        )
    body += (
        "\n## Вывод\n\nПоложительный и отрицательный прогоны разделены. Намеренный дефект обнаружен, исходные данные не повреждены. Полные протоколы и способ повторения входят в репозиторий; ограничения стенда явно указаны.\n\n"
        + SOURCES
        + code_appendix("testing/" + slug)
    )
    filename = f"МДК05_{i:02}_{slug}_{SUFFIX}.pdf"
    entries.append((slug, filename, "МДК.05.03: " + title, "testing/" + slug, body))
manifest = []
with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=shutil.which("chromium"),
        headless=True,
        args=["--no-sandbox", "--allow-file-access-from-files"],
    )
    page = browser.new_page()
    for key, filename, title, code, body in entries:
        md = DOCS / f"{key}.md"
        md.write_text(
            "\n".join(line.rstrip() for line in body.splitlines()).rstrip() + "\n"
        )
        target = WORK / f"{key}.html"
        subprocess.run(
            [
                "pandoc",
                str(md),
                "-s",
                "--no-highlight",
                "--metadata",
                "lang=ru",
                "--metadata",
                "title=" + title,
                "--css",
                (WORK / "report.css").as_uri(),
                "-o",
                str(target),
            ],
            check=True,
            capture_output=True,
        )
        target.write_text(
            target.read_text().replace(
                'src="../evidence/', 'src="' + (ROOT / "evidence").as_uri() + "/"
            )
        )
        page.goto(target.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        broken = page.locator("img").evaluate_all(
            "(els)=>els.filter(e=>!e.complete||e.naturalWidth===0).map(e=>e.src)"
        )
        if broken:
            raise RuntimeError(broken)
        page.pdf(
            path=str(ROOT / filename),
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template="<div></div>",
            footer_template='<div style="width:100%;font-size:8px;color:#66756b;padding:0 17mm;display:flex;justify-content:space-between"><span>Миронова А. А. · 4-ИСП9-46</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
            prefer_css_page_size=True,
        )
        manifest.append({"id": key, "pdf": filename, "title": title, "code": code})
        print("PDF", filename, flush=True)
    browser.close()
(ROOT / "reports/manifest.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
)
print("Created", len(manifest), "PDF reports")
