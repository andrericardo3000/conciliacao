from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from app.main import process_files
from app.outputs.report_builder import build_summary_card
from app.ui.components import show_header


def main() -> None:
    st.set_page_config(page_title="Conciliador Universal", layout="wide")
    show_header()

    uploaded_files = st.file_uploader(
        "Envie PDF, TXT, CSV, XLS ou XLSX",
        type=["pdf", "txt", "csv", "xls", "xlsx"],
        accept_multiple_files=True,
    )

    if st.button("Processar arquivos", type="primary") and uploaded_files:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_paths: list[str] = []
            temp_dir_path = Path(temp_dir)

            for uploaded_file in uploaded_files:
                file_path = temp_dir_path / uploaded_file.name
                file_path.write_bytes(uploaded_file.getbuffer())
                input_paths.append(str(file_path))

            output_path = temp_dir_path / "resultado_conciliacao.xlsx"
            results = process_files(input_paths=input_paths, output_path=str(output_path))
            summary = build_summary_card(results)

            st.success("Processamento concluído.")

            if summary:
                cols = st.columns(min(len(summary), 4))
                for idx, (key, value) in enumerate(summary.items()):
                    cols[idx % len(cols)].metric(key, value)

            with open(output_path, "rb") as fp:
                st.download_button(
                    "Baixar Excel de resultado",
                    data=fp.read(),
                    file_name="resultado_conciliacao.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )


if __name__ == "__main__":
    main()
