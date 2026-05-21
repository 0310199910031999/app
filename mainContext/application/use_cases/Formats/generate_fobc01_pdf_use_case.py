from typing import Any

from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_bc_01_repo import FOBC01Repo
from mainContext.domain.models.Formats.fo_bc_01 import FOBC01


class GenerateFoBc01PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, fobc01_repo: FOBC01Repo):
        self.pdf_generator = pdf_generator
        self.fobc01_repo = fobc01_repo

    @staticmethod
    def build_question_groups(answers: list[Any] | None) -> list[dict[str, Any]]:
        grouped_questions: dict[str, dict[str, Any]] = {}

        for answer in answers or []:
            question = getattr(answer, "fobc01_question", None)
            group_type = (getattr(question, "type", None) or "Sin categoría").strip() or "Sin categoría"
            description = getattr(question, "description", None) or "Sin descripción"

            group = grouped_questions.setdefault(
                group_type,
                {"type": group_type, "questions": []},
            )
            group["questions"].append(
                {
                    "id": getattr(answer, "id", None),
                    "question_id": getattr(question, "id", None),
                    "description": description,
                    "answer": getattr(answer, "answer", None),
                }
            )

        return list(grouped_questions.values())

    @staticmethod
    def build_battery_cell_rows(
        battery_cells: list[Any] | None,
        cells_x: int | None,
    ) -> list[list[Any]]:
        sorted_cells = sorted(
            battery_cells or [],
            key=lambda cell: (
                getattr(cell, "cell_number", 0) or 0,
                getattr(cell, "id", 0) or 0,
            ),
        )

        columns = cells_x if isinstance(cells_x, int) and cells_x > 0 else max(len(sorted_cells), 1)
        return [sorted_cells[index:index + columns] for index in range(0, len(sorted_cells), columns)]

    def execute(self, fobc01_id: int | None = None, data: FOBC01 | None = None) -> bytes:
        fobc01_data = data
        if fobc01_data is None:
            if fobc01_id is None:
                raise ValueError("Se requiere el id o el agregado FO-BC-01 para generar el PDF")
            fobc01_data = self.fobc01_repo.get_fobc01_by_id(fobc01_id)

        if not fobc01_data:
            raise ValueError(f"No se encontró el reporte FO-BC-01 con ID {fobc01_id}")

        question_groups = self.build_question_groups(fobc01_data.answers)
        battery_cell_rows = self.build_battery_cell_rows(
            fobc01_data.battery_cells,
            fobc01_data.cells_x,
        )

        return self.pdf_generator.generate_fobc01_pdf(
            data=dict(fobc01_data.__dict__),
            question_groups=question_groups,
            battery_cell_rows=battery_cell_rows,
        )